document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const oct4 = parseFloat(document.getElementById('oct4').value);
    const sox2 = parseFloat(document.getElementById('sox2').value);
    const nanog = parseFloat(document.getElementById('nanog').value);
    const lineage = document.getElementById('lineage').value;
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let potential = 0.6;
    const avgPluripotency = (oct4 + sox2 + nanog) / 3;
    
    if (avgPluripotency > 5) potential += 0.2;
    if (avgPluripotency < 2) potential += 0.15; // Low pluripotency = higher differentiation potential
    if (lineage === 'neural') potential += 0.1;
    
    potential = Math.max(0.2, Math.min(0.95, potential));
    
    const levels = ['Low', 'Moderate', 'High', 'Very High'];
    const levelIndex = Math.floor(potential * 4);
    const level = levels[Math.min(levelIndex, 3)];
    
    document.getElementById('differentiationPotential').textContent = level;
    document.getElementById('confidenceBar').style.width = (potential * 100) + '%';
    document.getElementById('confidenceValue').textContent = (potential * 100).toFixed(2) + '%';
    
    const recommendations = [];
    if (avgPluripotency > 5) recommendations.push('Consider pre-differentiation culture to reduce pluripotency markers');
    if (lineage === 'neural') recommendations.push('Use neural induction medium with retinoic acid');
    if (lineage === 'cardiac') recommendations.push('Apply BMP4 and activin A for cardiac differentiation');
    recommendations.push(`Optimize culture conditions for ${lineage} lineage`);
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Differentiation Potential';
});

