"""
Binarization Module
Detects shape and structure inconsistencies
"""

import cv2
import numpy as np


def apply_binarization(gray_frame, threshold=127, method='simple'):
    """
    Apply binarization to a grayscale frame.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        threshold: int - Threshold value (0-255)
        method: str - Binarization method ('simple', 'otsu', 'adaptive')
        
    Returns:
        binary: numpy array of shape (H, W) - Binary image
    """
    if method == 'simple':
        # Simple thresholding
        _, binary = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    
    elif method == 'otsu':
        # Otsu's thresholding (automatic threshold selection)
        _, binary = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    elif method == 'adaptive':
        # Adaptive thresholding (local threshold)
        binary = cv2.adaptiveThreshold(
            gray_frame, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return binary


def batch_binarize(gray_frames, threshold=127, method='simple'):
    """
    Apply binarization to multiple grayscale frames.
    
    Args:
        gray_frames: numpy array of shape (N, H, W) - Grayscale images
        threshold: int - Threshold value
        method: str - Binarization method
        
    Returns:
        binary_frames: numpy array of shape (N, H, W) - Binary images
    """
    binary_frames = []
    
    for frame in gray_frames:
        binary = apply_binarization(frame, threshold, method)
        binary_frames.append(binary)
    
    return np.array(binary_frames)


def multi_threshold_binarization(gray_frame):
    """
    Apply multiple thresholding methods and stack results.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        multi_binary: numpy array of shape (H, W, 3) - Multi-threshold binary
    """
    # Apply different methods
    binary_simple = apply_binarization(gray_frame, method='simple')
    binary_otsu = apply_binarization(gray_frame, method='otsu')
    binary_adaptive = apply_binarization(gray_frame, method='adaptive')
    
    # Stack into 3-channel feature map
    multi_binary = np.stack([binary_simple, binary_otsu, binary_adaptive], axis=-1)
    
    return multi_binary


def detect_shape_inconsistency(gray_frame):
    """
    Detect shape inconsistencies using binary analysis.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        inconsistency_score: float - Score indicating shape inconsistency
    """
    # Apply Otsu's binarization
    binary = apply_binarization(gray_frame, method='otsu')
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return 0.0
    
    # Analyze contour properties
    areas = [cv2.contourArea(cnt) for cnt in contours]
    perimeters = [cv2.arcLength(cnt, True) for cnt in contours]
    
    # Calculate circularity for each contour
    circularities = []
    for area, perimeter in zip(areas, perimeters):
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)
            circularities.append(circularity)
    
    if len(circularities) == 0:
        return 0.0
    
    # High variance in circularity indicates shape inconsistency
    inconsistency_score = np.std(circularities) * 100
    
    return inconsistency_score


if __name__ == "__main__":
    # Test the function
    print("Testing Binarization...")
    
    # Create a dummy grayscale frame
    test_frame = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Apply binarization
    binary_simple = apply_binarization(test_frame, method='simple')
    binary_otsu = apply_binarization(test_frame, method='otsu')
    binary_adaptive = apply_binarization(test_frame, method='adaptive')
    multi_binary = multi_threshold_binarization(test_frame)
    inconsistency = detect_shape_inconsistency(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"Binary (simple) shape: {binary_simple.shape}")
    print(f"Binary (Otsu) shape: {binary_otsu.shape}")
    print(f"Binary (adaptive) shape: {binary_adaptive.shape}")
    print(f"Multi-binary shape: {multi_binary.shape}")
    print(f"Shape inconsistency: {inconsistency:.2f}")
    print("[OK] Binarization working!")
