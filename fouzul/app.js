document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const abi = parseFloat(document.getElementById('abi').value);
    const age = parseFloat(document.getElementById('age').value);
    const diabetes = document.getElementById('diabetes').value === 'yes';
    const smoking = document.getElementById('smoking').value;
    const hypertension = document.getElementById('hypertension').value === 'yes';
    const cad = document.getElementById('cad').value === 'yes';
    const ckd = document.getElementById('ckd').value === 'yes';
    const rutherford = parseInt(document.getElementById('rutherford').value);
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let severity = 'Mild';
    let amputationRisk = 0.05;
    const riskFactors = [];
    const recommendations = [];
    
    if (abi < 0.4) {
        severity = 'Critical';
        amputationRisk = 0.35;
        riskFactors.push('Severely reduced ABI (< 0.4)');
        recommendations.push('Urgent vascular surgery consultation');
        recommendations.push('Consider revascularization');
    } else if (abi < 0.7) {
        severity = 'Moderate to Severe';
        amputationRisk = 0.15;
        riskFactors.push('Moderately reduced ABI (0.4-0.7)');
        recommendations.push('Vascular surgery referral');
        recommendations.push('Aggressive risk factor modification');
    } else if (abi < 0.9) {
        severity = 'Mild to Moderate';
        amputationRisk = 0.08;
        riskFactors.push('Mildly reduced ABI (0.7-0.9)');
        recommendations.push('Medical management');
        recommendations.push('Lifestyle modifications');
    } else {
        severity = 'Mild';
        amputationRisk = 0.02;
        recommendations.push('Conservative management');
        recommendations.push('Regular monitoring');
    }
    
    if (diabetes) {
        amputationRisk += 0.1;
        riskFactors.push('Diabetes significantly increases amputation risk');
        recommendations.push('Tight glycemic control essential');
    }
    
    if (smoking === 'current') {
        amputationRisk += 0.08;
        riskFactors.push('Current smoking increases risk');
        recommendations.push('Smoking cessation counseling');
    }
    
    if (rutherford >= 4) {
        amputationRisk += 0.2;
        severity = 'Critical';
        riskFactors.push('Advanced Rutherford classification');
        recommendations.push('Immediate intervention required');
    }
    
    if (ckd) {
        amputationRisk += 0.05;
        riskFactors.push('Chronic kidney disease');
    }
    
    amputationRisk = Math.min(0.6, amputationRisk);
    
    const severityColors = {
        'Mild': '#28a745',
        'Mild to Moderate': '#ffc107',
        'Moderate to Severe': '#fd7e14',
        'Critical': '#dc3545'
    };
    
    document.getElementById('severity').textContent = severity;
    document.getElementById('severity').style.color = severityColors[severity] || '#333';
    document.getElementById('amputationBar').style.width = (amputationRisk * 100) + '%';
    document.getElementById('amputationValue').textContent = (amputationRisk * 100).toFixed(1) + '%';
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors beyond baseline</div>';
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict PAD Severity & Amputation Risk';
});

