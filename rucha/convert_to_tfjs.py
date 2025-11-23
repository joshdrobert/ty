"""
Convert Keras .h5 model to TensorFlow.js format for browser deployment
"""
import tensorflowjs as tfjs
import tensorflow as tf
from tensorflow import keras
import os
import shutil

MODEL_DIR = "models"
H5_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.h5")
TFJS_OUTPUT_DIR = os.path.join(MODEL_DIR)

if not os.path.exists(H5_MODEL_PATH):
    print(f"Error: Model file not found at {H5_MODEL_PATH}")
    print("Please train the model first using train_model.py")
    exit(1)

# Check file size
file_size = os.path.getsize(H5_MODEL_PATH)
print(f"Model file size: {file_size / (1024*1024):.2f} MB")

# Backup existing TF.js model if it exists
if os.path.exists(os.path.join(TFJS_OUTPUT_DIR, "model.json")):
    backup_dir = os.path.join(TFJS_OUTPUT_DIR, "backup")
    os.makedirs(backup_dir, exist_ok=True)
    print(f"\nBacking up existing model to {backup_dir}/")
    for f in os.listdir(TFJS_OUTPUT_DIR):
        if f.endswith(('.json', '.bin')) and f != 'best_model.h5':
            shutil.move(os.path.join(TFJS_OUTPUT_DIR, f), os.path.join(backup_dir, f))

print(f"\nConverting {H5_MODEL_PATH} to TensorFlow.js format...")
print(f"Output directory: {TFJS_OUTPUT_DIR}")

try:
    # Load the model first
    print("Loading Keras model...")
    model = keras.models.load_model(H5_MODEL_PATH)
    print("✓ Model loaded successfully")
    
    # Convert to TensorFlow.js
    print("Converting to TensorFlow.js format...")
    tfjs.converters.save_keras_model(
        model,
        TFJS_OUTPUT_DIR
    )
    
    print(f"\n✓ Model converted successfully!")
    print(f"✓ TensorFlow.js model saved to: {TFJS_OUTPUT_DIR}/model.json")
    
    # List created files
    tfjs_files = [f for f in os.listdir(TFJS_OUTPUT_DIR) if f.endswith(('.json', '.bin'))]
    print(f"\nCreated {len(tfjs_files)} file(s):")
    for f in tfjs_files:
        size = os.path.getsize(os.path.join(TFJS_OUTPUT_DIR, f))
        print(f"  - {f} ({size / (1024*1024):.2f} MB)")
    
    print(f"\n✓ You can now use this model in your browser with TensorFlow.js")
    
except Exception as e:
    print(f"\n❌ Error converting model: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

