"""
Train CNN model for multi-disease chest X-ray classification
Dataset: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia
Classes: Normal, Pneumonia, COVID-19
"""

import os
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Configuration
DATA_DIR = 'data'
# Check for chest_xray subdirectory (handle nested structure)
if os.path.exists(os.path.join(DATA_DIR, 'chest_xray', 'chest_xray', 'train')):
    TRAIN_DIR = os.path.join(DATA_DIR, 'chest_xray', 'chest_xray', 'train')
    TEST_DIR = os.path.join(DATA_DIR, 'chest_xray', 'chest_xray', 'test')
elif os.path.exists(os.path.join(DATA_DIR, 'chest_xray', 'train')):
    TRAIN_DIR = os.path.join(DATA_DIR, 'chest_xray', 'train')
    TEST_DIR = os.path.join(DATA_DIR, 'chest_xray', 'test')
else:
    TRAIN_DIR = os.path.join(DATA_DIR, 'train')
    TEST_DIR = os.path.join(DATA_DIR, 'test')
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10  # Reduced from 20 for faster training (can increase later)
NUM_CLASSES = 2  # Normal, Pneumonia (dataset only has 2 classes)

def build_model():
    """Build CNN model for chest X-ray classification"""
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
    # Skip if model already exists
    MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.h5')
    if os.path.exists(MODEL_PATH):
        print(f"✓ Model already exists at {MODEL_PATH}")
        print("Skipping training. Delete the model file to retrain.")
        return
    

    """Train the model"""
    print("Building model...")
    model = build_model()
    model.summary()
    
    # Data generators
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
    
    # Callbacks
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
    
    # Evaluate
    print("\nEvaluating on test set...")
    test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Save
    model.save(os.path.join(MODEL_DIR, 'final_model.h5'))
    print(f"\nModel saved to {MODEL_DIR}/")
    
    return model, history

if __name__ == '__main__':
    train_model()

