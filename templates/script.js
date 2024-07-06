const form = document.getElementById('uploadForm');
const enhanceBtn = document.getElementById('enhanceBtn');
const processingMsg = document.getElementById('processingMsg');

form.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('fileInput');
    const scaleSelect = document.getElementById('scale');
    const file = fileInput.files[0];
    const scale = scaleSelect.value;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('scale', scale);

    processingMsg.style.display = 'block';  // Show processing message

    const response = await fetch('/upscale', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    const resultDiv = document.getElementById('result');
    const originalImage = document.getElementById('original-image');
    const enhancedImage = document.getElementById('enhanced-image');
    const originalInfo = document.getElementById('original-info');
    const enhancedInfo = document.getElementById('enhanced-info');
    const downloadLink = document.getElementById('download-link');

    originalImage.src = data.original_path;
    enhancedImage.src = data.output_path;
    downloadLink.href = data.output_path;
    resultDiv.style.display = 'block';

    originalInfo.textContent = `Resolution: ${data.original_width}x${data.original_height}`;
    enhancedInfo.textContent = `Resolution: ${data.output_width}x${data.output_height}`;

    processingMsg.style.display = 'none';  // Hide processing message

    // Show download link
    downloadLink.style.display = 'block';
});
