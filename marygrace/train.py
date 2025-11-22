"""
Train model for marygrace (tabular data)
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
NUM_CLASSES = 3

def load_data():
    """Load and preprocess data"""
    # Find CSV file
    csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("No CSV file found in " + DATA_DIR)
    
    df = pd.read_csv(os.path.join(DATA_DIR, csv_files[0]))
    
    # Auto-detect target column (common names)
    target_cols = ['target', 'label', 'class', 'outcome', 'DEATH_EVENT', 'stroke', 
                   'diagnosis', 'fetal_health', 'level', 'species', 'drug', 'y']
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
    # marygrace has numeric values (1, 2, 3) that need to be 0-indexed
    if y.dtype == 'object':
        y = pd.Categorical(y).codes
    elif y.dtype in ['int64', 'float64']:
        # Convert to 0-indexed if values start at 1
        y_min = y.min()
        if y_min > 0:
            y = y - y_min  # Convert 1,2,3 to 0,1,2
    
    # Auto-detect number of classes (handle both pandas Series and numpy arrays)
    if hasattr(y, 'unique'):
        num_classes = len(y.unique())
    else:
        num_classes = len(np.unique(y))
    print(f"Detected {num_classes} classes in data (values: {sorted(np.unique(y))})")
    
    return X, y, num_classes

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
        print("✓ Model already exists at " + MODEL_PATH)
        print("Skipping training. Delete the model file to retrain.")
        return
    
    print("Loading data...")
    X, y, num_classes = load_data()
    
    # Update NUM_CLASSES based on actual data
    global NUM_CLASSES
    NUM_CLASSES = num_classes
    print(f"Using {NUM_CLASSES} classes (auto-detected from data)")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    print("Training samples: " + str(len(X_train)) + ", Test samples: " + str(len(X_test)))
    print("Features: " + str(X_train.shape[1]) + ", Classes: " + str(NUM_CLASSES))
    
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
        ),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1)
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
    print("Test Accuracy: {:.4f}".format(test_accuracy))
    
    # Save final model
    model.save(os.path.join(MODEL_DIR, 'best_model.h5'))
    print("\nModel saved to " + MODEL_DIR + "/")

if __name__ == '__main__':
    train_model()
