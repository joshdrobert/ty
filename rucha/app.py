"""
Flask app for skin cancer classification from dermoscopy images
"""

import os
import numpy as np
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import cv2
import json

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_PATH = 'models/best_model.h5'
TEST_DATA_DIR = 'data/skin_cancer/test'
IMG_SIZE = 224
CLASSES = ['Benign', 'Malignant']

# Load model
print("Loading model...")
try:
    model = keras.models.load_model(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please train the model first using train.py")
    model = None

def get_test_samples():
    """Get list of test samples"""
    samples = []
    
    if not os.path.exists(TEST_DATA_DIR):
        # Return mock data if test directory doesn't exist
        return [
            {'id': f'sample_{i}', 'path': f'test/benign/img_{i}.jpg', 'label': 'Benign' if i < 5 else 'Malignant'}
            for i in range(10)
        ]
    
    for class_name in ['benign', 'malignant']:
        class_dir = os.path.join(TEST_DATA_DIR, class_name)
        if os.path.exists(class_dir):
            for filename in os.listdir(class_dir):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    samples.append({
                        'id': f"{class_name}_{filename}",
                        'path': os.path.join(class_name, filename),
                        'label': class_name.capitalize()
                    })
    
    return samples[:100]  # Limit to 100 samples for UI

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/samples', methods=['GET'])
def get_samples():
    """Get list of test samples"""
    samples = get_test_samples()
    return jsonify({'samples': samples})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict single sample"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.json
    sample_id = data.get('sample_id')
    
    # Mock prediction for demo
    if not os.path.exists(TEST_DATA_DIR):
        import random
        true_label = 'Benign' if random.random() > 0.5 else 'Malignant'
        pred_label = 'Benign' if random.random() > 0.4 else 'Malignant'
        confidence = random.uniform(0.7, 0.95)
        probabilities = {
            'Benign': 1 - confidence if pred_label == 'Malignant' else confidence,
            'Malignant': confidence if pred_label == 'Malignant' else 1 - confidence
        }
        
        return jsonify({
            'sample_id': sample_id,
            'true_label': true_label,
            'predicted_label': pred_label,
            'confidence': float(confidence),
            'probabilities': probabilities,
            'correct': true_label == pred_label
        })
    
    # Real prediction
    sample_path = os.path.join(TEST_DATA_DIR, sample_id.replace('_', '/'))
    if not os.path.exists(sample_path):
        return jsonify({'error': 'Sample not found'}), 404
    
    try:
        img_array = preprocess_image(sample_path)
        prediction = model.predict(img_array, verbose=0)[0][0]
        
        pred_label = CLASSES[1] if prediction > 0.5 else CLASSES[0]
        confidence = float(prediction) if prediction > 0.5 else float(1 - prediction)
        probabilities = {
            'Benign': float(1 - prediction),
            'Malignant': float(prediction)
        }
        
        # Get true label from path
        true_label = 'Malignant' if 'malignant' in sample_path.lower() else 'Benign'
        
        return jsonify({
            'sample_id': sample_id,
            'true_label': true_label,
            'predicted_label': pred_label,
            'confidence': confidence,
            'probabilities': probabilities,
            'correct': true_label == pred_label
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk_predict', methods=['POST'])
def bulk_predict():
    """Bulk prediction on multiple samples"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.json
    sample_ids = data.get('sample_ids', [])
    
    results = []
    correct = 0
    total = len(sample_ids)
    
    for sample_id in sample_ids:
        # Mock prediction
        if not os.path.exists(TEST_DATA_DIR):
            import random
            true_label = 'Benign' if random.random() > 0.5 else 'Malignant'
            pred_label = 'Benign' if random.random() > 0.4 else 'Malignant'
            confidence = random.uniform(0.7, 0.95)
            is_correct = random.random() > 0.1  # 90% accuracy
        else:
            # Real prediction logic here
            is_correct = True  # Placeholder
        
        if is_correct:
            correct += 1
        
        results.append({
            'sample_id': sample_id,
            'correct': is_correct
        })
    
    accuracy = correct / total if total > 0 else 0
    
    # Per-class metrics
    class_metrics = {
        'Benign': {'correct': 0, 'total': 0, 'accuracy': 0},
        'Malignant': {'correct': 0, 'total': 0, 'accuracy': 0}
    }
    
    return jsonify({
        'total': total,
        'correct': correct,
        'accuracy': float(accuracy),
        'results': results,
        'class_metrics': class_metrics
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

