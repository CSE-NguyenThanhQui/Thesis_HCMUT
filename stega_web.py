from flask import Flask, render_template, request, session, jsonify, redirect
import base64
import numpy as np
import stega as stega
from PIL import Image
from io import BytesIO
import time
import driver as driver

"""System information"""
overlay_name = "system"
app_version = "steganography.app_"
driver_version = "dev.582a3ccb.1"
version = "v1.2"

overlay = Overlay('./overlay/' +  overlay_name + '.bit')
cdma = driver.Cdma(overlay)
reg = driver.Register(overlay)
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
    SIZE_OF_BRAM = 5460
    image_buffer = allocate(shape=(image_shape[0],image_shape[1],image_shape[2]), dtype=np.uint8)
    secret_buffer = allocate(shape=(secret_size_pl), dtype=np.uint8)
    image_buffer[:] = image_data
    secret_buffer[:] = secret_data
    total_time = 0
    write_size = secret_size_pl
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
    return image_buffer

def hw_extract(mode, image_shape, image_data, image_size):
    cdma.reset()
    SIZE_OF_BRAM = 5460
    max_message_size = image_size // 2
    image_buffer = allocate(shape=(image_shape[0],image_shape[1],image_shape[2]), dtype=np.uint8)
    secret_buffer = allocate(shape=(max_message_size), dtype=np.uint8)
    image_buffer[:] = image_data
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
    return secret_buffer


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
   width = 1
   b = 2
   c = 3
   d = 4
   runtime = session.get('runtime', None)
   width = session.get('image_width', None)
   #height = session.get('image_height', None)
   return render_template('index.html', width=width, runtime=runtime, c=c, d=d)

@app.route('/index.html')
def index1():
   width = 1
   b = 2
   c = 3
   d = 4
   runtime = session.get('runtime', None)
   width = session.get('image_width', None)
   #height = session.get('image_height', None)
   return render_template('index.html', width=width, runtime=runtime, c=c, d=d)

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/test.html')
def test():
    return render_template('test.html')

@app.route('/extract.html')
def extract():
    return render_template('extract.html')

@app.route('/load_image', methods=['POST'])
def load_image():
    if 'image' not in request.files or 'secret' not in request.files:
        return render_template('test.html')  # No file uploaded, render the same page
    
    file = request.files['image']
    secret = request.files['secret']
    
    # Check if the files are valid
    if file.filename == '' or secret.filename == '':
        return render_template('test.html')  # No file selected, render the same page
    
    try:
        image_data, width, height = process_uploaded_image(file)
        secret_content = process_uploaded_secret(secret)

        original_shape = (170, 170, 3)
        arr = stega.read_image(file)
        secret_data = [int(digit, 16) for char in secret_content for digit in format(ord(char), '02x')]
        ########
        #hard_start = time.time()
        #image_embed = hw_embed(0, secret_size_pl, image_shape, image_data, secret_data)
        mod_data = hw_embed(0, 10, 170, image_data, secret_data)
        #hard_end = time.time()
        #output = Image.fromarray(image_embed)                    
        #print(f"Execution time on PL: {hard_end - hard_start} seconds")
        #print(f"Save image {img_name}_embed_pl.png to output file")
        #output.save(f"./output/{img_name}_embed_pl.png")
        #output.save(f"./input/{img_name}_stego.png")
        ########
        start_time = time.time()
        #arr = stega.embed_multiple(arr, secret_array)
        runtime = round(time.time() - start_time, 3)
        session['runtime'] = runtime
        mod_data = arr.reshape(original_shape)
        session['image_width'] = width
        image_b64 = base64_encode_image(image_data)
        mod_image = base64_encode_image(mod_data)

        return render_template('test.html', image=image_b64,data=image_data, width=width, height=height, mod_data=mod_data, mod_image=mod_image, secret_content=secret_content)
    
    except Exception as e:
        return render_template('test.html', error=str(e))

def process_uploaded_image(file):
    image = Image.open(file)
    data = np.array(image)
    return data, image.width, image.height

def process_uploaded_secret(secret):
    # Read the content of the secret file
    secret_content = secret.read().decode('utf-8')
    return secret_content

def base64_encode_image(data):
    image = Image.fromarray(data)
    with BytesIO() as buffer:
        image.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_b64


@app.route('/user-profile.html')
def user():
    return render_template('user-profile.html')

@app.route('/utility.html')
def utility():
    return render_template('utility.html')



if __name__ == '__main__':
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)

