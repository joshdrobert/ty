document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const particleSize = parseFloat(document.getElementById('particleSize').value);
    const surfaceCharge = parseFloat(document.getElementById('surfaceCharge').value);
    const hydrophobicity = parseFloat(document.getElementById('hydrophobicity').value);
    const molecularWeight = parseFloat(document.getElementById('molecularWeight').value);
    const cellLine = document.getElementById('cellLine').value;
    const targeting = document.getElementById('targeting').value;
    const drugLoading = parseFloat(document.getElementById('drugLoading').value);
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let efficiency = 0.5;
    const recommendations = [];
    
    // Optimal particle size is typically 50-200 nm
    if (particleSize >= 50 && particleSize <= 200) {
        efficiency += 0.15;
    } else if (particleSize < 50) {
        efficiency -= 0.1;
        recommendations.push('Consider increasing particle size (optimal: 50-200 nm)');
    } else {
        efficiency -= 0.15;
        recommendations.push('Consider reducing particle size (optimal: 50-200 nm)');
    }
    
    // Slightly negative charge is often optimal
    if (surfaceCharge >= -20 && surfaceCharge <= 10) {
        efficiency += 0.1;
    } else if (surfaceCharge < -30) {
        efficiency -= 0.1;
        recommendations.push('Consider reducing negative charge');
    }
    
    // Moderate hydrophobicity is often best
    if (hydrophobicity >= 3 && hydrophobicity <= 7) {
        efficiency += 0.1;
    } else {
        recommendations.push('Optimize hydrophobicity for better cell uptake');
    }
    
    // Targeting ligands improve efficiency
    if (targeting !== 'none') {
        efficiency += 0.2;
    } else {
        recommendations.push('Consider adding targeting ligand for improved specificity');
    }
    
    // Higher drug loading is better
    if (drugLoading > 10) {
        efficiency += 0.1;
    } else {
        recommendations.push('Consider increasing drug loading capacity');
    }
    
    // Cancer cell lines often show better uptake
    if (cellLine === 'cancer') {
        efficiency += 0.05;
    }
    
    efficiency = Math.max(0.1, Math.min(0.95, efficiency));
    
    let efficiencyLevel = 'Moderate';
    if (efficiency > 0.7) {
        efficiencyLevel = 'High';
    } else if (efficiency < 0.4) {
        efficiencyLevel = 'Low';
    }
    
    const efficiencyColors = {
        'Low': '#dc3545',
        'Moderate': '#ffc107',
        'High': '#28a745'
    };
    
    document.getElementById('efficiency').textContent = efficiencyLevel;
    document.getElementById('efficiency').style.color = efficiencyColors[efficiencyLevel];
    document.getElementById('efficiencyBar').style.width = (efficiency * 100) + '%';
    document.getElementById('efficiencyValue').textContent = (efficiency * 100).toFixed(1) + '%';
    
    if (recommendations.length === 0) {
        recommendations.push('Current parameters appear optimal');
    }
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Delivery Efficiency';
});

