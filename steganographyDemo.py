from pynq import Overlay
from pynq import allocate
from pynq import MMIO
import driver as driver
from PIL import Image
import numpy as np
import time
import os
import pathlib
import shutil
import pandas as pd
import scipy.io.wavfile as wav
import cv2
import PIL
"""System information"""
overlay_name = "design_1"
app_version = "steganography.app_"
driver_version = "dev.582a3ccb.1"
version = "v1.2"

overlay = Overlay('./' +  overlay_name + '.bit')

reg_address = overlay.ip_dict['register_bank_0']['phys_addr']
print(reg_address)
cdma = driver.Cdma(overlay)
reg = driver.Register(overlay)
np.set_printoptions(threshold=np.inf)
def setup_system():
    secret_path = None
    success = True
    print("Select the operating mode for the Steganography system:")
    print("1. Embedding mode")
    print("2. Extracting mode")
    sel = int(input("Enter mode: "))
    if sel == 1:
        mode = 0
        img_name = input("Enter name of cover image: ")
        secret_name = input("Enter name of secret file: ")
        img_path = "./" + img_name
        secret_path = "./" + secret_name
        if os.path.isfile(img_path) == False:
            print("[Error] Input file: Cover image is not found")
            success = False
        if os.path.isfile(secret_path) == False:
            print("[Error] Input file: Secret file is not found")
            success = False
    elif sel == 2:
        mode = 1
        img_name = input("Enter name of stego image: ")
        s_length = input("Length of secret: ")
        img_path = "./" + img_name
        if os.path.isfile(img_path) == False:
            print("[Error] Input file: Cover image is not found")
            success = False
    else:
        print("[Error] Selection is invalid")
    return mode, img_path, secret_path, success, img_name, s_length

def load_image(img_path):
    image = Image.open(img_path)
    data = np.array(image)
    return data, image.width, image.height

def load_audio(cover_audio_path):
    sample_rate, audio_data = wav.read(cover_audio_path)
    wav.write(f"./test.wav", sample_rate, audio_data)
    image_like_array = audio_data.reshape((145, 145, 3))
    shape_0 = 145
    shape_1 = 145
    return image_like_array, shape_0, shape_1, sample_rate

def load_secret(secret_path):
    secret_file = open(secret_path,"r")
    secret_text = secret_file.read()
    data = np.frombuffer(bytes(secret_text, 'utf-8'), dtype=np.uint8)
    secret_file.close()
    return data

def conv_secret(secret_data):
    data = np.arange(len(secret_data) * 2)
    for i in range(0, len(secret_data)):
        secret_bin = bin(secret_data[i])[2:].zfill(8)
        data[i * 2] = int(secret_bin[0:4], 2)
        data[i * 2 + 1] = int(secret_bin[4:], 2)
    return data

def hw_process(mode, input_size):
    control = mode * 4 + 2
    reg.write(1 * 4, 1)
    reg.write(1 * 4, 0)
    reg.write(2 * 4, input_size)
    reg.write(3 * 4, input_size)
    hw_start = time.time()
    reg.write(1 * 4, control) # start engine
    status = reg.read(0)
    while (status == 0):
        status = reg.read(0)
    hw_end = time.time()
    return (hw_end - hw_start)

def hw_embed(mode, secret_size_pl, image_shape, image_data, secret_data):
    cdma.reset()
    SIZE_OF_BRAM = 54600
    image_buffer = allocate(shape=(image_shape[0],image_shape[1],image_shape[2]), dtype=np.uint8)
    secret_buffer = allocate(shape=(secret_size_pl), dtype=np.uint8)
    image_buffer[:] = image_data
    secret_buffer[:] = secret_data
    ######################################print(image_buffer[0:1])
    #print(secret_buffer[:1])
    total_time = 0
    write_size = secret_size_pl
    #print("secret_size_pl = " + str(write_size))
    i = 0
    #print("Perform PL Embed...", end="")
    if write_size <= SIZE_OF_BRAM:
        reg.write(1 * 4, 8)
        cdma.transfer(image_buffer.physical_address, driver.CDMA_BRAM_0, write_size * 6)
        cdma.transfer(secret_buffer.physical_address, driver.CDMA_BRAM_1, write_size)
        process_time = hw_process(mode, write_size)
        reg.write(1 * 4, 8)
        cdma.transfer(driver.CDMA_BRAM_0, image_buffer.physical_address, write_size * 6)
        total_time = total_time + process_time
    else:
        while write_size > SIZE_OF_BRAM:
            reg.write(1 * 4, 8)
            cdma.transfer(image_buffer.physical_address + SIZE_OF_BRAM * 6 * i, driver.CDMA_BRAM_0, SIZE_OF_BRAM * 6)
            cdma.transfer(secret_buffer.physical_address + SIZE_OF_BRAM * i, driver.CDMA_BRAM_1, SIZE_OF_BRAM)
            process_time = hw_process(mode, SIZE_OF_BRAM)
            reg.write(1 * 4, 8)
            cdma.transfer(driver.CDMA_BRAM_0, image_buffer.physical_address + SIZE_OF_BRAM * 6 * i,  SIZE_OF_BRAM * 6)
            total_time = total_time + process_time
            write_size = write_size - SIZE_OF_BRAM
            i = i + 1
        reg.write(1 * 4, 8)
        cdma.transfer(image_buffer.physical_address + SIZE_OF_BRAM * 6 * i, driver.CDMA_BRAM_0, write_size * 6)
        cdma.transfer(secret_buffer.physical_address + SIZE_OF_BRAM * i, driver.CDMA_BRAM_1, write_size)
        process_time = hw_process(mode, write_size)
        reg.write(1 * 4, 8)
        cdma.transfer(driver.CDMA_BRAM_0, image_buffer.physical_address + SIZE_OF_BRAM * 6 * i, write_size * 6)
        total_time = total_time + process_time
    #print("Done.")               
    #print(f"Number of phase processing: {i + 1}")
    #########################################Sprint(image_buffer[0:1])
    return image_buffer

def hw_extract(mode, image_shape, image_data, image_size):
    cdma.reset()
    SIZE_OF_BRAM = 54600
    max_message_size = image_size // 2
    image_buffer = allocate(shape=(image_shape[0],image_shape[1],image_shape[2]), dtype=np.uint8)
    secret_buffer = allocate(shape=(max_message_size), dtype=np.uint8)
    image_buffer[:] = image_data
    #print(image_buffer[:1])
    #print(secret_buffer[:])
    write_size = max_message_size
    total_time = 0
    end_flag = False
    i = 0
    #print("Perform PL Extract...", end="")
    if write_size < SIZE_OF_BRAM:
        #print("Loading data...")
        reg.write(1 * 4, 8)
        cdma.transfer(image_buffer.physical_address, driver.CDMA_BRAM_0, write_size * 6)
        process_time = hw_process(mode, write_size)
        reg.write(1 * 4, 8)
        cdma.transfer(driver.CDMA_BRAM_1, secret_buffer.physical_address, write_size)
        total_time = total_time + process_time
        end_iteration = np.where(secret_buffer == 35)
        num_end = len(end_iteration[0])
        if num_end >= 2:
            for j in range(1, num_end):
                if end_iteration[0][j] == end_iteration[0][j - 1] + 1:
                    secret_buffer = np.resize(secret_buffer, end_iteration[0][j] + 1)
                    break
    else:
        while write_size > SIZE_OF_BRAM:
            reg.write(1 * 4, 8)
            cdma.transfer(image_buffer.physical_address + SIZE_OF_BRAM * 6 * i, driver.CDMA_BRAM_0, SIZE_OF_BRAM * 6)
            process_time = hw_process(mode, SIZE_OF_BRAM)
            reg.write(1 * 4, 8)
            cdma.transfer(driver.CDMA_BRAM_1, secret_buffer.physical_address + SIZE_OF_BRAM * i, SIZE_OF_BRAM)
            total_time = total_time + process_time
            write_size = write_size - SIZE_OF_BRAM
            i = i + 1
            end_iteration = np.where(secret_buffer == 35)
            num_end = len(end_iteration[0])
            if num_end >= 2:
                for j in range(1, num_end):
                    if end_iteration[0][j] == end_iteration[0][j - 1] + 1:
                        end_flag = True
                        secret_buffer = np.resize(secret_buffer, end_iteration[0][j] + 1)
                        break    
            if end_flag:
                break
        if not end_flag:
            reg.write(1 * 4, 8)
            cdma.transfer(image_buffer.physical_address + SIZE_OF_BRAM * 6 * i, driver.CDMA_BRAM_0, write_size * 6)
            process_time = hw_process(mode, write_size)
            reg.write(1 * 4, 8)
            cdma.transfer(driver.CDMA_BRAM_1, secret_buffer.physical_address + SIZE_OF_BRAM * i, write_size)
            total_time = total_time + process_time
            end_iteration = np.where(secret_buffer == 35)
            num_end = len(end_iteration[0])
            if num_end >= 2:
                for j in range(1, num_end):
                    if end_iteration[0][j] == end_iteration[0][j - 1] + 1:
                        end_flag = True
                        secret_buffer = np.resize(secret_buffer, end_iteration[0][j] + 1)
                        break
    #print("Done.")                
    #print(f"Number of phase processing: {i + 1}")
    #print(secret_buffer[:1000])
    #for i in range(0, len(secret_buffer)):
        #print(chr(secret_buffer[i]))
    #s = "".join([chr(c) for c in secret_buffer])
    #print(type(secret_buffer))
    return secret_buffer

def main():
    print("+---------------------------------------------+")
    print("|    Welcome to hardware Steganography Demo   |")
    print("+---------------------------------------------+")
    print(f"|    App version   : {app_version}{version}   |")
    print("|    Driver version: " + driver_version + "           |")
    print("+---------------------------------------------+")
    print()
    
    print("Config hardware...")
    print("Hardware version: " + version)
    print()
    
    print("Type 'help' for instructions")
    print()
    
    mode = -1
    img_path = ""
    img_name = ""
    secret_path = ""
    success = False
    image_data = None
    secret_data = None
    secret_byte = None
    debug = False
    image_shape = [0, 0, 3]
    image_size = 0
    secret_size_ps = 0
    secret_size_pl = 0
    app_start = time.time()
    cmd = input(">>> ")
    while (cmd != "exit"):
        if cmd == "load":
            mode, img_path, secret_path, success, img_name, s_length = setup_system()
            img_name = pathlib.PureWindowsPath(img_name).stem
            if success == True:
                if mode == 0:
                    image_data, image_shape[0], image_shape[1] = load_image(img_path)
                    secret_data = load_secret(secret_path)
                    secret_byte = conv_secret(secret_data)
                    image_size = image_shape[0] * image_shape[1]
                    secret_size_ps = len(secret_byte)
                    secret_size_pl = len(secret_data)
                    if secret_size_ps > image_size:
                        print("[Error] Secret text too large")
                elif mode == 1:
                    image_data, image_shape[0], image_shape[1] = load_image(img_path)
                    image_size = image_shape[0] * image_shape[1]
                else:
                    print("[Error] Operating mode is invalid")
        elif cmd == "pl_embed":
            if mode == 0:
                hard_start = time.time()
                image_embed = hw_embed(mode, secret_size_pl, image_shape, image_data, secret_data)
                hard_end = time.time()
                output = Image.fromarray(image_embed)                    
                print(f"Execution time on PL: {hard_end - hard_start} seconds")
                print(f"Save image {img_name}_embed_pl.png to output file")
                output.save(f"./{img_name}_embed_pl.png")
                output.save(f"./{img_name}_stego.png")
            else:
                print("[Error] Operating mode for command: hw_embed is invalid")
        elif cmd == "pl_extract":
            if mode == 1:
                hard_start = time.time()
                message = hw_extract(mode, image_shape, image_data, image_size)
                hard_end = time.time()                    
                print(f"Execution time on PL: {hard_end - hard_start} seconds")
                str_message = ''.join(map(chr, message))
                s_length = int(s_length)
                str_message = str_message[:s_length]
                print(f"Save message text {img_name}_message_pl.txt to output file")
                message_file = open(f"./{img_name}_message_pl.txt", "w")
                message_file.write(str_message)
                message_file.close()
                shutil.copyfile(f"./{img_name}_message_pl.txt", f"./{img_name}_pl.txt")
            else:
                print("[Error] Operating mode for command: hw_extract is invalid")
        elif cmd == "pl_reset":
            print("Hardware reset...")
            cdma.reset()
            reg.write(1 * 4, 1)
            reg.write(1 * 4, 0)
        elif cmd == "help":
            print("     load      : load data from microSD card")
            print("     pl_embed  : perform embedding with accelerate system")
            print("     pl_extract: perform extracting with accelerate system")
            print("     pl_reset  : soft reset CDMA and system")
            print("     exit      : exit program")
        else:
            print(f"[Error] Command {cmd} is not supported")  
        print()
        cmd = input(">>> ")
    app_end = time.time()
    print(f"Application usage time: {app_end - app_start} seconds")
def compare_secret(original_secret_path, extracted_secret):
    try:
        with open(original_secret_path, 'r') as original_file:
            original_content = original_file.read()
        if original_content == extracted_secret:
            print("Secret content matches between original and extracted.")
            return True
        else:
            print("Error: Secret content does not match between original and extracted.")
            return False
    except FileNotFoundError:
        print(f"Error: Original secret file not found at {original_secret_path}.")
        return False    

def quicktest():
    results = []
    for i in range(1, 11):
        folder_name = str(i)
        cover_image_path = f"./{folder_name}/cover.png"
        secret_text_path = f"./{folder_name}/secret.txt"
        
        if os.path.isfile(cover_image_path) and os.path.isfile(secret_text_path):
            print(f"\nProcessing folder {folder_name}...")
            image_data, image_shape_0, image_shape_1 = load_image(cover_image_path)
            secret_data = load_secret(secret_text_path)
            secret_byte = conv_secret(secret_data)
            secret_len = len(secret_data)
            image_size = image_shape_0 * image_shape_1
            secret_size_ps = len(secret_byte)
            secret_size_pl = len(secret_data)

            if secret_size_ps > image_size:
                print("[Error] Secret text too large")
                continue

            # Embedding
            hard_start = time.time()
            image_embed = hw_embed(0, secret_size_pl, [image_shape_0, image_shape_1, 3], image_data, secret_data)
            hard_end = time.time()

            output_embedded = Image.fromarray(image_embed)
            output_embedded.save(f"./{folder_name}/cover_embedded.png")
            output_embedded.save(f"./{folder_name}/stego.png")
            embed_time = hard_end - hard_start
            print(f"Embedding time of test folder {folder_name}:  {embed_time} seconds")
            #print(f"Saved embedded image of test folder {folder_name}")

            # Extraction
            hard_start = time.time()
            message = hw_extract(1, [image_shape_0, image_shape_1, 3], image_embed, image_size)
            hard_end = time.time()

            str_message = ''.join(map(chr, message))
            extract_time = hard_end - hard_start
            print(f"Extracting time of test folder {folder_name}: {extract_time} seconds")
            print(f"Length of secret text: {secret_len}")
            message_file = open(f"./{folder_name}/extracted_message_pl.txt", "w")
            str_message = str_message[:secret_len]
            message_file.write(str_message)
            message_file.close()
            
             # Compare secret
            compare_result = compare_secret(secret_text_path, str_message)
            results.append({
                'ID': folder_name,
                'Secret Length': secret_len,
                'Verification': compare_result,
                'Embedding Time': embed_time,
                'Extracting Time': extract_time
            })
            if compare_result:
                print("Secret content verification passed.")
                message_file = open(f"./{folder_name}/extracted_message_pl.txt", "w")
                message_file.write(str_message)
                message_file.close()
            else:
                print("Secret content verification failed.")
        else:
            print(f"[Error] Missing files in folder {folder_name}")
    df_results = pd.DataFrame(results)
    df_results.to_excel('verification_results.xlsx', index=False)
def quicktest_audio():
    results = []
    for i in range(11, 12):
        folder_name = str(i)
        cover_image_path = f"./{folder_name}/cover.wav"
        secret_text_path = f"./{folder_name}/secret.txt"
        
        if os.path.isfile(cover_image_path) and os.path.isfile(secret_text_path):
            print(f"\nProcessing folder {folder_name}...")
            image_data, image_shape_0, image_shape_1, sample_rate = load_audio(cover_image_path)
            secret_data = load_secret(secret_text_path)
            secret_byte = conv_secret(secret_data)
            secret_len = len(secret_data)
            image_size = image_shape_0 * image_shape_1
            secret_size_ps = len(secret_byte)
            secret_size_pl = len(secret_data)

            if secret_size_ps > image_size:
                print("[Error] Secret text too large")
                continue

            # Embedding
            hard_start = time.time()
            image_embed = hw_embed(0, secret_size_pl, [image_shape_0, image_shape_1, 3], image_data, secret_data)
            hard_end = time.time()

            image_embed_flatten = image_embed.flatten()
            print (sample_rate)
            print (len(image_embed_flatten))
            image_embed_flatten = np.int16(np.clip(image_embed_flatten, -32768, 32767))
            wav.write(f"./{folder_name}/cover_embedded.wav", sample_rate, image_embed_flatten)
            embed_time = hard_end - hard_start
            print(f"Embedding time of test folder {folder_name}:  {embed_time} seconds")
            #print(f"Saved embedded image of test folder {folder_name}")

            # Extraction
            hard_start = time.time()
            message = hw_extract(1, [image_shape_0, image_shape_1, 3], image_embed, image_size)
            hard_end = time.time()

            str_message = ''.join(map(chr, message))
            extract_time = hard_end - hard_start
            print(f"Extracting time of test folder {folder_name}: {extract_time} seconds")
            print(f"Length of secret text: {secret_len}")
            message_file = open(f"./{folder_name}/extracted_message_pl.txt", "w")
            str_message = str_message[:secret_len]
            message_file.write(str_message)
            message_file.close()
        else:
            print(f"[Error] Missing files in folder {folder_name}")


def quicktest_video():
    results = []
    for i in range(1, 11):
        folder_name = str(i)
        cover_image_path = f"./{folder_name}/cover.mp4"
        secret_text_path = f"./{folder_name}/secret.txt"
        output = cv2.VideoWriter( 
        "./{folder_name}/output.avi", cv2.VideoWriter_fourcc(*'MPEG'), 30, (1920, 1080), True) 
        if os.path.isfile(cover_image_path) and os.path.isfile(secret_text_path):
            print(f"\nProcessing folder {folder_name}...")

            cap = cv2.VideoCapture(cover_image_path)
            if not cap.isOpened():
                print("Error: Could not open video file.")
                exit()
        frames = []
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            if (i == 0):
                crop = frame[0:70, 0:70]

                crop[:, :] = [0, 0, 0]
                ###############
                image_data = crop
                image_shape_0 = 70
                image_shape_1 = 70
                secret_data = load_secret(secret_text_path)
                secret_byte = conv_secret(secret_data)
                secret_len = len(secret_data)
                image_size = image_shape_0 * image_shape_1
                secret_size_ps = len(secret_byte)
                secret_size_pl = len(secret_data)
                if secret_size_ps > image_size:
                    print("[Error] Secret text too large")
                    continue
                hard_start = time.time()
                image_embed = hw_embed(0, secret_size_pl, [image_shape_0, image_shape_1, 3], image_data, secret_data)
                hard_end = time.time()

                hard_start = time.time()
                message = hw_extract(1, [image_shape_0, image_shape_1, 3], image_embed, image_size)
                hard_end = time.time()

                str_message = ''.join(map(chr, message))
                extract_time = hard_end - hard_start
                print(f"Extracting time of test folder {folder_name}: {extract_time} seconds")
                print(f"Length of secret text: {secret_len}")
                message_file = open(f"./{folder_name}/extracted_message_pl.txt", "w")
                str_message = str_message[:secret_len]
                message_file.write(str_message)
                message_file.close()
                ###############
                frame[0:70, 0:70] = image_data
            output.write(frame) 
            cv2.imshow("output", frame) 
            if cv2.waitKey(1) & 0xFF == ord('s'): 
                break
            i = i + 1
            cv2.imwrite("my_img.png", frames[0])
            cv2.destroyAllWindows()
            cap.release()
            output.release()
            
quicktest()
#quicktest_audio()