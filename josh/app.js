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
    const abnormalities = ['Normal', 'Stenosis', 'Regurgitation', 'Prolapse', 'Vegetation'];
    const probs = [
        0.2 + Math.random() * 0.3,
        0.15 + Math.random() * 0.25,
        0.15 + Math.random() * 0.25,
        0.1 + Math.random() * 0.2,
        0.05 + Math.random() * 0.15
    ];
    const sum = probs.reduce((a, b) => a + b, 0);
    const normalizedProbs = probs.map(p => p / sum);
    
    const maxIndex = normalizedProbs.indexOf(Math.max(...normalizedProbs));
    const predicted = abnormalities[maxIndex];
    const confidence = normalizedProbs[maxIndex];
    
    document.getElementById('abnormality').textContent = predicted;
    document.getElementById('abnormality').style.color = predicted === 'Normal' ? '#28a745' : '#dc3545';
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const distHtml = abnormalities.map((abn, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${abn}:</span>
                <span>${(normalizedProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${normalizedProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('abnormalityDistribution').innerHTML = distHtml;
    
    const implications = [];
    if (predicted === 'Normal') {
        implications.push('No intervention needed');
        implications.push('Routine follow-up');
    } else if (predicted === 'Stenosis') {
        implications.push('Consider severity assessment');
        implications.push('Monitor for symptoms');
        implications.push('Consider intervention if severe');
    } else if (predicted === 'Regurgitation') {
        implications.push('Assess severity and etiology');
        implications.push('Monitor left ventricular function');
        implications.push('Consider intervention if symptomatic or progressive');
    } else if (predicted === 'Prolapse') {
        implications.push('Assess for mitral valve prolapse');
        implications.push('Monitor for complications');
    } else {
        implications.push('Urgent evaluation for endocarditis');
        implications.push('Blood cultures and echocardiography');
        implications.push('Consider antibiotic therapy');
    }
    
    document.getElementById('implications').innerHTML = implications.map(i => `<div>• ${i}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Valve Abnormality';
});

