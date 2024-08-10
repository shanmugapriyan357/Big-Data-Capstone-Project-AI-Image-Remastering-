import streamlit as st
from PIL import Image
import torch
from RealESRGAN import RealESRGAN
from io import BytesIO

# Define the target size for the image
TARGET_SIZE = (240, 240)

# Function to load the model based on scale and anime toggle
def load_model(scale, anime=False):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=scale, anime=anime)
    model_path = {
        (2, False): 'model/RealESRGAN_x2.pth',
        (4, False): 'model/RealESRGAN_x4plus.pth',
        (8, False): 'model/RealESRGAN_x8.pth',
        (4, True): 'model/RealESRGAN_x4plus_anime_6B.pth'
    }[(scale, anime)]
    model.load_weights(model_path)
    return model

def enhance_image(image, scale, anime):
    model = load_model(scale, anime=anime)
    
    # Convert image to RGB if it has an alpha channel
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize image to target dimensions
    image = image.resize(TARGET_SIZE)
    
    sr_image = model.predict(image)
    
    buffer = BytesIO()
    sr_image.save(buffer, format="PNG")
    buffer.seek(0)
    return sr_image, buffer

def main():
    st.title("Generative AI Image Restoration")

    # Image upload
    uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        
        # Anime toggle
        anime = st.checkbox("Anime Image", value=False)
        
        # Conditional scale options
        if anime:
            scale = "4x"  # Set to 4x automatically when anime is selected
        else:
            scale = st.radio("Upscaling Factor", ["2x", "4x", "8x"], index=0)
        
        scale_value = int(scale.replace('x', ''))
        
        # Enhance button
        if st.button("Restore Image"):
            enhanced_image, buffer = enhance_image(image, scale_value, anime)
            
            # Show images side by side
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original Image", use_column_width=True)
            with col2:
                st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)
            
            # Download button
            st.download_button(
                label="Download Enhanced Image",
                data=buffer,
                file_name="enhanced_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()
