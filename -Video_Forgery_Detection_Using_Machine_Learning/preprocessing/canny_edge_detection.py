"""
Canny Edge Detection Module
Detects edges in frames to identify unnatural boundaries from forgery
"""

import cv2
import numpy as np


def apply_canny_edge(gray_frame, threshold1=100, threshold2=200):
    """
    Apply Canny edge detection to a grayscale frame.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        threshold1: int - Lower threshold for edge detection (default: 100)
        threshold2: int - Upper threshold for edge detection (default: 200)
        
    Returns:
        edges: numpy array of shape (H, W) - Binary edge map
    """
    # Apply Canny edge detection
    edges = cv2.Canny(gray_frame, threshold1, threshold2)
    
    return edges


def batch_canny_edge(gray_frames, threshold1=100, threshold2=200):
    """
    Apply Canny edge detection to multiple grayscale frames.
    
    Args:
        gray_frames: numpy array of shape (N, H, W) or list of grayscale images
        threshold1: int - Lower threshold
        threshold2: int - Upper threshold
        
    Returns:
        edge_frames: numpy array of shape (N, H, W) - Edge maps
    """
    edge_frames = []
    
    for frame in gray_frames:
        edges = apply_canny_edge(frame, threshold1, threshold2)
        edge_frames.append(edges)
    
    return np.array(edge_frames)


def adaptive_canny(gray_frame, sigma=0.33):
    """
    Apply Canny edge detection with automatic threshold calculation.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        sigma: float - Sigma value for automatic threshold calculation
        
    Returns:
        edges: numpy array of shape (H, W) - Binary edge map
    """
    # Compute the median of the single channel pixel intensities
    v = np.median(gray_frame)
    
    # Apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(gray_frame, lower, upper)
    
    return edges


if __name__ == "__main__":
    # Test the function
    print("Testing Canny Edge Detection...")
    
    # Create a dummy grayscale frame
    test_frame = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Apply Canny edge detection
    edges = apply_canny_edge(test_frame)
    adaptive_edges = adaptive_canny(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"Output shape: {edges.shape}")
    print(f"Adaptive output shape: {adaptive_edges.shape}")
    print(f"Edge pixels detected: {np.sum(edges > 0)}")
    print("[OK] Canny edge detection working!")
