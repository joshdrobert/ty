"""
Train model for josh (tabular data)
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
NUM_CLASSES = 2

def load_data():
    """Load and preprocess data"""
    # Find CSV file
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in {DATA_DIR}")
    
    df = pd.read_csv(os.path.join(DATA_DIR, csv_files[0]))
    
    # Auto-detect target column (common names)
    target_cols = ['target', 'label', 'class', 'outcome', 'DEATH_EVENT', 'stroke', 'diagnosis']
    target_col = None
    for col in target_cols:
        if col in df.columns:
            target_col = col
            break
    
    if target_col is None:
        # Use last column as target
        target_col = df.columns[-1]
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    # Handle categorical columns
    X = pd.get_dummies(X, drop_first=True)
    
    # Convert target to numeric if needed
    if y.dtype == 'object':
        y = pd.Categorical(y).codes
    
    return X, y

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
    # Skip if model already exists
    MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.h5')
    if os.path.exists(MODEL_PATH):
        print(f"✓ Model already exists at {MODEL_PATH}")
        print("Skipping training. Delete the model file to retrain.")
        return
    

    print("Loading data...")
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    print(f"Features: {X_train.shape[1]}, Classes: {NUM_CLASSES}")
    
    print("Building model...")
    model = build_model(X_train.shape[1])
    model.summary()
    
    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(
            os.path.join(MODEL_DIR, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.2,
        callbacks=callbacks,
        verbose=1
    )
    
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=1)
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    print(f"Model saved to {os.path.join(MODEL_DIR, 'best_model.h5')}")

if __name__ == '__main__':
    train_model()
