let selectedImage = null;

document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            selectedImage = event.target.result;
            document.getElementById('previewImage').src = selectedImage;
            document.getElementById('previewSection').style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const stage = document.getElementById('stage').value;
    const grade = document.getElementById('grade').value;
    const tumorSize = parseFloat(document.getElementById('tumorSize').value);
    const numTumors = parseInt(document.getElementById('numTumors').value);
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let recurrenceRisk = 0.3;
    const riskFactors = [];
    const recommendations = [];
    
    if (stage === 'T2' || stage === 'T3' || stage === 'T4') {
        recurrenceRisk += 0.25;
        riskFactors.push('Muscle-invasive or advanced stage');
    } else if (stage === 'T1') {
        recurrenceRisk += 0.15;
        riskFactors.push('T1 stage (invades subepithelial tissue)');
    }
    
    if (grade === 'high') {
        recurrenceRisk += 0.2;
        riskFactors.push('High grade tumor');
    }
    
    if (tumorSize > 3) {
        recurrenceRisk += 0.15;
        riskFactors.push('Large tumor size (> 3 cm)');
    }
    
    if (numTumors > 3) {
        recurrenceRisk += 0.2;
        riskFactors.push('Multiple tumors (> 3)');
    }
    
    recurrenceRisk = Math.min(0.95, recurrenceRisk);
    
    let riskLevel = 'Low';
    if (recurrenceRisk > 0.6) {
        riskLevel = 'High';
        recommendations.push('Intensive surveillance (every 3 months)');
        recommendations.push('Consider intravesical therapy');
    } else if (recurrenceRisk > 0.4) {
        riskLevel = 'Moderate';
        recommendations.push('Regular surveillance (every 6 months)');
        recommendations.push('Consider BCG therapy for high-grade Ta/T1');
    } else {
        recommendations.push('Standard surveillance (every 6-12 months)');
    }
    
    const riskColors = {
        'Low': '#28a745',
        'Moderate': '#ffc107',
        'High': '#dc3545'
    };
    
    document.getElementById('recurrenceRisk').textContent = riskLevel;
    document.getElementById('recurrenceRisk').style.color = riskColors[riskLevel];
    document.getElementById('riskBar').style.width = (recurrenceRisk * 100) + '%';
    document.getElementById('riskValue').textContent = (recurrenceRisk * 100).toFixed(1) + '%';
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors beyond baseline</div>';
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Recurrence Risk';
});

