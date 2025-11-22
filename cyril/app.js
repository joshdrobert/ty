document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const tumorSize = parseFloat(document.getElementById('tumorSize').value);
    const numTumors = parseInt(document.getElementById('numTumors').value);
    const bclcStage = document.getElementById('bclcStage').value;
    const afp = parseFloat(document.getElementById('afp').value);
    const vascularInvasion = document.getElementById('vascularInvasion').value;
    const geneScore = parseFloat(document.getElementById('geneScore').value);
    const cirrhosis = document.getElementById('cirrhosis').value === 'yes';
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let recurrenceRisk = 0.25;
    const riskFactors = [];
    const recommendations = [];
    
    if (tumorSize > 5) {
        recurrenceRisk += 0.15;
        riskFactors.push('Large tumor size (> 5 cm)');
    }
    
    if (numTumors > 3) {
        recurrenceRisk += 0.2;
        riskFactors.push('Multiple tumors (> 3)');
    }
    
    if (bclcStage === 'C' || bclcStage === 'D') {
        recurrenceRisk += 0.25;
        riskFactors.push('Advanced BCLC stage');
    } else if (bclcStage === 'B') {
        recurrenceRisk += 0.15;
        riskFactors.push('Intermediate BCLC stage');
    }
    
    if (afp > 400) {
        recurrenceRisk += 0.15;
        riskFactors.push('Elevated AFP (> 400 ng/mL)');
    }
    
    if (vascularInvasion === 'macro') {
        recurrenceRisk += 0.3;
        riskFactors.push('Macrovascular invasion');
        recommendations.push('Consider systemic therapy');
    } else if (vascularInvasion === 'micro') {
        recurrenceRisk += 0.15;
        riskFactors.push('Microvascular invasion');
    }
    
    if (geneScore > 7) {
        recurrenceRisk += 0.2;
        riskFactors.push('High gene expression risk score');
    }
    
    if (cirrhosis) {
        recurrenceRisk += 0.1;
        riskFactors.push('Underlying cirrhosis');
    }
    
    recurrenceRisk = Math.min(0.95, recurrenceRisk);
    
    let riskLevel = 'Low';
    if (recurrenceRisk > 0.6) {
        riskLevel = 'High';
        recommendations.push('Intensive surveillance (every 3 months)');
        recommendations.push('Consider adjuvant therapy');
    } else if (recurrenceRisk > 0.4) {
        riskLevel = 'Moderate';
        recommendations.push('Regular surveillance (every 6 months)');
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

