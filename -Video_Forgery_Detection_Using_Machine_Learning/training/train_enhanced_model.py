"""
Training Script for Enhanced Video Forgery Detection Model
"""

import numpy as np
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from model.enhanced_model import build_enhanced_model, compile_model
from model.feature_combiner import batch_extract_all_features
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt


def load_training_data(data_path=None):
    """
    Load training data (Xtrain and Ytrain).

    Args:
        data_path: str - Path to dataset directory

    Returns:
        Xtrain: numpy array - RGB frames
        Ytrain: numpy array - Labels
    """
    print("Loading training data...")

    if data_path is None:
        data_path = os.path.join(parent_dir, 'video_tampering_dataset')

    Xtrain_path = os.path.join(data_path, 'Xtrain.npy')
    Ytrain_path = os.path.join(data_path, 'Ytrain.npy')
    
    if not os.path.exists(Xtrain_path) or not os.path.exists(Ytrain_path):
        print(f"[ERROR] Data files not found in {data_path}")
        print("Please run generate_synthetic_data.py first!")
        return None, None
    
    Xtrain = np.load(Xtrain_path)
    Ytrain = np.load(Ytrain_path)
    
    print(f"[OK] Loaded {len(Xtrain)} training samples")
    print(f"   Frame shape: {Xtrain.shape}")
    print(f"   Labels shape: {Ytrain.shape}")
    
    return Xtrain, Ytrain


def preprocess_data(Xtrain, Ytrain, use_subset=None):
    """
    Preprocess training data by extracting multi-features.
    
    Args:
        Xtrain: numpy array - RGB frames
        Ytrain: numpy array - Labels
        use_subset: int - Use only subset of data (for quick testing)
        
    Returns:
        X_features: numpy array - Multi-channel features
        Y: numpy array - Labels
    """
    if use_subset is not None:
        print(f"Using subset of {use_subset} samples for quick testing...")
        Xtrain = Xtrain[:use_subset]
        Ytrain = Ytrain[:use_subset]
    
    print("\nExtracting multi-features from frames...")
    print("This may take a while...")
    
    X_features = batch_extract_all_features(Xtrain)
    
    print(f"\n[OK] Feature extraction complete!")
    print(f"   Features shape: {X_features.shape}")
    
    return X_features, Ytrain


def train_model(X_features, Y, epochs=20, batch_size=32, validation_split=0.2):
    """
    Train the enhanced model.
    
    Args:
        X_features: numpy array - Multi-channel features
        Y: numpy array - Labels
        epochs: int - Number of training epochs
        batch_size: int - Batch size
        validation_split: float - Validation split ratio
        
    Returns:
        model: Trained Keras model
        history: Training history
    """
    print("\nBuilding enhanced model...")
    model = build_enhanced_model(input_shape=X_features.shape[1:], num_classes=1)
    model = compile_model(model, learning_rate=0.0001)
    
    print("\nModel architecture:")
    model.summary()
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            'forgery_model_enhanced.keras',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    print(f"\nStarting training...")
    print(f"  Epochs: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Validation split: {validation_split}")
    
    history = model.fit(
        X_features, Y,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\n[OK] Training complete!")
    
    return model, history


def plot_training_history(history):
    """
    Plot training history (accuracy and loss).
    
    Args:
        history: Keras History object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
    print("[OK] Training history plot saved as 'training_history.png'")
    plt.show()


if __name__ == "__main__":
    print("="*60)
    print("ENHANCED VIDEO FORGERY DETECTION - TRAINING")
    print("="*60)
    
    # Load data
    Xtrain, Ytrain = load_training_data()
    
    if Xtrain is None:
        print("\n[ERROR] Cannot proceed without training data.")
        print("Run: python generate_small_synthetic_data.py")
        exit(1)
    
    # Preprocess (use subset for quick testing)
    # Change use_subset=100 to use_subset=None for full dataset
    X_features, Y = preprocess_data(Xtrain, Ytrain, use_subset=100)
    
    # Train model
    model, history = train_model(
        X_features, Y,
        epochs=10,  # Change to 20-30 for better results
        batch_size=16,  # Reduced for memory efficiency
        validation_split=0.2
    )
    
    # Plot results
    plot_training_history(history)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"Model saved as: forgery_model_enhanced.keras")
    print(f"Training plot saved as: training_history.png")
