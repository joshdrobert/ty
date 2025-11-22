document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const baselineHR = parseFloat(document.getElementById('baselineHR').value);
    const accelerations = parseFloat(document.getElementById('accelerations').value);
    const fetalMovement = parseFloat(document.getElementById('fetalMovement').value);
    const uterineContractions = parseFloat(document.getElementById('uterineContractions').value);
    const lightDecelerations = parseFloat(document.getElementById('lightDecelerations').value);
    const severeDecelerations = parseFloat(document.getElementById('severeDecelerations').value);
    const prolongedDecelerations = parseFloat(document.getElementById('prolongedDecelerations').value);
    const abnormalSTV = parseFloat(document.getElementById('abnormalSTV').value);
    const meanSTV = parseFloat(document.getElementById('meanSTV').value);
    const abnormalLTV = parseFloat(document.getElementById('abnormalLTV').value);
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let healthStatus = 'Normal';
    let confidence = 0.7;
    const riskFactors = [];
    
    if (baselineHR < 110 || baselineHR > 160) {
        healthStatus = 'Suspicious';
        confidence = 0.6;
        riskFactors.push('Abnormal baseline fetal heart rate');
    }
    
    if (severeDecelerations > 0 || prolongedDecelerations > 0) {
        healthStatus = 'Pathological';
        confidence = 0.8;
        riskFactors.push('Presence of severe or prolonged decelerations');
    }
    
    if (accelerations < 2) {
        riskFactors.push('Reduced accelerations');
        if (healthStatus === 'Normal') {
            healthStatus = 'Suspicious';
            confidence = 0.65;
        }
    }
    
    if (abnormalSTV > 50 || abnormalLTV > 50) {
        riskFactors.push('Abnormal variability patterns');
        if (healthStatus === 'Normal') healthStatus = 'Suspicious';
    }
    
    if (meanSTV < 5) {
        riskFactors.push('Low short-term variability');
    }
    
    const statusColors = {
        'Normal': '#28a745',
        'Suspicious': '#ffc107',
        'Pathological': '#dc3545'
    };
    
    document.getElementById('healthStatus').textContent = healthStatus;
    document.getElementById('healthStatus').style.color = statusColors[healthStatus];
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    document.getElementById('riskAssessment').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified. Fetal monitoring parameters appear normal.</div>';
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Fetal Health';
});

