document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const alphaPower = parseFloat(document.getElementById('alphaPower').value);
    const betaPower = parseFloat(document.getElementById('betaPower').value);
    const gammaPower = parseFloat(document.getElementById('gammaPower').value);
    const muPower = parseFloat(document.getElementById('muPower').value);
    const channel = document.getElementById('channel').value;
    const movement = document.getElementById('movement').value;
    
    const btn = document.querySelector('.predict-btn');
    const resultsSection = document.getElementById('resultsSection');
    
    btn.disabled = true;
    btn.textContent = 'Processing...';
    resultsSection.classList.remove('show');
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock prediction
    const intents = ['Left Hand', 'Right Hand', 'Left Foot', 'Right Foot', 'Tongue', 'Rest'];
    const probs = [0.15, 0.15, 0.15, 0.15, 0.15, 0.25];
    
    // Adjust based on features
    if (movement === 'left_hand' && channel === 'C3') {
        probs[0] += 0.3; // Left hand movement activates right motor cortex (C3)
    } else if (movement === 'right_hand' && channel === 'C4') {
        probs[1] += 0.3; // Right hand movement activates left motor cortex (C4)
    }
    
    if (betaPower > 20) {
        probs[0] += 0.1; // High beta associated with hand movement
        probs[1] += 0.1;
    }
    
    if (muPower < 5) {
        probs[0] += 0.1; // Mu suppression during movement
        probs[1] += 0.1;
    }
    
    if (alphaPower < 10 && betaPower < 15 && gammaPower < 10) {
        probs[5] += 0.2; // Low power across bands suggests rest
    }
    
    // Normalize
    const sum = probs.reduce((a, b) => a + b, 0);
    const normalizedProbs = probs.map(p => Math.max(0, p / sum));
    
    const maxIndex = normalizedProbs.indexOf(Math.max(...normalizedProbs));
    const predicted = intents[maxIndex];
    const confidence = normalizedProbs[maxIndex];
    
    document.getElementById('predictedIntent').textContent = predicted;
    document.getElementById('confidenceBar').style.width = (confidence * 100) + '%';
    document.getElementById('confidenceValue').textContent = (confidence * 100).toFixed(2) + '%';
    
    const distHtml = intents.map((intent, idx) => `
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>${intent}:</span>
                <span>${(normalizedProbs[idx] * 100).toFixed(2)}%</span>
            </div>
            <div class="probability-bar" style="height: 20px;">
                <div class="probability-fill" style="width: ${normalizedProbs[idx] * 100}%"></div>
            </div>
        </div>
    `).join('');
    
    document.getElementById('intentDistribution').innerHTML = distHtml;
    
    resultsSection.classList.add('show');
    btn.disabled = false;
    btn.textContent = 'Classify Motor Intent';
});

