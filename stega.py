from PIL import Image
import numpy as np
import time
import copy
import sys
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def embed(arr, secret):
    n = len(arr)
    for i in range(0,3):
        if (arr[i] == 0): 
            arr[i] = 1
        if (arr[i] == 255):
            arr[i] = 254
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
    for i in range(0, len(arr), 3):
        arr[i:i+3] = embed(arr[i:i+3], secret_array[cnt])
        cnt = cnt + 1
        if (cnt >= len(secret_array)): 
            break
    return arr
def extract(arr):
    n = len(arr)
    f = sum(arr[i] * pow(3, i) for i in range(n))
    f = f % pow(3, 3)
    return f

def extract_multiple(arr, length):
    extracted_values = []
    #if len(arr) % 3 != 0:
    #    raise ValueError("Invalid input sizes")

    for i in range(0, length * 3, 3):
        temp = extract(arr[i:i+3])
        extracted_values.append(temp)
    #print("Extracted Values:", extracted_values)
    return extracted_values
    #return arr

def cv_ascii(array):
    result = []
    for i in range(0, len(array), 2):
        num = array[i] * 16 + array[i + 1]
        result.append(chr(num))
    return ''.join(result)

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
    #with open(filename, 'r') as file:
    secret_text = filename.read().decode('utf-8')
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



