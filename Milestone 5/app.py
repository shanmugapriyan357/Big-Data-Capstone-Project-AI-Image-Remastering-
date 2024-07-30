
import os
import torch
from PIL import Image
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from RealESRGAN import RealESRGAN

# Function to load the model based on scale and anime toggle
def load_model(scale, anime=False):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=scale, anime=anime)
    model_path = {
        (2, False): 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Capstone_Project\\model\\RealESRGAN_x2.pth',
        (4, False): 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Capstone_Project\\model\\RealESRGAN_x4plus.pth',
        (8, False): 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Capstone_Project\\model\\RealESRGAN_x8.pth',
        (4, True): 'C:\\Users\\Admin\\Downloads\\Term 3\\Big Data Capstone Project\\Capstone_Project\\model\\RealESRGAN_x4plus_anime_6B.pth'
    }[(scale, anime)]
    model.load_weights(model_path)
    return model

# Function to load the face enhancer model (removed for simplicity)
# Add back if needed

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
    anime = request.form.get('anime') == 'true'
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    filename = secure_filename(file.filename)
    input_path = os.path.join('uploads', filename)
    output_path = os.path.join('uploads', f'upscaled_{filename}')
    file.save(input_path)

    # Load model and perform the upscaling
    model = load_model(scale, anime=anime)
    image = Image.open(input_path).convert('RGB')
    sr_image = model.predict(image)
    
    # Save the enhanced image
    sr_image.save(output_path)

    # Get image dimensions
    original_width, original_height = image.size
    enhanced_width, enhanced_height = sr_image.size

    return jsonify({
        'original_path': f'/uploads/{filename}',
        'output_path': f'/uploads/upscaled_{filename}',
        'original_width': original_width,
        'original_height': original_height,
        'output_width': enhanced_width,
        'output_height': enhanced_height
    })

@app.route('/uploads/<filename>')
def send_image(filename):
    return send_file(os.path.join('uploads', filename))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
