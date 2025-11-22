let samples = [];
let selectedSampleId = null;

// Load samples on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSamples();
    
    document.getElementById('loadSamplesBtn').addEventListener('click', loadSamples);
    document.getElementById('randomBtn').addEventListener('click', selectRandom);
    document.getElementById('classFilter').addEventListener('change', filterSamples);
    document.getElementById('predictBtn').addEventListener('click', predictSelected);
    document.getElementById('bulkPredictBtn').addEventListener('click', bulkPredict);
});

async function loadSamples() {
    try {
        const response = await fetch('/api/samples');
        const data = await response.json();
        samples = data.samples;
        displaySamples();
    } catch (error) {
        console.error('Error loading samples:', error);
        alert('Error loading samples. Using mock data.');
        // Use mock data
        samples = Array.from({length: 20}, (_, i) => ({
            id: `sample_${i}`,
            path: `test/${i % 2 === 0 ? 'benign' : 'malignant'}/img_${i}.jpg`,
            label: i % 2 === 0 ? 'Benign' : 'Malignant'
        }));
        displaySamples();
    }
}

function displaySamples() {
    const filter = document.getElementById('classFilter').value;
    const filteredSamples = filter === 'all' 
        ? samples 
        : samples.filter(s => s.label === filter);
    
    const grid = document.getElementById('samplesList');
    grid.innerHTML = '';
    
    filteredSamples.forEach(sample => {
        const item = document.createElement('div');
        item.className = `sample-item ${selectedSampleId === sample.id ? 'selected' : ''}`;
        item.innerHTML = `
            <div class="sample-id">${sample.id}</div>
            <div class="sample-label">${sample.label}</div>
        `;
        item.addEventListener('click', () => selectSample(sample.id));
        grid.appendChild(item);
    });
    
    updateButtons();
}

function filterSamples() {
    displaySamples();
}

function selectSample(sampleId) {
    selectedSampleId = sampleId;
    displaySamples();
    updateButtons();
}

function selectRandom() {
    if (samples.length === 0) return;
    const randomIndex = Math.floor(Math.random() * samples.length);
    selectSample(samples[randomIndex].id);
}

function updateButtons() {
    document.getElementById('predictBtn').disabled = selectedSampleId === null;
    document.getElementById('bulkPredictBtn').disabled = samples.length === 0;
}

async function predictSelected() {
    if (!selectedSampleId) return;
    
    const btn = document.getElementById('predictBtn');
    btn.disabled = true;
    btn.textContent = 'Predicting...';
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({sample_id: selectedSampleId})
        });
        
        const result = await response.json();
        displayPrediction(result);
    } catch (error) {
        console.error('Error predicting:', error);
        alert('Error making prediction');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Predict Selected';
    }
}

function displayPrediction(result) {
    document.getElementById('predictionSection').style.display = 'block';
    document.getElementById('trueLabel').textContent = result.true_label;
    document.getElementById('predictedLabel').textContent = result.predicted_label;
    document.getElementById('predictedLabel').style.color = result.correct ? '#28a745' : '#dc3545';
    document.getElementById('confidence').textContent = (result.confidence * 100).toFixed(2) + '%';
    
    // Display probabilities
    const probDiv = document.getElementById('probabilities');
    probDiv.innerHTML = '';
    
    Object.entries(result.probabilities).forEach(([label, prob]) => {
        const item = document.createElement('div');
        item.className = 'probability-item';
        item.innerHTML = `
            <span>${label}:</span>
            <div class="probability-bar">
                <div class="probability-fill" style="width: ${prob * 100}%">${(prob * 100).toFixed(1)}%</div>
            </div>
        `;
        probDiv.appendChild(item);
    });
}

async function bulkPredict() {
    const btn = document.getElementById('bulkPredictBtn');
    btn.disabled = true;
    btn.textContent = 'Analyzing...';
    
    try {
        const response = await fetch('/api/bulk_predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({sample_ids: samples.map(s => s.id)})
        });
        
        const result = await response.json();
        displayBulkAnalysis(result);
    } catch (error) {
        console.error('Error in bulk prediction:', error);
        alert('Error performing bulk analysis');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Bulk Analysis (All Samples)';
    }
}

function displayBulkAnalysis(result) {
    document.getElementById('bulkAnalysis').style.display = 'block';
    document.getElementById('totalSamples').textContent = result.total;
    document.getElementById('correctSamples').textContent = result.correct;
    document.getElementById('overallAccuracy').textContent = (result.accuracy * 100).toFixed(2) + '%';
    
    // Display per-class metrics
    const classMetricsDiv = document.getElementById('classMetrics');
    classMetricsDiv.innerHTML = '<h3>Per-Class Performance</h3>';
    
    Object.entries(result.class_metrics).forEach(([className, metrics]) => {
        const metricDiv = document.createElement('div');
        metricDiv.className = 'metric';
        metricDiv.innerHTML = `
            <span class="metric-label">${className}:</span>
            <span class="metric-value">${metrics.total > 0 ? (metrics.accuracy * 100).toFixed(2) + '%' : 'N/A'}</span>
            <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                ${metrics.correct}/${metrics.total} correct
            </div>
        `;
        classMetricsDiv.appendChild(metricDiv);
    });
}

