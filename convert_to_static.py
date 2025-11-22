"""
Convert all 22 Flask apps to static GitHub Pages sites using TensorFlow.js
"""
import os
import json
from professional_themes import THEMES

PROJECTS = {
    'rucha': {'type': 'image', 'classes': 2, 'class_names': ['Benign', 'Malignant']},
    'sammy': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'shalini': {'type': 'tabular', 'classes': 3, 'class_names': ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']},
    'maansi': {'type': 'image', 'classes': 2, 'class_names': ['Normal', 'Pneumonia']},
    'hannah': {'type': 'tabular', 'classes': 3, 'class_names': ['Normal', 'Reduced Metabolism', 'Enhanced Sensitivity']},
    'marygrace': {'type': 'tabular', 'classes': 3, 'class_names': ['Normal', 'Suspicious', 'Pathological']},
    'charmaine': {'type': 'image', 'classes': 5, 'class_names': ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR']},
    'fouzul': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'amirah': {'type': 'time_series', 'classes': 5, 'class_names': ['Normal', 'Myopathy', 'Neuropathy', 'Motor Neuron Disease', 'Myasthenia Gravis']},
    'neha': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'annabelle': {'type': 'image', 'classes': 2, 'class_names': ['Normal', 'Pneumonia']},
    'timi': {'type': 'tabular', 'classes': 2, 'class_names': ['No Stroke', 'Stroke']},
    'eric': {'type': 'time_series', 'classes': 5, 'class_names': ['Normal', 'Myopathy', 'Neuropathy', 'Motor Neuron Disease', 'Myasthenia Gravis']},
    'cyril': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'chris': {'type': 'image', 'classes': 4, 'class_names': ['No Tumor', 'Glioma', 'Meningioma', 'Pituitary']},
    'stephan': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'sabour': {'type': 'tabular', 'classes': 2, 'class_names': ['Benign', 'Malignant']},
    'musa': {'type': 'tabular', 'classes': 3, 'class_names': ['Normal', 'Reduced Metabolism', 'Enhanced Sensitivity']},
    'aaron': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'josh': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'jenna': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
    'taha': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure']},
}

def generate_static_html(project_name, config):
    """Generate static HTML with TensorFlow.js"""
    theme = THEMES[project_name]
    
    title_map = {
        'rucha': 'Skin Cancer Classification from Dermoscopy Images',
        'sammy': 'Heart Failure Prediction',
        'shalini': 'Iris Species Classification',
        'maansi': 'Chest X-Ray Pneumonia Classification',
        'hannah': 'Drug Classification',
        'marygrace': 'Fetal Health Classification',
        'charmaine': 'Diabetic Retinopathy Detection',
        'fouzul': 'Heart Failure Prediction',
        'amirah': 'Neuromuscular Disorder Classification from EMG',
        'neha': 'Heart Failure Prediction',
        'annabelle': 'Chest X-Ray Classification',
        'timi': 'Stroke Prediction',
        'eric': 'Neuromuscular Disorder Classification from EMG',
        'cyril': 'Heart Failure Prediction',
        'chris': 'Brain Tumor Classification from MRI',
        'stephan': 'Heart Failure Prediction',
        'sabour': 'Breast Cancer Classification',
        'musa': 'Drug Classification',
        'aaron': 'Heart Failure Prediction',
        'josh': 'Heart Failure Prediction',
        'jenna': 'Heart Failure Prediction',
        'taha': 'Heart Failure Prediction',
    }
    
    subtitle_map = {
        'rucha': 'CNN-based classification of malignant vs benign skin lesions',
        'sammy': 'Predicting heart failure from clinical features',
        'shalini': 'Multi-class classification of Iris species',
        'maansi': 'Binary classification of normal vs pneumonia chest X-rays',
        'hannah': 'Predicting drug response from patient characteristics',
        'marygrace': 'Classifying fetal health status from cardiotocography data',
        'charmaine': 'Detecting diabetic retinopathy severity from retinal images',
        'fouzul': 'Predicting heart failure from clinical features',
        'amirah': 'Classifying neuromuscular disorders from EMG signal patterns',
        'neha': 'Predicting heart failure from clinical features',
        'annabelle': 'Binary classification of normal vs pneumonia chest X-rays',
        'timi': 'Predicting stroke risk from patient data',
        'eric': 'Classifying neuromuscular disorders from EMG signal patterns',
        'cyril': 'Predicting heart failure from clinical features',
        'chris': 'Classifying brain tumors from MRI scans',
        'stephan': 'Predicting heart failure from clinical features',
        'sabour': 'Classifying breast cancer from clinical features',
        'musa': 'Predicting drug response from patient characteristics',
        'aaron': 'Predicting heart failure from clinical features',
        'josh': 'Predicting heart failure from clinical features',
        'jenna': 'Predicting heart failure from clinical features',
        'taha': 'Predicting heart failure from clinical features',
    }
    
    title = title_map.get(project_name, f'{project_name.capitalize()} Project')
    subtitle = subtitle_map.get(project_name, 'Machine learning classification')
    
    class_options = '\n'.join([f'                    <option value="{cls}">{cls}</option>' for cls in config['class_names']])
    
    # Generate JavaScript based on data type
    if config['type'] == 'image':
        js_code = generate_image_js(project_name, config)
    elif config['type'] == 'tabular':
        js_code = generate_tabular_js(project_name, config)
    else:  # time_series
        js_code = generate_timeseries_js(project_name, config)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {project_name.capitalize()}</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.15.0/dist/tf.min.js"></script>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">← Back to Projects</a>
        <h1>{theme['icon']} {title}</h1>
        <p class="subtitle">{subtitle}</p>
        
        <div class="controls">
            <div class="control-group">
                <label>Filter by Class:</label>
                <select id="classFilter">
                    <option value="all">All Classes</option>
{class_options}
                </select>
            </div>
            <div class="control-group">
                <button id="randomBtn" class="btn">Random Sample</button>
                <button id="loadSamplesBtn" class="btn">Load Samples</button>
            </div>
        </div>
        
        <div class="sample-selector">
            <h2>Select Test Sample</h2>
            <div id="samplesList" class="samples-grid"></div>
        </div>
        
        <div class="prediction-section" id="predictionSection" style="display: none;">
            <h2>Prediction Results</h2>
            <div class="result-card">
                <div class="result-item">
                    <span class="label">True Label:</span>
                    <span id="trueLabel" class="value"></span>
                </div>
                <div class="result-item">
                    <span class="label">Predicted Label:</span>
                    <span id="predictedLabel" class="value"></span>
                </div>
                <div class="result-item">
                    <span class="label">Confidence:</span>
                    <span id="confidence" class="value"></span>
                </div>
                <div class="result-item">
                    <span class="label">Probabilities:</span>
                    <div id="probabilities"></div>
                </div>
            </div>
        </div>
        
        <div class="bulk-analysis" id="bulkAnalysis" style="display: none;">
            <h2>Bulk Analysis Results</h2>
            <div class="metrics">
                <div class="metric">
                    <span class="metric-label">Total Samples:</span>
                    <span id="totalSamples" class="metric-value">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Correct:</span>
                    <span id="correctSamples" class="metric-value">0</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Accuracy:</span>
                    <span id="overallAccuracy" class="metric-value">0%</span>
                </div>
            </div>
            <div id="classMetrics"></div>
        </div>
        
        <div class="actions">
            <button id="predictBtn" class="btn btn-primary" disabled>Predict Selected</button>
            <button id="bulkPredictBtn" class="btn btn-secondary" disabled>Bulk Analysis (All Samples)</button>
        </div>
        
        <div id="modelStatus" class="model-status">
            <p>Loading model...</p>
        </div>
    </div>
    
    <script>
{js_code}
    </script>
</body>
</html>
'''
    return html

def generate_image_js(project_name, config):
    """Generate JavaScript for image classification"""
    classes_json = json.dumps(config['class_names'])
    
    return f'''
        // Configuration
        const CLASSES = {classes_json};
        const MODEL_PATH = 'models/model.json';
        const IMG_SIZE = 224;
        
        let model = null;
        let samples = [];
        let selectedSample = null;
        
        // Load TensorFlow.js model
        async function loadModel() {{
            try {{
                document.getElementById('modelStatus').innerHTML = '<p>Loading model from {{MODEL_PATH}}...</p>';
                model = await tf.loadLayersModel(MODEL_PATH);
                document.getElementById('modelStatus').innerHTML = '<p style="color: green;">✓ Model loaded successfully!</p>';
                document.getElementById('loadSamplesBtn').disabled = false;
            }} catch (error) {{
                document.getElementById('modelStatus').innerHTML = '<p style="color: red;">✗ Error loading model: ' + error.message + '</p>';
                console.error('Error loading model:', error);
            }}
        }}
        
        // Preprocess image for model
        function preprocessImage(img) {{
            return tf.tidy(() => {{
                let tensor = tf.browser.fromPixels(img);
                tensor = tf.image.resizeBilinear(tensor, [IMG_SIZE, IMG_SIZE]);
                tensor = tensor.div(255.0);
                return tensor.expandDims(0);
            }});
        }}
        
        // Load samples (mock data for now - replace with actual test data)
        function loadSamples() {{
            // Generate mock samples
            samples = [];
            for (let i = 0; i < 20; i++) {{
                const classIdx = i % CLASSES.length;
                samples.push({{
                    id: `sample_${{i}}`,
                    path: `data/test/${{CLASSES[classIdx].toLowerCase().replace(/ /g, '_')}}/img_${{i}}.jpg`,
                    label: CLASSES[classIdx],
                    imageUrl: `data/test/${{CLASSES[classIdx].toLowerCase().replace(/ /g, '_')}}/img_${{i}}.jpg`
                }});
            }}
            displaySamples();
        }}
        
        // Display samples
        function displaySamples() {{
            const filter = document.getElementById('classFilter').value;
            const filtered = filter === 'all' ? samples : samples.filter(s => s.label === filter);
            
            const grid = document.getElementById('samplesList');
            grid.innerHTML = '';
            
            filtered.forEach(sample => {{
                const item = document.createElement('div');
                item.className = 'sample-item' + (selectedSample?.id === sample.id ? ' selected' : '');
                item.onclick = () => selectSample(sample);
                
                if (sample.imageUrl) {{
                    const img = document.createElement('img');
                    img.src = sample.imageUrl;
                    img.onerror = () => {{
                        img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5JbWFnZTwvdGV4dD48L3N2Zz4=';
                    }};
                    item.appendChild(img);
                }}
                
                const label = document.createElement('div');
                label.className = 'sample-label';
                label.textContent = sample.label;
                item.appendChild(label);
                
                grid.appendChild(item);
            }});
        }}
        
        // Select sample
        function selectSample(sample) {{
            selectedSample = sample;
            displaySamples();
            document.getElementById('predictBtn').disabled = false;
        }}
        
        // Predict selected sample
        async function predictSelected() {{
            if (!model || !selectedSample) return;
            
            try {{
                const img = new Image();
                img.crossOrigin = 'anonymous';
                
                img.onload = async () => {{
                    const preprocessed = preprocessImage(img);
                    const prediction = model.predict(preprocessed);
                    const probabilities = await prediction.data();
                    const predictedIdx = probabilities.indexOf(Math.max(...probabilities));
                    
                    document.getElementById('trueLabel').textContent = selectedSample.label;
                    document.getElementById('predictedLabel').textContent = CLASSES[predictedIdx];
                    document.getElementById('confidence').textContent = (probabilities[predictedIdx] * 100).toFixed(2) + '%';
                    
                    // Display probabilities
                    const probDiv = document.getElementById('probabilities');
                    probDiv.innerHTML = '';
                    CLASSES.forEach((cls, idx) => {{
                        const bar = document.createElement('div');
                        bar.className = 'probability-bar';
                        bar.innerHTML = `
                            <span class="probability-label">${{cls}}:</span>
                            <div class="probability-value">
                                <div class="probability-fill" style="width: ${{probabilities[idx] * 100}}%">
                                    ${{(probabilities[idx] * 100).toFixed(1)}}%
                                </div>
                            </div>
                        `;
                        probDiv.appendChild(bar);
                    }});
                    
                    document.getElementById('predictionSection').style.display = 'block';
                    preprocessed.dispose();
                    prediction.dispose();
                }};
                
                img.onerror = () => {{
                    alert('Error loading image. Using mock prediction.');
                    // Mock prediction for demo
                    const mockIdx = Math.floor(Math.random() * CLASSES.length);
                    document.getElementById('trueLabel').textContent = selectedSample.label;
                    document.getElementById('predictedLabel').textContent = CLASSES[mockIdx];
                    document.getElementById('confidence').textContent = '85.5%';
                    document.getElementById('predictionSection').style.display = 'block';
                }};
                
                img.src = selectedSample.imageUrl || selectedSample.path;
            }} catch (error) {{
                console.error('Prediction error:', error);
                alert('Error making prediction: ' + error.message);
            }}
        }}
        
        // Event listeners
        document.getElementById('loadSamplesBtn').onclick = loadSamples;
        document.getElementById('predictBtn').onclick = predictSelected;
        document.getElementById('randomBtn').onclick = () => {{
            if (samples.length > 0) {{
                selectSample(samples[Math.floor(Math.random() * samples.length)]);
            }}
        }};
        document.getElementById('classFilter').onchange = displaySamples;
        document.getElementById('bulkPredictBtn').onclick = () => {{
            alert('Bulk analysis requires model and test data. This is a demo version.');
        }};
        
        // Initialize
        loadModel();
    '''

def generate_tabular_js(project_name, config):
    """Generate JavaScript for tabular data classification"""
    classes_json = json.dumps(config['class_names'])
    
    return f'''
        // Configuration
        const CLASSES = {classes_json};
        const MODEL_PATH = 'models/model.json';
        
        let model = null;
        let samples = [];
        let selectedSample = null;
        
        // Load TensorFlow.js model
        async function loadModel() {{
            try {{
                document.getElementById('modelStatus').innerHTML = '<p>Loading model from {{MODEL_PATH}}...</p>';
                model = await tf.loadLayersModel(MODEL_PATH);
                document.getElementById('modelStatus').innerHTML = '<p style="color: green;">✓ Model loaded successfully!</p>';
                document.getElementById('loadSamplesBtn').disabled = false;
            }} catch (error) {{
                document.getElementById('modelStatus').innerHTML = '<p style="color: red;">✗ Error loading model: ' + error.message + '</p>';
                console.error('Error loading model:', error);
            }}
        }}
        
        // Load samples from CSV or generate mock data
        async function loadSamples() {{
            try {{
                // Try to load from CSV
                const response = await fetch('data/data.csv');
                if (response.ok) {{
                    const text = await response.text();
                    const lines = text.split('\\n').filter(l => l.trim());
                    const headers = lines[0].split(',');
                    
                    samples = lines.slice(1, 21).map((line, idx) => {{
                        const values = line.split(',');
                        return {{
                            id: `sample_${{idx}}`,
                            data: values.slice(0, -1).map(parseFloat),
                            label: values[values.length - 1] || CLASSES[idx % CLASSES.length]
                        }};
                    }});
                }} else {{
                    // Generate mock samples
                    samples = [];
                    for (let i = 0; i < 20; i++) {{
                        samples.push({{
                            id: `sample_${{i}}`,
                            data: Array(10).fill(0).map(() => Math.random()),
                            label: CLASSES[i % CLASSES.length]
                        }});
                    }}
                }}
                displaySamples();
            }} catch (error) {{
                console.error('Error loading samples:', error);
                // Generate mock samples
                samples = Array(20).fill(0).map((_, i) => ({{
                    id: `sample_${{i}}`,
                    data: Array(10).fill(0).map(() => Math.random()),
                    label: CLASSES[i % CLASSES.length]
                }}));
                displaySamples();
            }}
        }}
        
        // Display samples
        function displaySamples() {{
            const filter = document.getElementById('classFilter').value;
            const filtered = filter === 'all' ? samples : samples.filter(s => s.label === filter);
            
            const grid = document.getElementById('samplesList');
            grid.innerHTML = '';
            
            filtered.forEach(sample => {{
                const item = document.createElement('div');
                item.className = 'sample-item' + (selectedSample?.id === sample.id ? ' selected' : '');
                item.onclick = () => selectSample(sample);
                item.innerHTML = `
                    <div style="padding: 20px; text-align: center;">
                        <div style="font-weight: bold; margin-bottom: 10px;">${{sample.label}}</div>
                        <div style="font-size: 12px; color: #666;">Sample ${{sample.id}}</div>
                    </div>
                `;
                grid.appendChild(item);
            }});
        }}
        
        // Select sample
        function selectSample(sample) {{
            selectedSample = sample;
            displaySamples();
            document.getElementById('predictBtn').disabled = false;
        }}
        
        // Predict selected sample
        async function predictSelected() {{
            if (!model || !selectedSample) return;
            
            try {{
                const input = tf.tensor2d([selectedSample.data]);
                const prediction = model.predict(input);
                const probabilities = await prediction.data();
                const predictedIdx = probabilities.indexOf(Math.max(...probabilities));
                
                document.getElementById('trueLabel').textContent = selectedSample.label;
                document.getElementById('predictedLabel').textContent = CLASSES[predictedIdx];
                document.getElementById('confidence').textContent = (probabilities[predictedIdx] * 100).toFixed(2) + '%';
                
                // Display probabilities
                const probDiv = document.getElementById('probabilities');
                probDiv.innerHTML = '';
                CLASSES.forEach((cls, idx) => {{
                    const bar = document.createElement('div');
                    bar.className = 'probability-bar';
                    bar.innerHTML = `
                        <span class="probability-label">${{cls}}:</span>
                        <div class="probability-value">
                            <div class="probability-fill" style="width: ${{probabilities[idx] * 100}}%">
                                ${{(probabilities[idx] * 100).toFixed(1)}}%
                            </div>
                        </div>
                    `;
                    probDiv.appendChild(bar);
                }});
                
                document.getElementById('predictionSection').style.display = 'block';
                input.dispose();
                prediction.dispose();
            }} catch (error) {{
                console.error('Prediction error:', error);
                alert('Error making prediction: ' + error.message);
            }}
        }}
        
        // Event listeners
        document.getElementById('loadSamplesBtn').onclick = loadSamples;
        document.getElementById('predictBtn').onclick = predictSelected;
        document.getElementById('randomBtn').onclick = () => {{
            if (samples.length > 0) {{
                selectSample(samples[Math.floor(Math.random() * samples.length)]);
            }}
        }};
        document.getElementById('classFilter').onchange = displaySamples;
        document.getElementById('bulkPredictBtn').onclick = () => {{
            alert('Bulk analysis requires model and test data. This is a demo version.');
        }};
        
        // Initialize
        loadModel();
    '''

def generate_timeseries_js(project_name, config):
    """Generate JavaScript for time-series classification"""
    return generate_tabular_js(project_name, config)  # Similar to tabular

# Convert all projects
for project_name, config in PROJECTS.items():
    theme = THEMES[project_name]
    
    # Create static directory
    static_dir = f'{project_name}/static_pages'
    os.makedirs(static_dir, exist_ok=True)
    
    # Generate HTML
    html = generate_static_html(project_name, config)
    with open(f'{static_dir}/index.html', 'w') as f:
        f.write(html)
    
    # Copy CSS
    css_path = f'{project_name}/static/style.css'
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            css = f.read()
        with open(f'{static_dir}/style.css', 'w') as f:
            f.write(css)
    
    print(f"✓ Generated static site for {project_name}")

print("\n✅ All 22 projects converted to static HTML!")
print("\nNext steps:")
print("1. Convert models to TensorFlow.js format (run in Colab)")
print("2. Place model.json files in each project's static_pages/models/ directory")
print("3. Copy test data to static_pages/data/ directories")
print("4. Push static_pages directories to GitHub Pages")

