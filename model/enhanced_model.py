"""
Enhanced Video Forgery Detection Model
Combines multi-feature extraction with ResNet50 and CNN classifier
"""

import numpy as np
from keras.models import Model
from keras.layers import (Input, Conv2D, MaxPooling2D, Flatten, Dense, 
                          Dropout, GlobalAveragePooling2D, BatchNormalization)
from keras.applications import ResNet50
from keras.optimizers import Adam


def build_enhanced_model(input_shape=(240, 320, 12), num_classes=1):
    """
    Build enhanced forgery detection model with multi-feature input.
    
    Args:
        input_shape: tuple - Input shape (H, W, 12 channels)
        num_classes: int - Number of output classes (1 for binary)
        
    Returns:
        model: Keras Model - Complete model
    """
    # Input layer (12 channels)
    inputs = Input(shape=input_shape, name='multi_feature_input')
    
    # Reduce 12 channels to 3 for ResNet50 compatibility
    x = Conv2D(64, (3, 3), padding='same', activation='relu', name='channel_reduction_1')(inputs)
    x = BatchNormalization()(x)
    x = Conv2D(32, (3, 3), padding='same', activation='relu', name='channel_reduction_2')(x)
    x = BatchNormalization()(x)
    x = Conv2D(3, (1, 1), padding='same', activation='relu', name='channel_reduction_3')(x)
    
    # ResNet50 base (pre-trained on ImageNet)
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(240, 320, 3)
    )
    
    # Freeze ResNet50 layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Apply ResNet50
    x = base_model(x)
    
    # Explicit MaxPooling2D (2×2)
    x = MaxPooling2D(pool_size=(2, 2), strides=2, name='max_pooling_explicit')(x)
    
    # Global Average Pooling
    x = GlobalAveragePooling2D(name='global_avg_pooling')(x)
    
    # Dense layers (CNN Classifier)
    x = Dense(512, activation='relu', name='dense_1')(x)
    x = Dropout(0.5, name='dropout_1')(x)
    
    x = Dense(256, activation='relu', name='dense_2')(x)
    x = Dropout(0.3, name='dropout_2')(x)
    
    x = Dense(128, activation='relu', name='dense_3')(x)
    x = Dropout(0.2, name='dropout_3')(x)
    
    # Output layer
    if num_classes == 1:
        # Binary classification
        outputs = Dense(1, activation='sigmoid', name='output_binary')(x)
    else:
        # Multi-class classification
        outputs = Dense(num_classes, activation='softmax', name='output_multiclass')(x)
    
    # Create model
    model = Model(inputs=inputs, outputs=outputs, name='enhanced_forgery_detector')
    
    return model


def build_active_passive_model(input_shape=(240, 320, 12)):
    """
    Build model for Active vs Passive forgery classification.
    
    Args:
        input_shape: tuple - Input shape (H, W, 12 channels)
        
    Returns:
        model: Keras Model - Model with 3 classes (Authentic, Active, Passive)
    """
    # Use the same architecture but with 3 output classes
    model = build_enhanced_model(input_shape=input_shape, num_classes=3)
    return model


def compile_model(model, learning_rate=0.0001):
    """
    Compile the model with optimizer and loss function.

    Args:
        model: Keras Model - Model to compile
        learning_rate: float - Learning rate for optimizer

    Returns:
        model: Compiled Keras Model
    """
    # Determine loss function based on model output shape
    output_shape = model.output_shape

    if output_shape[-1] == 1:
        # Binary classification
        loss = 'binary_crossentropy'
        metrics = ['accuracy']
    else:
        # Multi-class classification
        loss = 'categorical_crossentropy'
        metrics = ['accuracy']

    # Compile
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss=loss,
        metrics=metrics
    )

    return model


if __name__ == "__main__":
    # Test model creation
    print("Testing Enhanced Model Architecture...")
    
    # Build binary classification model
    print("\n1. Building binary classification model...")
    binary_model = build_enhanced_model(input_shape=(240, 320, 12), num_classes=1)
    binary_model = compile_model(binary_model)
    
    print(f"✅ Binary model created!")
    print(f"   Input shape: {binary_model.input_shape}")
    print(f"   Output shape: {binary_model.output_shape}")
    print(f"   Total parameters: {binary_model.count_params():,}")
    
    # Build active/passive classification model
    print("\n2. Building active/passive classification model...")
    active_passive_model = build_active_passive_model(input_shape=(240, 320, 12))
    active_passive_model = compile_model(active_passive_model)
    
    print(f"✅ Active/Passive model created!")
    print(f"   Input shape: {active_passive_model.input_shape}")
    print(f"   Output shape: {active_passive_model.output_shape}")
    print(f"   Total parameters: {active_passive_model.count_params():,}")
    
    # Print model summary
    print("\n3. Model Summary:")
    binary_model.summary()
