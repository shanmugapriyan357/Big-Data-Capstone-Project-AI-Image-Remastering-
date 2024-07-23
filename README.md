# # Big-Data-Capstone-Project-AI-Image-Remastering-
AI Image Remastering

# AI Image Remastering - Big Data Capstone Project

This project leverages the Real-ESRGAN model for image restoration. It features a web interface built using Flask, allowing users to upload low-resolution images, enhance them using the model, and download the restored images.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Model Evaluation](#model-evaluation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Real-ESRGAN model, based on the RRDBNet architecture, is designed to enhance low-resolution images. This project integrates the model into a Flask web application, providing an easy-to-use interface for image restoration tasks.

## Features

- Upload low-resolution images.
- Enhance images using the Real-ESRGAN model.
- Download the restored images.
- Evaluate model performance using metrics like PSNR and VGG Loss.

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/shanmugapriyan357/Big-Data-Capstone-Project-AI-Image-Remastering-.git
    cd Big-Data-Capstone-Project-AI-Image-Remastering-
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download the Real-ESRGAN model:**
    Download the model files and place them in the appropriate directory. You can find the models [here](https://github.com/xinntao/Real-ESRGAN).

## Usage

1. **Run the Flask application:**
    ```bash
    python app.py
    ```

2. **Open your browser and go to:**
    ```
    http://127.0.0.1:5000
    ```

3. **Use the web interface to upload and enhance images:**
    - Click on "Upload Image" to select a low-resolution image.
    - Click on "Enhance Image" to process the uploaded image.
    - Download the enhanced image once processing is complete.

## Model Evaluation

The model has been evaluated on a validation set using the following metrics:

- **Average PSNR:** 32.65 dB
- **Average VGG Loss:** 0.0628

Visual inspection confirmed that while the model generally performs well, some artifacts may appear on certain images, particularly those with human faces.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
