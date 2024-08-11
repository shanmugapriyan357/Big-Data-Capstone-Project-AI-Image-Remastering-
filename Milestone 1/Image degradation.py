import os
import cv2
import numpy as np
from PIL import Image
from pathlib import Path

def downsample_image(image, scale_factor):
    height, width = image.shape[:2]
    new_dimensions = (int(width / scale_factor), int(height / scale_factor))
    downsampled_image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)
    return downsampled_image

def add_noise(image, noise_level):
    noise = np.random.normal(0, noise_level, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, noise)
    return noisy_image

def compress_image(image, compression_factor):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), compression_factor]
    _, compressed_image = cv2.imencode('.jpg', image, encode_param)
    return cv2.imdecode(compressed_image, 1)

def resize_and_pad_image(image, target_size=(256, 256)):
    height, width = image.shape[:2]
    new_size = (max(width, height), max(width, height))

    # Create a new image with a white background
    padded_image = np.full((new_size[1], new_size[0], 3), 255, dtype=np.uint8)

    # Calculate center position
    top = (new_size[1] - height) // 2
    left = (new_size[0] - width) // 2

    # Place the original image in the center
    padded_image[top:top + height, left:left + width] = image

    # Resize to the target size
    resized_image = cv2.resize(padded_image, target_size, interpolation=cv2.INTER_AREA)

    return resized_image

def process_image(image_path, output_path, scale_factor=4, noise_level=10, compression_factor=50):
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to read image {image_path}")
        return

    # Degrade the image
    downsampled_image = downsample_image(image, scale_factor)
    noisy_image = add_noise(downsampled_image, noise_level)
    degraded_image = compress_image(noisy_image, compression_factor)
    
    # Resize and pad the image to 256x256
    final_image = resize_and_pad_image(degraded_image, target_size=(256, 256))
    
    # Save the final image
    cv2.imwrite(str(output_path), final_image)

# Paths to the input and output folders
input_folder = Path("C:/Users/Admin/Downloads/Term 3/Big Data Capstone Project/High res images/archive/dataset/Raw Data/high_res/")
output_folder = Path("C:/Users/Admin/Downloads/Term 3/Big Data Capstone Project/High res images/archive/dataset/Raw Data/low_res/")
output_folder.mkdir(parents=True, exist_ok=True)

# Process all images in the input folder
for image_file in input_folder.glob("*.png"):
    output_file = output_folder / image_file.name
    process_image(image_file, output_file)
