document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const creatinine = parseFloat(document.getElementById('creatinine').value);
    const egfr = parseFloat(document.getElementById('egfr').value);
    const urineOutput = parseFloat(document.getElementById('urineOutput').value);
    const sbp = parseFloat(document.getElementById('sbp').value);
    const heartRate = parseFloat(document.getElementById('heartRate').value);
    const nephrotoxic = document.getElementById('nephrotoxic').value;
    const sepsis = document.getElementById('sepsis').value === 'yes';
    const diabetes = document.getElementById('diabetes').value === 'yes';
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let akiRisk = 0.15;
    const riskFactors = [];
    const recommendations = [];
    
    if (creatinine > 1.5) {
        akiRisk += 0.2;
        riskFactors.push('Elevated serum creatinine');
    }
    
    if (egfr < 60) {
        akiRisk += 0.15;
        riskFactors.push('Reduced eGFR');
    }
    
    if (urineOutput < 0.5) {
        akiRisk += 0.25;
        riskFactors.push('Oliguria (< 0.5 mL/kg/hr)');
        recommendations.push('Urgent fluid management');
    }
    
    if (sbp < 90) {
        akiRisk += 0.2;
        riskFactors.push('Hypotension');
        recommendations.push('Hemodynamic support');
    }
    
    if (sepsis) {
        akiRisk += 0.3;
        riskFactors.push('Sepsis');
        recommendations.push('Sepsis protocol and fluid resuscitation');
    }
    
    if (nephrotoxic === 'multiple') {
        akiRisk += 0.2;
        riskFactors.push('Multiple nephrotoxic medications');
        recommendations.push('Review and discontinue non-essential nephrotoxic medications');
    } else if (nephrotoxic !== 'none') {
        akiRisk += 0.1;
        riskFactors.push('Nephrotoxic medication exposure');
    }
    
    if (diabetes) {
        akiRisk += 0.1;
        riskFactors.push('Diabetes');
    }
    
    akiRisk = Math.min(0.95, akiRisk);
    
    let riskLevel = 'Low';
    if (akiRisk > 0.6) {
        riskLevel = 'High';
        recommendations.push('Frequent monitoring (every 4-6 hours)');
        recommendations.push('Consider nephrology consultation');
    } else if (akiRisk > 0.3) {
        riskLevel = 'Moderate';
        recommendations.push('Close monitoring (every 8-12 hours)');
        recommendations.push('Optimize volume status');
    } else {
        recommendations.push('Standard monitoring');
        recommendations.push('Continue preventive measures');
    }
    
    const riskColors = {
        'Low': '#28a745',
        'Moderate': '#ffc107',
        'High': '#dc3545'
    };
    
    document.getElementById('akiRisk').textContent = riskLevel;
    document.getElementById('akiRisk').style.color = riskColors[riskLevel];
    document.getElementById('riskBar').style.width = (akiRisk * 100) + '%';
    document.getElementById('riskValue').textContent = (akiRisk * 100).toFixed(1) + '%';
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified</div>';
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict AKI Risk';
});

