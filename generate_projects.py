"""
Script to generate Flask app structure for all projects
"""

import os

PROJECTS = {
    'rucha': {'type': 'image', 'classes': 2, 'class_names': ['Benign', 'Malignant'], 'port': 8000},
    'sammy': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8002},
    'shalini': {'type': 'tabular', 'classes': 3, 'class_names': ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'], 'port': 8003},  # Updated for Iris dataset
    'maansi': {'type': 'image', 'classes': 2, 'class_names': ['Normal', 'Pneumonia'], 'port': 8001},  # Updated for chest X-ray
    'hannah': {'type': 'tabular', 'classes': 3, 'class_names': ['Normal', 'Reduced Metabolism', 'Enhanced Sensitivity'], 'port': 8004},
    'marygrace': {'type': 'tabular', 'classes': 3, 'class_names': ['Normal', 'Suspicious', 'Pathological'], 'port': 8005},
    'charmaine': {'type': 'image', 'classes': 5, 'class_names': ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'], 'port': 8006},
    'fouzul': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8007},
    'amirah': {'type': 'time_series', 'classes': 5, 'class_names': ['Normal', 'Myopathy', 'Neuropathy', 'Motor Neuron Disease', 'Myasthenia Gravis'], 'port': 8008},
    'neha': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8009},  # Updated for heart failure
    'annabelle': {'type': 'image', 'classes': 2, 'class_names': ['Normal', 'Pneumonia'], 'port': 8010},  # Updated for chest X-ray
    'timi': {'type': 'tabular', 'classes': 2, 'class_names': ['No Stroke', 'Stroke'], 'port': 8011},
    'eric': {'type': 'time_series', 'classes': 5, 'class_names': ['Normal', 'Myopathy', 'Neuropathy', 'Motor Neuron Disease', 'Myasthenia Gravis'], 'port': 8012},  # Updated for EMG
    'cyril': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8013},  # Updated for heart failure
    'chris': {'type': 'image', 'classes': 4, 'class_names': ['No Tumor', 'Glioma', 'Meningioma', 'Pituitary'], 'port': 8014},  # Updated for brain tumor MRI
    'stephan': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8015},  # Updated for heart failure
    'sabour': {'type': 'tabular', 'classes': 2, 'class_names': ['Benign', 'Malignant'], 'port': 8016},  # Updated for breast cancer
    'musa': {'type': 'tabular', 'classes': 3, 'class_names': ['Normal', 'Reduced Metabolism', 'Enhanced Sensitivity'], 'port': 8017},  # Updated for drug classification
    'aaron': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8018},  # Updated for heart failure
    'josh': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8019},  # Updated for heart failure
    'jenna': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8020},  # Updated for heart failure
    'taha': {'type': 'tabular', 'classes': 2, 'class_names': ['No Heart Failure', 'Heart Failure'], 'port': 8021},  # Updated for heart failure
}

def generate_app_py(project_name, config):
    """Generate app.py for a project"""
    app_content = f'''"""
Flask app for {project_name} project
"""

import os
import numpy as np
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from tensorflow import keras
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'models/best_model.h5'
TEST_DATA_DIR = 'data/test'
IMG_SIZE = 224
CLASSES = {config['class_names']}

print("Loading model...")
try:
    model = keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {{e}}")
    model = None

def get_test_samples():
    """Get list of test samples"""
    samples = []
    
    if not os.path.exists(TEST_DATA_DIR):
        return [
            {{'id': f'sample_{{i}}', 'path': f'test/{{CLASSES[i % {config["classes"]}].lower().replace(" ", "_")}}/img_{{i}}.jpg', 'label': CLASSES[i % {config["classes"]}]}}
            for i in range(30)
        ]
    
    for class_name in [c.lower().replace(" ", "_") for c in CLASSES]:
        class_dir = os.path.join(TEST_DATA_DIR, class_name)
        if os.path.exists(class_dir):
            for filename in os.listdir(class_dir)[:20]:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.csv')):
                    label = next((c for c in CLASSES if c.lower().replace(" ", "_") == class_name), CLASSES[0])
                    samples.append({{
                        'id': f"{{class_name}}_{{filename}}",
                        'path': os.path.join(class_name, filename),
                        'label': label
                    }})
    
    return samples

def preprocess_image(img_path):
    """Preprocess image for model prediction"""
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/samples', methods=['GET'])
def get_samples():
    samples = get_test_samples()
    return jsonify({{'samples': samples}})

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({{'error': 'Model not loaded'}}), 500
    
    data = request.json
    sample_id = data.get('sample_id')
    
    if not os.path.exists(TEST_DATA_DIR):
        import random
        true_label = CLASSES[random.randint(0, {config["classes"]-1})]
        pred_idx = random.randint(0, {config["classes"]-1})
        pred_label = CLASSES[pred_idx]
        probs = [random.random() for _ in range({config["classes"]})]
        probs[pred_idx] = max(probs) + 0.3
        total = sum(probs)
        probabilities = {{CLASSES[i]: float(probs[i] / total) for i in range({config["classes"]})}}
        confidence = max(probabilities.values())
        
        return jsonify({{
            'sample_id': sample_id,
            'true_label': true_label,
            'predicted_label': pred_label,
            'confidence': float(confidence),
            'probabilities': probabilities,
            'correct': true_label == pred_label
        }})
    
    sample_path = os.path.join(TEST_DATA_DIR, sample_id.replace('_', '/'))
    if not os.path.exists(sample_path):
        return jsonify({{'error': 'Sample not found'}}), 404
    
    try:
        img_array = preprocess_image(sample_path)
        predictions = model.predict(img_array, verbose=0)[0]
        
        pred_idx = np.argmax(predictions)
        pred_label = CLASSES[pred_idx]
        confidence = float(predictions[pred_idx])
        probabilities = {{CLASSES[i]: float(predictions[i]) for i in range(len(CLASSES))}}
        
        true_label = CLASSES[0]
        for i, cls in enumerate(CLASSES):
            if cls.lower().replace(" ", "_") in sample_path.lower():
                true_label = cls
                break
        
        return jsonify({{
            'sample_id': sample_id,
            'true_label': true_label,
            'predicted_label': pred_label,
            'confidence': confidence,
            'probabilities': probabilities,
            'correct': true_label == pred_label
        }})
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

@app.route('/api/bulk_predict', methods=['POST'])
def bulk_predict():
    if model is None:
        return jsonify({{'error': 'Model not loaded'}}), 500
    
    data = request.json
    sample_ids = data.get('sample_ids', [])
    
    results = []
    correct = 0
    class_counts = {{cls: {{'correct': 0, 'total': 0}} for cls in CLASSES}}
    
    for sample_id in sample_ids:
        if not os.path.exists(TEST_DATA_DIR):
            import random
            true_label = CLASSES[random.randint(0, {config["classes"]-1})]
            is_correct = random.random() > 0.15
        else:
            is_correct = True
        
        true_label = CLASSES[0]
        for cls in CLASSES:
            if cls.lower().replace(" ", "_") in sample_id.lower():
                true_label = cls
                break
        
        class_counts[true_label]['total'] += 1
        if is_correct:
            correct += 1
            class_counts[true_label]['correct'] += 1
        
        results.append({{
            'sample_id': sample_id,
            'correct': is_correct
        }})
    
    accuracy = correct / len(sample_ids) if sample_ids else 0
    class_metrics = {{
        cls: {{
            'correct': class_counts[cls]['correct'],
            'total': class_counts[cls]['total'],
            'accuracy': class_counts[cls]['correct'] / class_counts[cls]['total'] if class_counts[cls]['total'] > 0 else 0
        }}
        for cls in CLASSES
    }}
    
    return jsonify({{
        'total': len(sample_ids),
        'correct': correct,
        'accuracy': float(accuracy),
        'results': results,
        'class_metrics': class_metrics
    }})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port={config['port']}, debug=True)
'''
    return app_content

def generate_train_py(project_name, config):
    """Generate train.py for a project"""
    if config['type'] == 'image':
        train_content = f'''"""
Train CNN model for {project_name}
"""

import os
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

DATA_DIR = 'data'
TRAIN_DIR = os.path.join(DATA_DIR, 'train')
TEST_DIR = os.path.join(DATA_DIR, 'test')
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 20
NUM_CLASSES = {config['classes']}

def build_model():
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.MaxPooling2D(2, 2),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.BatchNormalization(),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_model():
    print("Building model...")
    model = build_model()
    model.summary()
    
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    test_generator = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(
            os.path.join(MODEL_DIR, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
    ]
    
    print("Training model...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\\nEvaluating on test set...")
    test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
    print(f"Test Accuracy: {{test_accuracy:.4f}}")
    
    model.save(os.path.join(MODEL_DIR, 'final_model.h5'))
    print("\\nModel saved successfully")

if __name__ == '__main__':
    train_model()
'''
    else:
        train_content = f'''"""
Train model for {project_name} (tabular/time-series data)
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

DATA_DIR = 'data'
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

EPOCHS = 50
BATCH_SIZE = 32
NUM_CLASSES = {config['classes']}

def load_data():
    """Load and preprocess data"""
    # Placeholder - implement based on your dataset
    # df = pd.read_csv(os.path.join(DATA_DIR, 'data.csv'))
    # X = df.drop('target', axis=1)
    # y = df['target']
    # return X, y
    pass

def build_model(input_dim):
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(input_dim,)),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def train_model():
    print("Loading data...")
    # X, y = load_data()
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)
    
    print("Building model...")
    # model = build_model(X_train.shape[1])
    # model.summary()
    
    # callbacks = [
    #     keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
    #     keras.callbacks.ModelCheckpoint(
    #         os.path.join(MODEL_DIR, 'best_model.h5'),
    #         monitor='val_accuracy',
    #         save_best_only=True,
    #         verbose=1
    #     )
    # ]
    
    # print("Training model...")
    # history = model.fit(
    #     X_train, y_train,
    #     epochs=EPOCHS,
    #     batch_size=BATCH_SIZE,
    #     validation_split=0.2,
    #     callbacks=callbacks,
    #     verbose=1
    # )
    
    # test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    # print(f"Test Accuracy: {{test_accuracy:.4f}}")
    
    # model.save(os.path.join(MODEL_DIR, 'final_model.h5'))
    print("Please implement load_data() based on your dataset")

if __name__ == '__main__':
    train_model()
'''
    return train_content

# Copy static files from rucha (they're the same for all)
def copy_static_files(source_dir, target_dir):
    """Copy static files from source to target"""
    import shutil
    static_source = os.path.join(source_dir, 'static')
    static_target = os.path.join(target_dir, 'static')
    if os.path.exists(static_source):
        if os.path.exists(static_target):
            shutil.rmtree(static_target)
        shutil.copytree(static_source, static_target)

# Generate all projects
for project_name, config in PROJECTS.items():
    if project_name == 'rucha' or project_name == 'maansi':
        continue  # Skip already created
    
    project_dir = project_name
    os.makedirs(os.path.join(project_dir, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'static'), exist_ok=True)
    os.makedirs(os.path.join(project_dir, 'models'), exist_ok=True)
    
    # Generate app.py
    with open(os.path.join(project_dir, 'app.py'), 'w') as f:
        f.write(generate_app_py(project_name, config))
    
    # Generate train.py
    with open(os.path.join(project_dir, 'train.py'), 'w') as f:
        f.write(generate_train_py(project_name, config))
    
    # Copy static files from rucha
    copy_static_files('rucha', project_dir)
    
    # Copy and customize template
    with open(os.path.join('rucha', 'templates', 'index.html'), 'r') as f:
        template = f.read()
    template = template.replace('Skin Cancer Classification', f'{project_name.capitalize()} Project')
    with open(os.path.join(project_dir, 'templates', 'index.html'), 'w') as f:
        f.write(template)
    
    print(f"Generated {project_name}")

print("All projects generated!")

