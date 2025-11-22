document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const meanAmplitude = parseFloat(document.getElementById('meanAmplitude').value);
    const frequency = parseFloat(document.getElementById('frequency').value);
    const muapDuration = parseFloat(document.getElementById('muapDuration').value);
    const polyphasia = parseFloat(document.getElementById('polyphasia').value);
    const fibrillation = document.getElementById('fibrillation').value;
    const muscleGroup = document.getElementById('muscleGroup').value;
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    const disorders = ['Normal', 'Myopathy', 'Neuropathy', 'Motor Neuron Disease', 'Myasthenia Gravis'];
    const probs = [0.2, 0.2, 0.2, 0.2, 0.2];
    
    // Adjust probabilities based on features
    if (fibrillation !== 'none') {
        probs[2] += 0.3; // Neuropathy
        probs[3] += 0.2; // Motor Neuron Disease
        probs[0] -= 0.2; // Normal
    }
    
    if (polyphasia > 30) {
        probs[1] += 0.2; // Myopathy
        probs[2] += 0.1; // Neuropathy
    }
    
    if (muapDuration > 15) {
        probs[1] += 0.15; // Myopathy
    }
    
    if (meanAmplitude < 200) {
        probs[4] += 0.2; // Myasthenia Gravis
    }
    
    // Normalize
    const sum = probs.reduce((a, b) => a + b, 0);
    const normalizedProbs = probs.map(p => Math.max(0, p / sum));
    const renormalizedSum = normalizedProbs.reduce((a, b) => a + b, 0);
    const finalProbs = normalizedProbs.map(p => p / renormalizedSum);
    
    const maxIndex = finalProbs.indexOf(Math.max(...finalProbs));
    const predicted = disorders[maxIndex];
    const confidence = finalProbs[maxIndex];
    
    document.getElementById('predictedDisorder').textContent = predicted;
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const probHtml = disorders.map((dis, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${dis}:</span>
                <span>${(finalProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${finalProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('probabilities').innerHTML = probHtml;
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Disorder';
});

