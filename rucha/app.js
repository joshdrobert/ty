let selectedImage = null;

document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            selectedImage = event.target.result;
            document.getElementById('previewImage').src = selectedImage;
            document.getElementById('previewSection').style.display = 'block';
            document.getElementById('predictBtn').disabled = false;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('predictBtn').addEventListener('click', async function() {
    if (!selectedImage) return;
    
    const btn = document.getElementById('predictBtn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    // Simulate model inference
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction results
    const isMalignant = Math.random() > 0.5;
    const confidence = 0.75 + Math.random() * 0.2;
    const malignantProb = isMalignant ? confidence : 1 - confidence;
    const benignProb = 1 - malignantProb;
    
    document.getElementById('predictedClass').textContent = isMalignant ? 'Malignant' : 'Benign';
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const probHtml = `
        <div style="margin-top: 10px;">
            <div>Malignant: ${(malignantProb * 100).toFixed(2)}%</div>
            <div>Benign: ${(benignProb * 100).toFixed(2)}%</div>
        </div>
    `;
    document.getElementById('probabilities').innerHTML = probHtml;
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Skin Lesion';
    
    // In production, this would use TensorFlow.js to load and run the actual model:
    // const model = await tf.loadLayersModel('model/model.json');
    // const img = tf.browser.fromPixels(preprocessedImage);
    // const prediction = model.predict(img);
});

