"""
DWT (Discrete Wavelet Transform) Features Module
Detects texture forgery and high-frequency artifacts
"""

import numpy as np
import pywt
import cv2


def extract_dwt_features(gray_frame, wavelet='haar'):
    """
    Extract DWT features from a grayscale frame.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        wavelet: str - Wavelet type (default: 'haar')
        
    Returns:
        dwt_features: numpy array of shape (H//2, W//2, 4) - DWT coefficients
    """
    # Apply 2D DWT
    coeffs = pywt.dwt2(gray_frame, wavelet)
    cA, (cH, cV, cD) = coeffs
    
    # Normalize each component to 0-255
    cA_norm = cv2.normalize(cA, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cH_norm = cv2.normalize(cH, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cV_norm = cv2.normalize(cV, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cD_norm = cv2.normalize(cD, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Stack into 4-channel feature map
    dwt_features = np.stack([cA_norm, cH_norm, cV_norm, cD_norm], axis=-1)
    
    return dwt_features


def batch_extract_dwt(gray_frames, wavelet='haar'):
    """
    Extract DWT features from multiple grayscale frames.
    
    Args:
        gray_frames: numpy array of shape (N, H, W) - Grayscale images
        wavelet: str - Wavelet type
        
    Returns:
        dwt_features: numpy array of shape (N, H//2, W//2, 4) - DWT features
    """
    dwt_features = []
    
    for frame in gray_frames:
        dwt = extract_dwt_features(frame, wavelet)
        dwt_features.append(dwt)
    
    return np.array(dwt_features)


def resize_dwt_to_original(dwt_features, target_shape):
    """
    Resize DWT features back to original frame size.
    
    Args:
        dwt_features: numpy array of shape (H//2, W//2, 4) - DWT coefficients
        target_shape: tuple (H, W) - Target shape
        
    Returns:
        resized: numpy array of shape (H, W, 4) - Resized DWT features
    """
    h, w = target_shape
    resized_channels = []
    
    for i in range(dwt_features.shape[-1]):
        channel = dwt_features[:, :, i]
        resized = cv2.resize(channel, (w, h), interpolation=cv2.INTER_LINEAR)
        resized_channels.append(resized)
    
    resized = np.stack(resized_channels, axis=-1)
    return resized


def detect_texture_forgery(gray_frame):
    """
    Detect texture forgery using DWT high-frequency analysis.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        forgery_score: float - Score indicating texture forgery
    """
    # Extract DWT features
    dwt = extract_dwt_features(gray_frame)
    
    # High-frequency components (cH, cV, cD) indicate texture anomalies
    high_freq = dwt[:, :, 1:]  # Skip cA (approximation)
    
    # Calculate forgery score based on high-frequency energy
    forgery_score = np.mean(high_freq)
    
    return forgery_score


if __name__ == "__main__":
    # Test the function
    print("Testing DWT Features...")
    
    # Create a dummy grayscale frame
    test_frame = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Extract DWT features
    dwt = extract_dwt_features(test_frame)
    resized_dwt = resize_dwt_to_original(dwt, (240, 320))
    forgery_score = detect_texture_forgery(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"DWT shape: {dwt.shape}")
    print(f"Resized DWT shape: {resized_dwt.shape}")
    print(f"Forgery score: {forgery_score:.2f}")
    print("[OK] DWT features working!")
