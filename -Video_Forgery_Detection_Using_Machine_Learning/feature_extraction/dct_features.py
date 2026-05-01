"""
DCT (Discrete Cosine Transform) Features Module
Detects compression artifacts and JPEG forgery traces
"""

import cv2
import numpy as np


def extract_dct_features(gray_frame):
    """
    Extract DCT features from a grayscale frame.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        dct_features: numpy array of shape (H, W) - DCT coefficients
    """
    # Convert to float32 for DCT
    float_frame = np.float32(gray_frame)
    
    # Apply DCT
    dct = cv2.dct(float_frame)
    
    # Normalize to 0-255 range for consistency
    dct_normalized = cv2.normalize(dct, None, 0, 255, cv2.NORM_MINMAX)
    dct_normalized = np.uint8(dct_normalized)
    
    return dct_normalized


def batch_extract_dct(gray_frames):
    """
    Extract DCT features from multiple grayscale frames.
    
    Args:
        gray_frames: numpy array of shape (N, H, W) - Grayscale images
        
    Returns:
        dct_features: numpy array of shape (N, H, W) - DCT features
    """
    dct_features = []
    
    for frame in gray_frames:
        dct = extract_dct_features(frame)
        dct_features.append(dct)
    
    return np.array(dct_features)


def extract_dct_blocks(gray_frame, block_size=8):
    """
    Extract DCT features in blocks (similar to JPEG compression).
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        block_size: int - Size of DCT blocks (default: 8 for JPEG)
        
    Returns:
        dct_blocks: numpy array - DCT coefficients for blocks
    """
    h, w = gray_frame.shape
    dct_blocks = np.zeros_like(gray_frame, dtype=np.float32)
    
    # Process in blocks
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            block = gray_frame[i:i+block_size, j:j+block_size]
            block_float = np.float32(block)
            
            # Apply DCT to block
            dct_block = cv2.dct(block_float)
            dct_blocks[i:i+block_size, j:j+block_size] = dct_block
    
    # Normalize
    dct_normalized = cv2.normalize(dct_blocks, None, 0, 255, cv2.NORM_MINMAX)
    dct_normalized = np.uint8(dct_normalized)
    
    return dct_normalized


def detect_compression_artifacts(gray_frame):
    """
    Detect compression artifacts using DCT analysis.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        artifact_score: float - Score indicating compression artifacts
    """
    # Extract DCT features
    dct = extract_dct_features(gray_frame)
    
    # High-frequency components indicate artifacts
    # Take bottom-right quadrant (high frequencies)
    h, w = dct.shape
    high_freq = dct[h//2:, w//2:]
    
    # Calculate artifact score
    artifact_score = np.mean(high_freq)
    
    return artifact_score


if __name__ == "__main__":
    # Test the function
    print("Testing DCT Features...")
    
    # Create a dummy grayscale frame
    test_frame = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Extract DCT features
    dct = extract_dct_features(test_frame)
    dct_blocks = extract_dct_blocks(test_frame)
    artifact_score = detect_compression_artifacts(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"DCT shape: {dct.shape}")
    print(f"DCT blocks shape: {dct_blocks.shape}")
    print(f"Artifact score: {artifact_score:.2f}")
    print("[OK] DCT features working!")
