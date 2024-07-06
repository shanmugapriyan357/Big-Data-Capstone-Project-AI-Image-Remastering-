import os
import torch
from PIL import Image
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from RealESRGAN import RealESRGAN

def load_model(scale):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=scale, anime=False)
    model_path = {
        2: 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Real-ESRGAN-GFP\\Img-Upscale-AI\\model\\RealESRGAN_x2.pth',
        4: 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Real-ESRGAN-GFP\\Img-Upscale-AI\\model\\RealESRGAN_x4plus.pth',
        8: 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Real-ESRGAN-GFP\\Img-Upscale-AI\\model\\RealESRGAN_x8.pth'
    }[scale]
    model.load_weights(model_path)
    return model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    scale = int(request.form['scale'])
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join('uploads', filename)
    output_path = os.path.join('uploads', f'upscaled_{filename}')
    file.save(input_path)

    # Load model and perform the upscaling
    model = load_model(scale)
    image = Image.open(input_path).convert('RGB')
    sr_image = model.predict(image)
    sr_image.save(output_path)

    # Resize original image to match the enhanced image size
    enhanced_width, enhanced_height = sr_image.size
    resized_original_image = image.resize((enhanced_width, enhanced_height))
    resized_original_path = os.path.join('uploads', f'resized_{filename}')
    resized_original_image.save(resized_original_path)

    return jsonify({
        'resized_original_path': f'/uploads/resized_{filename}',
        'output_path': f'/uploads/upscaled_{filename}'
    })

@app.route('/uploads/<filename>')
def send_image(filename):
    return send_file(os.path.join('uploads', filename))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
