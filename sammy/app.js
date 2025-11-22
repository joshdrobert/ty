document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const age = parseFloat(document.getElementById('age').value);
    const vesselDiameter = parseFloat(document.getElementById('vesselDiameter').value);
    const lesionLength = parseFloat(document.getElementById('lesionLength').value);
    const deviceType = document.getElementById('deviceType').value;
    const comorbidityScore = parseFloat(document.getElementById('comorbidityScore').value);
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction based on inputs
    let successProb = 0.7;
    if (vesselDiameter > 5 && vesselDiameter < 8) successProb += 0.1;
    if (lesionLength < 20) successProb += 0.1;
    if (deviceType === 'stent') successProb += 0.05;
    if (comorbidityScore < 3) successProb += 0.05;
    if (age > 70) successProb -= 0.1;
    if (lesionLength > 50) successProb -= 0.15;
    
    successProb = Math.max(0.1, Math.min(0.95, successProb));
    const isSuccess = successProb > 0.6;
    
    document.getElementById('predictedOutcome').textContent = isSuccess ? 'Success' : 'Failure';
    document.getElementById('predictedOutcome').style.color = isSuccess ? '#28a745' : '#dc3545';
    document.getElementById('successBar').style.width = (successProb * 100) + '%';
    document.getElementById('successValue').textContent = (successProb * 100).toFixed(2) + '%';
    
    const riskFactors = [];
    if (age > 75) riskFactors.push('Advanced age');
    if (lesionLength > 40) riskFactors.push('Long lesion length');
    if (comorbidityScore > 5) riskFactors.push('High comorbidity burden');
    if (vesselDiameter < 3) riskFactors.push('Small vessel diameter');
    
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified</div>';
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Procedure Success';
});

