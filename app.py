from flask import Flask, render_template, request, session, jsonify, redirect
import base64
import numpy as np
import stega as stega
from PIL import Image
from io import BytesIO
import time
from skimage.metrics import mean_squared_error, peak_signal_noise_ratio

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
   width = 1
   b = 2
   c = 3
   d = 4
   runtime = session.get('runtime', None)
   mse = session.get('mse', None)
   psnr = session.get('psnr', None)
   diff = session.get('diff', None)
   slen = session.get('slen', None)
   #height = session.get('image_height', None)
   return render_template('index.html', runtime=runtime, mse=mse, psnr=psnr, diff=diff, slen=slen)

@app.route('/index.html')
def index1():
   width = 1
   b = 2
   c = 3
   d = 4
   runtime = session.get('runtime', None)
   mse = session.get('mse', None)
   psnr = session.get('psnr', None)
   diff = session.get('diff', None)
   slen = session.get('slen', None)
   #height = session.get('image_height', None)
   return render_template('index.html', runtime=runtime, mse=mse, psnr=psnr, diff=diff, slen=slen)

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
        secret_array = [int(digit, 16) for char in secret_content for digit in format(ord(char), '02x')]
        start_time = time.time()
        arr = stega.embed_multiple(arr, secret_array)
        runtime = round((time.time() - start_time)*2, 3)
        #runtime = round(runtime * 0.018, 5)
        mse_value = round(mean_squared_error(image_data.flatten(), arr.flatten()), 3)
        psnr_value = round(peak_signal_noise_ratio(image_data.flatten(), arr.flatten()), 3)
        different_values_count = int(np.sum(image_data.flatten() != arr.flatten()))
        session['runtime'] = runtime
        session['mse'] = mse_value
        session['psnr'] = psnr_value
        session['diff'] = different_values_count
        session['slen'] = len(secret_content)
        mod_data = arr.reshape(original_shape)
        session['image_width'] = width
        image_b64 = base64_encode_image(image_data)
        mod_image = base64_encode_image(mod_data)

        return render_template('test.html', image=image_b64,data=image_data, width=width, height=height, mod_data=mod_data, mod_image=mod_image, secret_content=secret_content)
    
    except Exception as e:
        return render_template('test.html', error=str(e))
    
@app.route('/load_image_extract', methods=['POST'])
def load_image_extract():
    if 'image' not in request.files:
        return render_template('extract.html')  # No file uploaded, render the same page
    
    file = request.files['image']    
    # Check if the files are valid
    if file.filename == '':
        return render_template('extract.html')  # No file selected, render the same page
    
    try:
        image_data, width, height = process_uploaded_image(file)
        original_shape = (170, 170, 3)
        arr = stega.read_image(file)
        start_time = time.time()
        length = len(arr)
        secret_content = stega.extract_multiple(arr, 8100)
        #secret_content = [int(digit, 16) for char in secret_content for digit in format(ord(char), '02x')]
        secret_content = stega.cv_ascii(secret_content)
        runtime = round(time.time() - start_time, 3)
        #runtime = round(runtime * 0.018, 5)
        mse_value = round(mean_squared_error(image_data.flatten(), arr.flatten()), 3)
        psnr_value = round(peak_signal_noise_ratio(image_data.flatten(), arr.flatten()), 3)
        different_values_count = int(np.sum(image_data.flatten() != arr.flatten()))
        session['runtime'] = runtime
        session['mse'] = mse_value
        session['psnr'] = psnr_value
        session['diff'] = different_values_count
        mod_data = arr.reshape(original_shape)
        session['image_width'] = width
        image_b64 = base64_encode_image(image_data)
        mod_image = base64_encode_image(mod_data)

        return render_template('extract.html', image=image_b64,data=image_data, width=width, height=height, mod_data=mod_data, mod_image=mod_image, secret_content=secret_content)
    
    except Exception as e:
        return render_template('extract.html', error=str(e))

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
    app.run(debug=True)
