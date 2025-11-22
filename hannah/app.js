document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const drugName = document.getElementById('drugName').value;
    const cyp2c9 = document.getElementById('cyp2c9').value;
    const vkorc1 = document.getElementById('vkorc1').value;
    const age = parseFloat(document.getElementById('age').value);
    const weight = parseFloat(document.getElementById('weight').value);
    const medications = document.getElementById('medications').value.toLowerCase();
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    let response = 'Normal';
    let doseAdjustment = 'Standard dosing recommended';
    const riskFactors = [];
    
    if (cyp2c9.includes('*2') || cyp2c9.includes('*3')) {
        response = 'Reduced Metabolism';
        doseAdjustment = 'Reduce dose by 30-50%';
        riskFactors.push('CYP2C9 variant associated with reduced metabolism');
    }
    
    if (vkorc1 === 'AA') {
        response = 'Enhanced Sensitivity';
        doseAdjustment = 'Reduce dose by 50%';
        riskFactors.push('VKORC1 AA genotype increases sensitivity');
    }
    
    if (age > 75) {
        riskFactors.push('Advanced age may require dose reduction');
    }
    
    if (medications.includes('amiodarone') || medications.includes('fluconazole')) {
        riskFactors.push('Concomitant medications may inhibit metabolism');
        doseAdjustment = 'Consider additional 20-30% dose reduction';
    }
    
    if (weight < 60) {
        riskFactors.push('Low body weight may require dose adjustment');
    }
    
    document.getElementById('predictedResponse').textContent = response;
    document.getElementById('doseAdjustment').textContent = doseAdjustment;
    document.getElementById('riskFactors').innerHTML = riskFactors.length > 0 
        ? riskFactors.map(f => `<div>• ${f}</div>`).join('')
        : '<div>No significant risk factors identified</div>';
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict Drug Response';
});

