from flask import Flask, render_template, request, session, jsonify, redirect
import base64
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def foo(data1):
    if (data1 < 150):
        data1 += 100
    return data1

@app.route('/')
def index():
   width = 1
   b = 2
   c = 3
   d = 4
   #data = session.get('image_data', None)
   width = session.get('image_width', None)
   #height = session.get('image_height', None)
   return render_template('index.html', width=width, b=b, c=c, d=d)

@app.route('/index.html')
def index1():
   width = 1
   b = 2
   c = 3
   d = 4
   #data = session.get('image_data', None)
   width = session.get('image_width', None)
   #height = session.get('image_height', None)
   return render_template('index.html', width=width, b=b, c=c, d=d)

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
        original_data = image_data
        original_width = width 
        original_height = height
        secret_content = process_uploaded_secret(secret)
        mod_data = foo(image_data)
        mod_width = width
        mod_height = height
        session['image_width'] = width
        
        original_image_b64 = base64_encode_image(original_data)
        mod_image_b64 = base64_encode_image(mod_data)
        return render_template('test.html', original_image=original_image_b64,original_data=original_data, original_width=original_width, original_height=original_height, mod_image=mod_image_b64, mod_data=mod_data, mod_height=mod_height,mod_width=mod_width,secret_content=secret_content)
    
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
    #app.run(debug=True)
    app.run(debug=True, host='127.0.0.1', port=5000)