from PIL import Image
import numpy as np
import time
import copy
import sys
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

#np.set_printoptions(threshold=sys.maxsize)

def embed(arr, secret):
    n = len(arr)
    for i in range(0,3):
        for j in range(0,3):
            if (arr[j] == 255):
                arr[j] = 254
            if (arr[j] == 0): 
                arr[j] = 1
            
    for i in range(0,3):
        f = sum(arr[i] * pow(3, i) for i in range(n))
        f = f % pow(3, 3)
    if f == secret:
        return arr
    else:
        s = (secret - f) % pow(3, 3)
        for i in range(n):
            modified_f = ((s - (pow(3, i) - 1) // 2 - 1) // pow(3, i)) % 3
            if s > ((pow(3, i) - 1) // 2) and modified_f == 0:
                arr[i] += 1
            if s > ((pow(3, i) - 1) // 2) and modified_f == 1:
                arr[i] -= 1
    return arr   

def embed_multiple(arr, secret_array):
    cnt = 0
    cnt_saturation = 0
    for i in range(0, len(arr), 3):
        if len(arr) % 3 != 0:
            raise ValueError("Invalid input sizes")
    for i in range(0,3):
        if (arr[i] == 255):
            cnt_saturation = cnt_saturation + 1
            arr[i] = 254
    for i in range(0,3):
        if (arr[i] == 0): 
            cnt_saturation = cnt_saturation + 1
            arr[i] = 1
    for i in range(0, len(arr), 3):
        arr[i:i+3] = embed(arr[i:i+3], secret_array[cnt])
        cnt = cnt + 1
        if (cnt >= len(secret_array)): 
            break
            #continue
        #else: 
        #    arr[i:i+3] = embed(arr[i:i+3], secret_array[cnt])
        #    cnt = cnt + 1
    #wav.write('new.wav', 22050, arr)
def extract(arr):
    for i in range(0,3):
        if (arr[i] == 256):
            arr[i] = 255
    for i in range(0,3):
        if (arr[i] == -1): 
            arr[i] = 0
    n = len(arr)
    for i in range(0,3):
        f = sum(arr[i] * pow(3, i) for i in range(n))
        f = f % pow(3, 3)
    return f

def extract_multiple(arr, length):
    extracted_values = []
    for i in range(0, len(arr), 3):
        if len(arr) % 3 != 0:
            raise ValueError("Invalid input sizes")
    
    for i in range(0, len(arr), 3):
        temp = extract(arr[i:i+3])
        if (i < length * 3):
            extracted_values.append(temp)
    #print("Extracted Values:", extracted_values)
    return extracted_values

def scoreboard(original_secret, extracted_values):
    if len(original_secret) != len(extracted_values):
        print("Error: Incompatible array sizes.")
        return

    correct_count = 0
    total_count = len(original_secret)

    for original, extracted in zip(original_secret, extracted_values):
        if original == extracted:
            correct_count += 1

    accuracy = (correct_count / total_count) * 100

    print("Scoreboard:")
    #print("Original Secret Array:", original_secret)
    #print("Extracted Values Array:", extracted_values)
    print("Correctly Extracted:", correct_count)
    print("Total Elements:", total_count)
    print("Accuracy: {:.2f}%".format(accuracy))

def read_image(filename):
    img = Image.open(filename)
    rgb_values = np.array(img)
    #print(rgb_values)
    flattened_values = rgb_values.flatten()
    return flattened_values

def read_secret(filename):
    with open(filename, 'r') as file:
        secret_text = file.read()
    #secret_arr  = np.array(odr(secret_text))
    #print(secret_text)
    secret_ascii = [int(digit, 16) for char in secret_text for digit in format(ord(char), '02x')]
    return secret_ascii

def calculate_metrics(image1_path, image2_path):
    # Open the images
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Convert images to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Ensure images have the same shape
    if arr1.shape != arr2.shape:
        raise ValueError("Input images must have the same shape")

    # Calculate MSE
    mse = np.mean((arr1 - arr2) ** 2)

    # Calculate PSNR
    psnr = peak_signal_noise_ratio(arr1, arr2)


    return mse, psnr
# Example usage:
#arr = read_image('1000.png')  # Assuming the size is a multiple of 3
#print(arr[0:900])
#secret_array = read_secret('secret.txt')  # Size must be len(arr) // 3
#length = len(secret_array)
#print(length)
#print(len(arr))
#if (length * 3 < len(arr)):
    #arr = [1,2,3]
        #secret_array = [5]
#    start_time = time.time()
#    embed_multiple(arr, secret_array)
#    res = extract_multiple(arr, length)
#    scoreboard(secret_array, res)
#    print("--- %s seconds ---" % (time.time() - start_time))
#else:
#    print("Error")

# Assuming the original image shape is (height, width, channels)
#original_shape = (1000, 1000, 3)  # Update with the actual shape of your original image
#print(arr.size)
# Reshape the modified array to the original shape
#modified_image = arr.reshape(original_shape)

# Save the modified image
#modified_image = Image.fromarray(modified_image.astype('uint8'))
#modified_image.save('modified_image.png')

# Example usage:
#original_image_path = '1000.png'
#modified_image_path = 'modified_image.png'

#mse_value, psnr_value = calculate_metrics(original_image_path, modified_image_path)
#print("MSE:", mse_value)
#print("PSNR:", psnr_value)
    
def process_folder(folder_id):
    cover_path = f"{folder_id}/cover.png"
    #cover_path = f"{folder_id}/a.wav"
    secret_path = f"{folder_id}/secret.txt"

    try:
        arr = read_image(cover_path)
        #sample_rate, arr = wav.read(cover_path)
        arr = arr[:84681]
        secret_array = read_secret(secret_path)
        length = len(secret_array)

        if length * 3 < len(arr):
            start_time = time.time()
            embed_multiple(arr, secret_array)
            etime = time.time() - start_time
            start_time = time.time()
            extracted_values = extract_multiple(arr, length)
            extime = time.time() - start_time
            scoreboard(secret_array, extracted_values)
            
            return {
                'ID': folder_id,
                'Embedding Time': etime,
                'Extracting Time': extime,
                'Secret_Length': length / 2
            }
        else:
            return {
                'ID': folder_id,
                'Error': "Error: Secret size exceeds image size"
            }

    except Exception as e:
        return {
            'ID': folder_id,
            'Error': str(e)
        }

def run_stega_for_all_folders():
    results = []

    for folder_id in range(1, 11):
        result = process_folder(folder_id)
        results.append(result)

    # Create a DataFrame from the results
    df = pd.DataFrame(results)

    # Write the DataFrame to an Excel file
    df.to_excel('stega_results.xlsx', index=False)

def visualize_results():
    # Read the Excel file
    df = pd.read_excel('stega_results.xlsx')

    # Check if the DataFrame is empty
    if df.empty:
        print("No data to visualize.")
        return

    # Plot a line graph with blue lines
    plt.plot(df['ID'], df['Runtime'], 'b-', label='Runtime')

    # Plot red points
    plt.scatter(df['ID'], df['Runtime'], color='red', label='Points')

    # Add a bar graph for Secret Length
    plt.bar(df['ID'], df['Secret_Length'], color='green', alpha=0.5, label='Secret Length')

    # Add a line connecting the points from 0 to 50
    plt.plot([df['ID'].min(), df['ID'].max()], [50, 50])

    # Annotate each red point with its value
    for i, value in enumerate(df['Runtime']):
        plt.annotate(f'{value:.2f}', (df['ID'][i], value), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8, color='black')

    plt.xlabel('Folder ID')
    plt.ylabel('Runtime (seconds) / Secret Length')
    plt.title('Stega Processing Runtime and Secret Length for Each Folder')
    plt.legend()
    plt.ylim(0, 50)  # Set y-axis limits from 0 to 50
    plt.xticks(df['ID'])  # Display all Folder IDs on the x-axis
    plt.savefig('stega_results_plot.png')

    plt.show()

if __name__ == '__main__':
    run_stega_for_all_folders()
    #visualize_results()