document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const gestationalAge = parseFloat(document.getElementById('gestationalAge').value);
    const birthWeight = parseFloat(document.getElementById('birthWeight').value);
    const maternalFever = document.getElementById('maternalFever').value === 'yes';
    const prom = document.getElementById('prom').value === 'yes';
    const heartRate = parseFloat(document.getElementById('heartRate').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const respiratoryRate = parseFloat(document.getElementById('respiratoryRate').value);
    const wbc = parseFloat(document.getElementById('wbc').value);
    const crp = parseFloat(document.getElementById('crp').value);
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let sepsisRisk = 0.15;
    const riskFactors = [];
    const recommendations = [];
    
    if (gestationalAge < 37) {
        sepsisRisk += 0.15;
        riskFactors.push('Preterm birth (< 37 weeks)');
    }
    
    if (birthWeight < 2500) {
        sepsisRisk += 0.1;
        riskFactors.push('Low birth weight (< 2500g)');
    }
    
    if (maternalFever) {
        sepsisRisk += 0.2;
        riskFactors.push('Maternal fever (> 38°C)');
        recommendations.push('Consider maternal infection workup');
    }
    
    if (prom) {
        sepsisRisk += 0.15;
        riskFactors.push('Prolonged rupture of membranes (> 18 hours)');
    }
    
    if (heartRate > 180 || heartRate < 100) {
        sepsisRisk += 0.1;
        riskFactors.push('Abnormal heart rate');
    }
    
    if (temperature > 38 || temperature < 36) {
        sepsisRisk += 0.15;
        riskFactors.push('Abnormal temperature');
    }
    
    if (respiratoryRate > 60) {
        sepsisRisk += 0.1;
        riskFactors.push('Tachypnea (> 60/min)');
    }
    
    if (wbc < 5 || wbc > 20) {
        sepsisRisk += 0.1;
        riskFactors.push('Abnormal white blood cell count');
    }
    
    if (crp > 10) {
        sepsisRisk += 0.2;
        riskFactors.push('Elevated C-reactive protein');
    }
    
    sepsisRisk = Math.min(0.95, sepsisRisk);
    
    let riskLevel = 'Low';
    if (sepsisRisk > 0.6) {
        riskLevel = 'High';
        recommendations.push('Immediate blood culture and antibiotic initiation');
        recommendations.push('Consider intensive care monitoring');
    } else if (sepsisRisk > 0.3) {
        riskLevel = 'Moderate';
        recommendations.push('Blood culture recommended');
        recommendations.push('Close monitoring');
    } else {
        recommendations.push('Continue routine monitoring');
    }
    
    const riskColors = {
        'Low': '#28a745',
        'Moderate': '#ffc107',
        'High': '#dc3545'
    };
    
    document.getElementById('sepsisRisk').textContent = riskLevel;
    document.getElementById('sepsisRisk').style.color = riskColors[riskLevel];
    document.getElementById('riskBar').style.width = (sepsisRisk * 100) + '%';
    document.getElementById('riskValue').textContent = (sepsisRisk * 100).toFixed(1) + '%';
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified</div>';
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Sepsis Risk';
});

