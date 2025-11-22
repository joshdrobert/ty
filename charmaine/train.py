"""
Train CNN model for charmaine - Diabetic Retinopathy
Dataset has images in flat directory with CSV labels
"""
import os
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

DATA_DIR = 'data'
# Find the actual image directory
if os.path.exists(os.path.join(DATA_DIR, 'resized_train_cropped', 'resized_train_cropped')):
    IMAGE_DIR = os.path.join(DATA_DIR, 'resized_train_cropped', 'resized_train_cropped')
elif os.path.exists(os.path.join(DATA_DIR, 'resized_train_cropped')):
    IMAGE_DIR = os.path.join(DATA_DIR, 'resized_train_cropped')
else:
    IMAGE_DIR = os.path.join(DATA_DIR, 'train')

TEST_DIR = os.path.join(DATA_DIR, 'test')
MODEL_DIR = 'models'
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = 128  # Reduced from 224 for 4x faster processing (70K images!)
BATCH_SIZE = 64  # Increased batch size for faster training
EPOCHS = 5  # Reduced to 5 epochs (early stopping will likely trigger)
NUM_CLASSES = 5

def organize_images_by_class():
    """Organize images into class subdirectories based on CSV - OPTIMIZED"""
    # Check if already organized
    organized_dir = os.path.join(DATA_DIR, 'train_organized')
    if os.path.exists(organized_dir):
        class_dirs = [d for d in os.listdir(organized_dir) 
                      if os.path.isdir(os.path.join(organized_dir, d)) and d.startswith('class_')]
        if len(class_dirs) >= 5:
            print(f"✓ Using existing organized directory ({len(class_dirs)} classes)")
            return organized_dir
    
    csv_path = os.path.join(DATA_DIR, 'trainLabels_cropped.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(DATA_DIR, 'trainLabels.csv')
    
    if not os.path.exists(csv_path):
        print("⚠ CSV file not found. Using existing directory structure.")
        return IMAGE_DIR
    
    print("Loading CSV...")
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} images in CSV")
    
    # Create class directories
    os.makedirs(organized_dir, exist_ok=True)
    for level in range(5):
        class_dir = os.path.join(organized_dir, f'class_{level}')
        os.makedirs(class_dir, exist_ok=True)
    
    # OPTIMIZATION: Use subset for faster training (70K is too many!)
    # Use 20% of data for faster training (still ~14K images)
    if len(df) > 10000:
        print(f"⚠ Dataset has {len(df)} images - using 20% subset for faster training")
        df = df.sample(frac=0.2, random_state=42).reset_index(drop=True)
        print(f"Training on {len(df)} images (20% of full dataset)")
    
    # Organize images (use symlinks to save space and time)
    organized_count = 0
    skipped = 0
    for idx, row in df.iterrows():
        image_name = str(row['image']).split('.')[0]  # Remove extension if present
        level = int(row['level'])
        
        # Try different extensions
        found = False
        for ext in ['.jpeg', '.jpg', '.png']:
            src = os.path.join(IMAGE_DIR, f"{image_name}{ext}")
            if os.path.exists(src):
                dst = os.path.join(organized_dir, f'class_{level}', f"{image_name}{ext}")
                if not os.path.exists(dst):
                    try:
                        os.symlink(os.path.abspath(src), dst)
                        organized_count += 1
                        found = True
                    except:
                        try:
                            import shutil
                            shutil.copy2(src, dst)
                            organized_count += 1
                            found = True
                        except:
                            skipped += 1
                else:
                    organized_count += 1
                    found = True
                break
        
        if not found:
            skipped += 1
        
        if (idx + 1) % 1000 == 0:
            print(f"  Progress: {idx+1}/{len(df)} ({organized_count} organized, {skipped} skipped)")
    
    print(f"✓ Organized {organized_count} images into class directories")
    if skipped > 0:
        print(f"  (Skipped {skipped} images not found)")
    return organized_dir

def build_model():
    # Simplified model for faster training (70K images needs efficiency!)
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
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),  # Reduced from 512
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',  # Use sparse for integer labels
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
    
    print("Organizing images by class from CSV...")
    TRAIN_DIR = organize_images_by_class()
    
    # Check if we have class directories
    class_dirs = [d for d in os.listdir(TRAIN_DIR) 
                  if os.path.isdir(os.path.join(TRAIN_DIR, d)) and d.startswith('class_')]
    
    if len(class_dirs) < 5:
        print("⚠ Error: Could not organize images into class directories")
        print("Trying to use existing directory structure...")
        TRAIN_DIR = IMAGE_DIR
    
    print("Building model...")
    model = build_model()
    model.summary()
    
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        # Reduced augmentation for faster training
        horizontal_flip=True,
        validation_split=0.2
    )
    
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    print("Creating data generators...")
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='sparse',  # Use sparse for integer labels
        subset='training',
        shuffle=True
    )
    
    val_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='sparse',
        subset='validation',
        shuffle=False
    )
    
    if os.path.exists(TEST_DIR):
        test_generator = test_datagen.flow_from_directory(
            TEST_DIR,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='sparse',
            shuffle=False
        )
    else:
        test_generator = None
    
    print(f"Found {train_generator.samples} training samples")
    print(f"Found {val_generator.samples} validation samples")
    
    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True),  # More aggressive early stopping
        keras.callbacks.ModelCheckpoint(
            os.path.join(MODEL_DIR, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1, min_lr=1e-6)
    ]
    
    print("Training model...")
    print(f"Note: Optimized for speed - {EPOCHS} epochs, {IMG_SIZE}px images, batch size {BATCH_SIZE}")
    print(f"Training on {train_generator.samples} images - Expected time: 20-40 minutes")
    print("This should take ~15-30 minutes (optimized for speed)...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    if test_generator:
        test_loss, test_accuracy = model.evaluate(test_generator, verbose=1)
        print(f"Test Accuracy: {test_accuracy:.4f}")
    
    print(f"Model saved to {MODEL_DIR}/")

if __name__ == '__main__':
    train_model()
