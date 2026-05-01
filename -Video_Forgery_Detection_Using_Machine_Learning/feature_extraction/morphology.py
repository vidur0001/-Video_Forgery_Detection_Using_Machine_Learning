"""
Morphology Operations Module
Detects structural anomalies and noise patterns
"""

import cv2
import numpy as np


def apply_morphology(binary_frame, operation='all', kernel_size=5):
    """
    Apply morphological operations to a binary frame.
    
    Args:
        binary_frame: numpy array of shape (H, W) - Binary image
        operation: str - Operation type ('erosion', 'dilation', 'opening', 'closing', 'all')
        kernel_size: int - Size of morphological kernel
        
    Returns:
        result: numpy array or dict - Morphological operation result(s)
    """
    # Create kernel
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    if operation == 'erosion':
        return cv2.erode(binary_frame, kernel, iterations=1)
    
    elif operation == 'dilation':
        return cv2.dilate(binary_frame, kernel, iterations=1)
    
    elif operation == 'opening':
        return cv2.morphologyEx(binary_frame, cv2.MORPH_OPEN, kernel)
    
    elif operation == 'closing':
        return cv2.morphologyEx(binary_frame, cv2.MORPH_CLOSE, kernel)
    
    elif operation == 'gradient':
        return cv2.morphologyEx(binary_frame, cv2.MORPH_GRADIENT, kernel)
    
    elif operation == 'tophat':
        return cv2.morphologyEx(binary_frame, cv2.MORPH_TOPHAT, kernel)
    
    elif operation == 'blackhat':
        return cv2.morphologyEx(binary_frame, cv2.MORPH_BLACKHAT, kernel)
    
    elif operation == 'all':
        # Apply all major operations and return as dict
        results = {
            'erosion': cv2.erode(binary_frame, kernel, iterations=1),
            'dilation': cv2.dilate(binary_frame, kernel, iterations=1),
            'opening': cv2.morphologyEx(binary_frame, cv2.MORPH_OPEN, kernel),
            'closing': cv2.morphologyEx(binary_frame, cv2.MORPH_CLOSE, kernel)
        }
        return results
    
    else:
        raise ValueError(f"Unknown operation: {operation}")


def extract_morphology_features(binary_frame, kernel_size=5):
    """
    Extract morphological features as a multi-channel tensor.
    
    Args:
        binary_frame: numpy array of shape (H, W) - Binary image
        kernel_size: int - Size of morphological kernel
        
    Returns:
        morph_features: numpy array of shape (H, W, 4) - Morphological features
    """
    # Apply all operations
    results = apply_morphology(binary_frame, operation='all', kernel_size=kernel_size)
    
    # Stack into 4-channel feature map
    morph_features = np.stack([
        results['erosion'],
        results['dilation'],
        results['opening'],
        results['closing']
    ], axis=-1)
    
    return morph_features


def batch_extract_morphology(binary_frames, kernel_size=5):
    """
    Extract morphological features from multiple binary frames.
    
    Args:
        binary_frames: numpy array of shape (N, H, W) - Binary images
        kernel_size: int - Size of morphological kernel
        
    Returns:
        morph_features: numpy array of shape (N, H, W, 4) - Morphological features
    """
    morph_features = []
    
    for frame in binary_frames:
        morph = extract_morphology_features(frame, kernel_size)
        morph_features.append(morph)
    
    return np.array(morph_features)


def detect_structural_anomalies(binary_frame):
    """
    Detect structural anomalies using morphological analysis.
    
    Args:
        binary_frame: numpy array of shape (H, W) - Binary image
        
    Returns:
        anomaly_score: float - Score indicating structural anomalies
    """
    # Extract morphological features
    morph = extract_morphology_features(binary_frame)
    
    # Calculate differences between operations
    erosion = morph[:, :, 0]
    dilation = morph[:, :, 1]
    opening = morph[:, :, 2]
    closing = morph[:, :, 3]
    
    # Anomaly score based on structural differences
    diff1 = np.abs(erosion.astype(float) - dilation.astype(float))
    diff2 = np.abs(opening.astype(float) - closing.astype(float))
    
    anomaly_score = (np.mean(diff1) + np.mean(diff2)) / 2
    
    return anomaly_score


if __name__ == "__main__":
    # Test the function
    print("Testing Morphology Operations...")
    
    # Create a dummy binary frame
    test_frame = np.random.randint(0, 2, (240, 320), dtype=np.uint8) * 255
    
    # Apply morphology
    erosion = apply_morphology(test_frame, 'erosion')
    morph_features = extract_morphology_features(test_frame)
    anomaly = detect_structural_anomalies(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"Erosion shape: {erosion.shape}")
    print(f"Morphology features shape: {morph_features.shape}")
    print(f"Anomaly score: {anomaly:.2f}")
    print("✅ Morphology operations working!")
