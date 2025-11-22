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
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock predictions
    const classes = ['Normal', 'Pneumonia', 'COVID-19'];
    const probs = [
        0.2 + Math.random() * 0.3,
        0.2 + Math.random() * 0.3,
        0.2 + Math.random() * 0.3
    ];
    const sum = probs.reduce((a, b) => a + b, 0);
    const normalizedProbs = probs.map(p => p / sum);
    
    const maxIndex = normalizedProbs.indexOf(Math.max(...normalizedProbs));
    const predicted = classes[maxIndex];
    const confidence = normalizedProbs[maxIndex];
    
    document.getElementById('predictedDiagnosis').textContent = predicted;
    document.getElementById('predictedDiagnosis').style.color = predicted === 'Normal' ? '#28a745' : '#dc3545';
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const probHtml = classes.map((cls, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${cls}:</span>
                <span>${(normalizedProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${normalizedProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('probabilities').innerHTML = probHtml;
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify X-Ray';
});

