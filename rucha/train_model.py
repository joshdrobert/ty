"""
Train a CNN model for skin cancer classification (Benign vs Malignant)
Uses Transfer Learning with MobileNetV2 for high accuracy
Model will be converted to TensorFlow.js for GitHub Pages deployment
"""
import os
import numpy as np
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from collections import Counter
from sklearn.metrics import classification_report, confusion_matrix

# Configuration
DATA_DIR = "data"
TRAIN_DIR = os.path.join(DATA_DIR, "train")
MODEL_DIR = "models"
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50  # More epochs for better training
NUM_CLASSES = 2
CLASS_NAMES = ['Benign', 'Malignant']

# Create model directory
os.makedirs(MODEL_DIR, exist_ok=True)

# Check if model already exists
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.h5')
if os.path.exists(MODEL_PATH):
    print(f"✓ Model already exists at {MODEL_PATH}")
    print("Skipping training. Delete the model file to retrain.")
    exit(0)

# Enhanced data augmentation for better generalization
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.3,
    height_shift_range=0.3,
    horizontal_flip=True,
    vertical_flip=True,
    zoom_range=0.3,
    shear_range=0.2,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest',
    validation_split=0.2
)

# Validation data (no augmentation, just rescaling)
val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Load training data
print("Loading training data...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

validation_generator = val_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

print(f"Classes: {train_generator.class_indices}")
print(f"Training samples: {train_generator.samples}")
print(f"Validation samples: {validation_generator.samples}")

# Calculate class weights for imbalanced data
class_counts = Counter(train_generator.classes)
total_samples = sum(class_counts.values())
class_weights = {}
for class_idx, count in class_counts.items():
    class_weights[class_idx] = total_samples / (NUM_CLASSES * count)

print(f"\nClass distribution: {dict(class_counts)}")
print(f"Class weights (for imbalanced data): {class_weights}")

# Build model using Transfer Learning with MobileNetV2
print("\nBuilding model with Transfer Learning (MobileNetV2)...")

# Load pre-trained MobileNetV2 (trained on ImageNet)
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Freeze base model layers initially
base_model.trainable = False

# Add custom classification head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(NUM_CLASSES, activation='softmax')(x)

# Create the full model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile with lower learning rate for transfer learning
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', 'precision', 'recall']
)

print("\nModel architecture:")
print(model.summary())

print(model.summary())

# Callbacks
callbacks = [
    ModelCheckpoint(
        MODEL_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1,
        save_weights_only=False
    ),
    EarlyStopping(
        monitor='val_accuracy',
        patience=10,  # More patience for better training
        restore_best_weights=True,
        verbose=1,
        mode='max'
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
]

# Train model - Phase 1: Train only the head
print("\n" + "="*60)
print("Phase 1: Training classification head (base model frozen)")
print("="*60)
history1 = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=10,  # Train head for 10 epochs
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=callbacks,
    class_weight=class_weights,  # Use class weights for imbalanced data
    verbose=1
)

# Phase 2: Fine-tune the entire model
print("\n" + "="*60)
print("Phase 2: Fine-tuning entire model (unfreezing base layers)")
print("="*60)

# Unfreeze some layers of the base model for fine-tuning
base_model.trainable = True
# Freeze early layers, fine-tune later layers
for layer in base_model.layers[:-30]:  # Freeze first layers
    layer.trainable = False

# Recompile with lower learning rate for fine-tuning
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.00001),  # Lower LR for fine-tuning
    loss='categorical_crossentropy',
    metrics=['accuracy', 'precision', 'recall']
)

# Continue training
history2 = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS - 10,  # Remaining epochs
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1,
    initial_epoch=10
)

# Evaluate
print("\n" + "="*60)
print("Evaluating model on validation set...")
print("="*60)
results = model.evaluate(validation_generator, verbose=1)
print(f"\n✓ Final validation metrics:")
print(f"  - Loss: {results[0]:.4f}")
print(f"  - Accuracy: {results[1]:.4f} ({results[1]*100:.2f}%)")
if len(results) > 2:
    print(f"  - Precision: {results[2]:.4f}")
    print(f"  - Recall: {results[3]:.4f}")

# Get predictions for confusion matrix
print("\nGenerating detailed predictions...")
validation_generator.reset()
y_true = []
y_pred = []
for i in range(len(validation_generator)):
    x, y = validation_generator[i]
    pred = model.predict(x, verbose=0)
    y_true.extend(np.argmax(y, axis=1))
    y_pred.extend(np.argmax(pred, axis=1))

# Calculate per-class metrics
print("\n" + "="*60)
print("Classification Report:")
print("="*60)
class_names_list = [CLASS_NAMES[i] for i in sorted(train_generator.class_indices.values())]
print(classification_report(y_true, y_pred, target_names=class_names_list))

print("\nConfusion Matrix:")
print(confusion_matrix(y_true, y_pred))
print(f"\n✓ Model saved to: {MODEL_PATH}")
print("="*60)

