document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const age = parseFloat(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const mme = parseFloat(document.getElementById('mme').value);
    const numPrescriptions = parseInt(document.getElementById('numPrescriptions').value);
    const benzodiazepine = document.getElementById('benzodiazepine').value === 'yes';
    const sud = document.getElementById('sud').value === 'yes';
    const mentalHealth = document.getElementById('mentalHealth').value === 'yes';
    const chronicPain = document.getElementById('chronicPain').value === 'yes';
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let overdoseRisk = 0.05;
    const riskFactors = [];
    const recommendations = [];
    
    if (mme > 90) {
        overdoseRisk += 0.25;
        riskFactors.push('High daily opioid dose (> 90 MME)');
        recommendations.push('Consider dose reduction');
    } else if (mme > 50) {
        overdoseRisk += 0.15;
        riskFactors.push('Moderate-high daily opioid dose (50-90 MME)');
    }
    
    if (numPrescriptions > 5) {
        overdoseRisk += 0.15;
        riskFactors.push('Multiple opioid prescriptions');
        recommendations.push('Review prescription history and consider consolidation');
    }
    
    if (benzodiazepine) {
        overdoseRisk += 0.3;
        riskFactors.push('Concurrent benzodiazepine use (highly dangerous combination)');
        recommendations.push('URGENT: Avoid concurrent benzodiazepine and opioid use');
    }
    
    if (sud) {
        overdoseRisk += 0.2;
        riskFactors.push('History of substance use disorder');
        recommendations.push('Consider addiction medicine consultation');
        recommendations.push('Consider naloxone prescription');
    }
    
    if (mentalHealth) {
        overdoseRisk += 0.1;
        riskFactors.push('Mental health disorder');
        recommendations.push('Address mental health needs');
    }
    
    if (age > 65) {
        overdoseRisk += 0.1;
        riskFactors.push('Advanced age (increased sensitivity)');
    }
    
    if (gender === 'male' && age < 50) {
        overdoseRisk += 0.05;
    }
    
    overdoseRisk = Math.min(0.95, overdoseRisk);
    
    let riskLevel = 'Low';
    if (overdoseRisk > 0.5) {
        riskLevel = 'High';
        recommendations.push('Prescribe naloxone');
        recommendations.push('Consider alternative pain management');
        recommendations.push('Frequent monitoring and follow-up');
    } else if (overdoseRisk > 0.2) {
        riskLevel = 'Moderate';
        recommendations.push('Consider naloxone prescription');
        recommendations.push('Regular monitoring');
    } else {
        recommendations.push('Continue standard monitoring');
        recommendations.push('Patient education on safe opioid use');
    }
    
    const riskColors = {
        'Low': '#28a745',
        'Moderate': '#ffc107',
        'High': '#dc3545'
    };
    
    document.getElementById('overdoseRisk').textContent = riskLevel;
    document.getElementById('overdoseRisk').style.color = riskColors[riskLevel];
    document.getElementById('riskBar').style.width = (overdoseRisk * 100) + '%';
    document.getElementById('riskValue').textContent = (overdoseRisk * 100).toFixed(1) + '%';
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified</div>';
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Overdose Risk';
});

