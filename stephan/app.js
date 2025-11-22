document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const heartRate = parseFloat(document.getElementById('heartRate').value);
    const hrv = parseFloat(document.getElementById('hrv').value);
    const skinConductance = parseFloat(document.getElementById('skinConductance').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const motionIntensity = parseFloat(document.getElementById('motionIntensity').value);
    const duration = parseFloat(document.getElementById('duration').value);
    const history = document.getElementById('history').value;
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let severityProb = 0.3;
    const riskFactors = [];
    const recommendations = [];
    
    if (motionIntensity > 3) {
        severityProb += 0.2;
        riskFactors.push('High motion intensity');
    }
    
    if (duration > 60) {
        severityProb += 0.15;
        riskFactors.push('Prolonged exposure');
    }
    
    if (history === 'severe') {
        severityProb += 0.25;
        riskFactors.push('History of severe motion sickness');
    } else if (history === 'moderate') {
        severityProb += 0.15;
        riskFactors.push('History of moderate motion sickness');
    }
    
    if (skinConductance > 20) {
        severityProb += 0.1;
        riskFactors.push('Elevated skin conductance (stress response)');
    }
    
    if (hrv < 40) {
        severityProb += 0.1;
        riskFactors.push('Reduced heart rate variability');
    }
    
    if (heartRate > 100) {
        severityProb += 0.1;
        riskFactors.push('Elevated heart rate');
    }
    
    severityProb = Math.min(0.95, severityProb);
    
    let severity = 'Mild';
    if (severityProb > 0.7) {
        severity = 'Severe';
        recommendations.push('Consider antiemetic medication');
        recommendations.push('Reduce motion exposure if possible');
        recommendations.push('Focus on horizon or fixed point');
    } else if (severityProb > 0.5) {
        severity = 'Moderate';
        recommendations.push('Consider preventive measures');
        recommendations.push('Take breaks from motion');
        recommendations.push('Stay hydrated');
    } else {
        recommendations.push('Monitor symptoms');
        recommendations.push('Standard preventive measures');
    }
    
    const severityColors = {
        'Mild': '#28a745',
        'Moderate': '#ffc107',
        'Severe': '#dc3545'
    };
    
    document.getElementById('severity').textContent = severity;
    document.getElementById('severity').style.color = severityColors[severity];
    document.getElementById('severityBar').style.width = (severityProb * 100) + '%';
    document.getElementById('severityValue').textContent = (severityProb * 100).toFixed(1) + '%';
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified</div>';
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Motion Sickness Severity';
});

