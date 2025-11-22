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
    const timeFromOnset = parseFloat(document.getElementById('timeFromOnset').value) || 0;
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock predictions
    const strokeTypes = ['Ischemic', 'Hemorrhagic', 'No Stroke'];
    let probs = [
        0.3 + Math.random() * 0.4,
        0.2 + Math.random() * 0.3,
        0.1 + Math.random() * 0.2
    ];
    
    // Adjust based on time from onset (early CT may not show ischemic changes)
    if (timeFromOnset < 3) {
        probs[0] += 0.1; // Ischemic may be less visible early
    }
    
    const sum = probs.reduce((a, b) => a + b, 0);
    const normalizedProbs = probs.map(p => p / sum);
    
    const maxIndex = normalizedProbs.indexOf(Math.max(...normalizedProbs));
    const predicted = strokeTypes[maxIndex];
    const confidence = normalizedProbs[maxIndex];
    
    const typeColors = {
        'Ischemic': '#2196F3',
        'Hemorrhagic': '#dc3545',
        'No Stroke': '#28a745'
    };
    
    document.getElementById('strokeType').textContent = predicted;
    document.getElementById('strokeType').style.color = typeColors[predicted];
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const probHtml = strokeTypes.map((type, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${type}:</span>
                <span>${(normalizedProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${normalizedProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('probabilities').innerHTML = probHtml;
    
    const implications = [];
    if (predicted === 'Ischemic') {
        implications.push('Consider thrombolytic therapy if within time window');
        implications.push('Antiplatelet therapy indicated');
        implications.push('Consider endovascular thrombectomy');
    } else if (predicted === 'Hemorrhagic') {
        implications.push('Avoid anticoagulation and antiplatelet agents');
        implications.push('Blood pressure management critical');
        implications.push('Consider neurosurgical consultation');
    } else {
        implications.push('Continue diagnostic workup');
        implications.push('Consider alternative diagnoses');
    }
    
    document.getElementById('implications').innerHTML = implications.map(i => `<div>• ${i}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Stroke Type';
});

