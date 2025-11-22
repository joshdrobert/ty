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
    const severities = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'];
    const probs = [
        0.1 + Math.random() * 0.3,
        0.1 + Math.random() * 0.3,
        0.1 + Math.random() * 0.3,
        0.1 + Math.random() * 0.3,
        0.1 + Math.random() * 0.3
    ];
    const sum = probs.reduce((a, b) => a + b, 0);
    const normalizedProbs = probs.map(p => p / sum);
    
    const maxIndex = normalizedProbs.indexOf(Math.max(...normalizedProbs));
    const predicted = severities[maxIndex];
    const confidence = normalizedProbs[maxIndex];
    
    const severityColors = {
        'No DR': '#28a745',
        'Mild': '#ffc107',
        'Moderate': '#fd7e14',
        'Severe': '#dc3545',
        'Proliferative DR': '#721c24'
    };
    
    document.getElementById('severityLevel').textContent = predicted;
    document.getElementById('severityLevel').style.color = severityColors[predicted];
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const distHtml = severities.map((sev, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${sev}:</span>
                <span>${(normalizedProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${normalizedProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('severityDistribution').innerHTML = distHtml;
    
    const recommendations = [];
    if (predicted === 'No DR' || predicted === 'Mild') {
        recommendations.push('Annual screening recommended');
        recommendations.push('Continue diabetes management');
    } else if (predicted === 'Moderate') {
        recommendations.push('6-month follow-up recommended');
        recommendations.push('Consider ophthalmology referral');
    } else if (predicted === 'Severe') {
        recommendations.push('Immediate ophthalmology referral');
        recommendations.push('Consider treatment options');
    } else {
        recommendations.push('Urgent ophthalmology referral required');
        recommendations.push('Immediate treatment indicated');
    }
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Detect Retinopathy';
});

