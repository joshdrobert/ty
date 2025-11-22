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
    const stages = ['No Dementia', 'Very Mild Dementia', 'Mild Dementia', 'Moderate Dementia', 'Severe Dementia'];
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
    const predicted = stages[maxIndex];
    const confidence = normalizedProbs[maxIndex];
    
    const stageColors = {
        'No Dementia': '#28a745',
        'Very Mild Dementia': '#ffc107',
        'Mild Dementia': '#fd7e14',
        'Moderate Dementia': '#dc3545',
        'Severe Dementia': '#721c24'
    };
    
    document.getElementById('diseaseStage').textContent = predicted;
    document.getElementById('diseaseStage').style.color = stageColors[predicted];
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const distHtml = stages.map((stage, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${stage}:</span>
                <span>${(normalizedProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${normalizedProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('stageDistribution').innerHTML = distHtml;
    
    const recommendations = [];
    if (predicted === 'No Dementia' || predicted === 'Very Mild Dementia') {
        recommendations.push('Continue cognitive monitoring');
        recommendations.push('Lifestyle modifications (exercise, diet)');
    } else if (predicted === 'Mild Dementia') {
        recommendations.push('Consider cholinesterase inhibitors');
        recommendations.push('Cognitive rehabilitation');
        recommendations.push('Regular follow-up');
    } else if (predicted === 'Moderate Dementia') {
        recommendations.push('Cholinesterase inhibitors and memantine');
        recommendations.push('Support services and caregiver education');
        recommendations.push('Safety assessment');
    } else {
        recommendations.push('Palliative care considerations');
        recommendations.push('Focus on quality of life');
        recommendations.push('Advanced care planning');
    }
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Disease Stage';
});

