"""
LBP (Local Binary Patterns) Features Module
Detects texture discontinuities and cloning artifacts
"""

import numpy as np
from skimage.feature import local_binary_pattern
import cv2


def extract_lbp_features(gray_frame, radius=3, n_points=None, method='uniform'):
    """
    Extract LBP features from a grayscale frame.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        radius: int - Radius of circular pattern (default: 3)
        n_points: int - Number of points (default: 8 * radius)
        method: str - LBP method ('uniform', 'default', 'ror', 'var')
        
    Returns:
        lbp: numpy array of shape (H, W) - LBP features
    """
    if n_points is None:
        n_points = 8 * radius
    
    # Compute LBP
    lbp = local_binary_pattern(gray_frame, n_points, radius, method=method)
    
    # Normalize to 0-255 range
    lbp_normalized = cv2.normalize(lbp, None, 0, 255, cv2.NORM_MINMAX)
    lbp_normalized = np.uint8(lbp_normalized)
    
    return lbp_normalized


def batch_extract_lbp(gray_frames, radius=3, n_points=None, method='uniform'):
    """
    Extract LBP features from multiple grayscale frames.
    
    Args:
        gray_frames: numpy array of shape (N, H, W) - Grayscale images
        radius: int - Radius of circular pattern
        n_points: int - Number of points
        method: str - LBP method
        
    Returns:
        lbp_features: numpy array of shape (N, H, W) - LBP features
    """
    lbp_features = []
    
    for frame in gray_frames:
        lbp = extract_lbp_features(frame, radius, n_points, method)
        lbp_features.append(lbp)
    
    return np.array(lbp_features)


def extract_multi_scale_lbp(gray_frame):
    """
    Extract LBP features at multiple scales.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        multi_lbp: numpy array of shape (H, W, 3) - Multi-scale LBP features
    """
    # Extract LBP at different radii
    lbp1 = extract_lbp_features(gray_frame, radius=1, n_points=8)
    lbp2 = extract_lbp_features(gray_frame, radius=2, n_points=16)
    lbp3 = extract_lbp_features(gray_frame, radius=3, n_points=24)
    
    # Stack into multi-scale features
    multi_lbp = np.stack([lbp1, lbp2, lbp3], axis=-1)
    
    return multi_lbp


def detect_cloning_artifacts(gray_frame):
    """
    Detect cloning artifacts using LBP pattern analysis.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        cloning_score: float - Score indicating potential cloning
    """
    # Extract LBP features
    lbp = extract_lbp_features(gray_frame)
    
    # Calculate histogram
    hist, _ = np.histogram(lbp.ravel(), bins=256, range=(0, 256))
    
    # Normalize histogram
    hist = hist.astype(float) / hist.sum()
    
    # High uniformity in LBP patterns can indicate cloning
    # Calculate entropy (lower entropy = more uniform = potential cloning)
    hist_nonzero = hist[hist > 0]
    entropy = -np.sum(hist_nonzero * np.log2(hist_nonzero))
    
    # Inverse entropy as cloning score (higher = more suspicious)
    max_entropy = np.log2(256)
    cloning_score = (max_entropy - entropy) / max_entropy * 100
    
    return cloning_score


if __name__ == "__main__":
    # Test the function
    print("Testing LBP Features...")
    
    # Create a dummy grayscale frame
    test_frame = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Extract LBP features
    lbp = extract_lbp_features(test_frame)
    multi_lbp = extract_multi_scale_lbp(test_frame)
    cloning_score = detect_cloning_artifacts(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"LBP shape: {lbp.shape}")
    print(f"Multi-scale LBP shape: {multi_lbp.shape}")
    print(f"Cloning score: {cloning_score:.2f}%")
    print("[OK] LBP features working!")
