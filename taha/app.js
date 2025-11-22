let selectedImage = null;

document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            selectedImage = event.target.result;
            document.getElementById('previewImage').src = selectedImage;
            document.getElementById('previewSection').style.display = 'block';
            document.getElementById('predictBtn').disabled = false;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('predictBtn').addEventListener('click', async function() {
    if (!selectedImage) return;
    
    const btn = document.getElementById('predictBtn');
    const resultsSection = document.getElementById('resultsSection');
    const calciumScore = parseFloat(document.getElementById('calciumScore').value) || 0;
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock predictions
    const hasCAD = Math.random() > 0.3;
    let cadProb = hasCAD ? 0.6 + Math.random() * 0.3 : 0.1 + Math.random() * 0.2;
    
    // Adjust based on calcium score
    if (calciumScore > 400) {
        cadProb = Math.min(0.95, cadProb + 0.2);
    } else if (calciumScore > 100) {
        cadProb = Math.min(0.95, cadProb + 0.1);
    }
    
    const severities = ['No CAD', 'Mild', 'Moderate', 'Severe'];
    let severity = 'No CAD';
    if (cadProb > 0.7) {
        severity = 'Severe';
    } else if (cadProb > 0.5) {
        severity = 'Moderate';
    } else if (cadProb > 0.3) {
        severity = 'Mild';
    }
    
    const vessels = ['LAD', 'LCx', 'RCA'];
    const vesselProbs = vessels.map(() => Math.random() * 0.6);
    const maxVesselIdx = vesselProbs.indexOf(Math.max(...vesselProbs));
    
    document.getElementById('cadPresence').textContent = hasCAD ? 'Yes' : 'No';
    document.getElementById('cadPresence').style.color = hasCAD ? '#dc3545' : '#28a745';
    document.getElementById('severity').textContent = severity;
    document.getElementById('severity').style.color = severity === 'No CAD' ? '#28a745' : severity === 'Severe' ? '#dc3545' : '#ffc107';
    document.getElementById('confidenceBar').style.width = (cadProb * 100) + '%';
    document.getElementById('confidenceValue').textContent = (cadProb * 100).toFixed(2) + '%';
    
    const vesselHtml = vessels.map((vessel, idx) => `
        <div style="margin: 5px 0;">
            <span>${vessel}:</span>
            <span>${(vesselProbs[idx] * 100).toFixed(1)}% stenosis</span>
        </div>
    `).join('');
    
    document.getElementById('vesselInvolvement').innerHTML = vesselHtml;
    
    const recommendations = [];
    if (severity === 'Severe') {
        recommendations.push('Urgent cardiology consultation');
        recommendations.push('Consider invasive angiography');
        recommendations.push('Optimize medical therapy');
        recommendations.push('Consider revascularization');
    } else if (severity === 'Moderate') {
        recommendations.push('Cardiology consultation');
        recommendations.push('Optimize medical therapy (statin, antiplatelet)');
        recommendations.push('Lifestyle modifications');
        recommendations.push('Consider stress testing');
    } else if (severity === 'Mild') {
        recommendations.push('Medical therapy optimization');
        recommendations.push('Lifestyle modifications');
        recommendations.push('Regular follow-up');
    } else {
        recommendations.push('Continue preventive measures');
        recommendations.push('Lifestyle modifications');
    }
    
    document.getElementById('recommendations').innerHTML = recommendations.map(r => `<div>• ${r}</div>`).join('');
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Predict CAD';
});

