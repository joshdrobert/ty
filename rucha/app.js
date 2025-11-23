// TensorFlow.js Model and UI Logic
let model = null;
let testImages = [];

// Model configuration
const IMG_SIZE = 224;
const CLASS_NAMES = ['Benign', 'Malignant'];
const MODEL_PATH = 'models/model.json'; // TensorFlow.js model path

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadModel();
    await loadTestImages();
});

// Load TensorFlow.js model
async function loadModel() {
    const statusCard = document.getElementById('modelStatus');
    const statusIcon = statusCard.querySelector('.status-icon');
    const statusText = statusCard.querySelector('p');
    
    try {
        statusCard.className = 'status-card loading';
        statusIcon.textContent = '⏳';
        statusText.textContent = 'Loading AI model...';
        
        // Try to load the model
        // Load with explicit error handling for Keras 3.x compatibility
        model = await tf.loadLayersModel(MODEL_PATH, {
            strict: false  // Allow some flexibility with model structure
        });
        
        statusCard.className = 'status-card ready';
        statusIcon.textContent = '✓';
        statusText.textContent = 'Model loaded successfully!';
        
        console.log('Model loaded:', model);
    } catch (error) {
        console.error('Error loading model:', error);
        statusCard.className = 'status-card error';
        statusIcon.textContent = '⚠';
        
        // Show more detailed error message
        const errorMsg = error.message || error.toString();
        if (errorMsg.includes('404') || errorMsg.includes('Failed to fetch')) {
            statusText.textContent = 'Model file not found. Check that models/model.json exists.';
        } else if (errorMsg.includes('CORS')) {
            statusText.textContent = 'CORS error. Make sure you\'re using a local server (not file://).';
        } else {
            statusText.textContent = `Model loading error: ${errorMsg.substring(0, 100)}`;
        }
        
        // For demo purposes, create a mock model
        console.log('Creating mock model for demonstration...');
        model = createMockModel();
    }
}

// Create a mock model for demonstration (when actual model is not available)
function createMockModel() {
    return {
        predict: async (tensor) => {
            // Simulate prediction with some randomness
            await new Promise(resolve => setTimeout(resolve, 500));
            const random = Math.random();
            const benignProb = random > 0.5 ? random : 1 - random;
            const malignantProb = 1 - benignProb;
            return tf.tensor2d([[benignProb, malignantProb]]);
        }
    };
}

// Load test images from data directory
async function loadTestImages() {
    const gallery = document.getElementById('imageGallery');
    
    try {
        // Try to load test images from JSON file
        const response = await fetch('test_images.json');
        if (response.ok) {
            const imageData = await response.json();
            testImages = imageData;
            renderImageGallery();
        } else {
            // Fallback: try to discover images manually
            console.log('test_images.json not found, trying to discover images...');
            discoverTestImages();
        }
    } catch (error) {
        console.error('Error loading test images:', error);
        // Try fallback discovery
        discoverTestImages();
    }
}

// Fallback: Try to discover test images by attempting common paths
function discoverTestImages() {
    const gallery = document.getElementById('imageGallery');
    const commonPaths = [
        'data/test/benign_',
        'data/test/malignant_'
    ];
    
    // Try to load a few test images
    const testPaths = [];
    for (let i = 1; i <= 20; i++) {
        testPaths.push({ path: `data/test/benign_${i}.jpg`, label: 'benign', id: testPaths.length });
        testPaths.push({ path: `data/test/malignant_${i}.jpg`, label: 'malignant', id: testPaths.length });
    }
    
    // Verify which images exist
    let foundCount = 0;
    testImages = [];
    
    testPaths.forEach(async (img) => {
        try {
            const response = await fetch(img.path, { method: 'HEAD' });
            if (response.ok) {
                testImages.push(img);
                foundCount++;
            }
        } catch (e) {
            // Image doesn't exist, skip
        }
    });
    
    // Wait a bit then render
    setTimeout(() => {
        if (testImages.length > 0) {
            renderImageGallery();
        } else {
            gallery.innerHTML = '<p class="loading-text">No test images found. Please run download_data.py and generate_image_list.py first.</p>';
        }
    }, 1000);
}

// Render image gallery
function renderImageGallery() {
    const gallery = document.getElementById('imageGallery');
    gallery.innerHTML = '';
    
    testImages.forEach(image => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.dataset.imageId = image.id;
        
        item.innerHTML = `
            <img src="${image.path}" alt="${image.label}" loading="lazy">
            <div class="gallery-item-label">${image.label}</div>
        `;
        
        item.addEventListener('click', () => selectImage(image));
        gallery.appendChild(item);
    });
}

// Select and analyze an image
async function selectImage(image) {
    // Update selected state in gallery
    document.querySelectorAll('.gallery-item').forEach(item => {
        item.classList.remove('selected');
    });
    document.querySelector(`[data-image-id="${image.id}"]`).classList.add('selected');
    
    // Show analysis section
    const analysisSection = document.getElementById('analysisSection');
    analysisSection.classList.remove('hidden');
    
    // Display selected image
    const selectedImage = document.getElementById('selectedImage');
    selectedImage.src = image.path;
    
    // Show loading state
    updatePrediction('Analyzing...', 0, [0.5, 0.5]);
    
    // Preprocess and predict
    try {
        const prediction = await predictImage(image.path);
        const [benignProb, malignantProb] = prediction;
        const predictedClass = benignProb > malignantProb ? 0 : 1;
        const confidence = Math.max(benignProb, malignantProb);
        
        // Update UI
        updatePrediction(
            CLASS_NAMES[predictedClass],
            confidence,
            [benignProb, malignantProb]
        );
        
        // Update interpretation
        updateInterpretation(predictedClass, confidence);
        
    } catch (error) {
        console.error('Prediction error:', error);
        updatePrediction('Error', 0, [0, 0]);
    }
}

// Preprocess image and make prediction
async function predictImage(imagePath) {
    // Load and preprocess image
    const img = new Image();
    img.crossOrigin = 'anonymous';
    
    return new Promise((resolve, reject) => {
        img.onload = async () => {
            try {
                // Preprocess image
                const tensor = tf.browser.fromPixels(img)
                    .resizeNearestNeighbor([IMG_SIZE, IMG_SIZE])
                    .expandDims(0)
                    .div(255.0);
                
                // Make prediction
                const prediction = await model.predict(tensor);
                const probabilities = await prediction.data();
                
                // Clean up
                tensor.dispose();
                prediction.dispose();
                
                resolve([probabilities[0], probabilities[1]]);
            } catch (error) {
                reject(error);
            }
        };
        
        img.onerror = () => reject(new Error('Failed to load image'));
        img.src = imagePath;
    });
}

// Update prediction display
function updatePrediction(label, confidence, probabilities) {
    const predictionLabel = document.getElementById('predictionLabel');
    const predictionConfidence = document.getElementById('predictionConfidence');
    const confidenceBar = document.getElementById('confidenceBar');
    
    predictionLabel.textContent = label;
    predictionConfidence.textContent = `${(confidence * 100).toFixed(1)}%`;
    confidenceBar.style.width = `${confidence * 100}%`;
    
    // Update probability bars
    const benignProb = probabilities[0];
    const malignantProb = probabilities[1];
    
    document.getElementById('benignProb').style.width = `${benignProb * 100}%`;
    document.getElementById('benignPercent').textContent = `${(benignProb * 100).toFixed(1)}%`;
    
    document.getElementById('malignantProb').style.width = `${malignantProb * 100}%`;
    document.getElementById('malignantPercent').textContent = `${(malignantProb * 100).toFixed(1)}%`;
}

// Update clinical interpretation
function updateInterpretation(predictedClass, confidence) {
    const interpretationText = document.getElementById('interpretationText');
    
    const interpretations = {
        0: { // Benign
            high: "The AI model indicates a high probability of a benign lesion. However, any suspicious skin changes should be evaluated by a dermatologist for definitive diagnosis.",
            medium: "The model suggests this may be a benign lesion, but professional medical evaluation is recommended to confirm the diagnosis.",
            low: "The prediction suggests benign classification, but confidence is lower. Please consult with a healthcare professional for accurate diagnosis."
        },
        1: { // Malignant
            high: "⚠️ The AI model indicates a high probability of a malignant lesion. Immediate consultation with a dermatologist or oncologist is strongly recommended for proper evaluation and potential biopsy.",
            medium: "The model suggests this lesion may be malignant. Professional medical evaluation is essential for accurate diagnosis and appropriate treatment planning.",
            low: "There is some indication of potential malignancy, though confidence is moderate. Please seek professional medical evaluation to rule out any concerns."
        }
    };
    
    let confidenceLevel = 'medium';
    if (confidence > 0.8) confidenceLevel = 'high';
    else if (confidence < 0.6) confidenceLevel = 'low';
    
    interpretationText.textContent = interpretations[predictedClass][confidenceLevel];
    
    // Add warning styling for malignant predictions
    if (predictedClass === 1) {
        interpretationText.style.color = 'var(--accent-color)';
        interpretationText.style.fontWeight = '600';
    } else {
        interpretationText.style.color = 'var(--text-secondary)';
        interpretationText.style.fontWeight = '400';
    }
}

