"""
Grayscale Conversion Module
Converts RGB frames to grayscale for feature extraction
"""

import cv2
import numpy as np


def convert_to_grayscale(frame):
    """
    Convert a single RGB frame to grayscale.
    
    Args:
        frame: numpy array of shape (H, W, 3) - RGB image
        
    Returns:
        gray: numpy array of shape (H, W) - Grayscale image
    """
    if len(frame.shape) == 2:
        # Already grayscale
        return frame
    
    if frame.shape[2] == 3:
        # RGB to Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    elif frame.shape[2] == 4:
        # RGBA to Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
    else:
        gray = frame[:, :, 0]  # Take first channel
    
    return gray


def batch_convert_to_grayscale(frames):
    """
    Convert multiple RGB frames to grayscale.
    
    Args:
        frames: numpy array of shape (N, H, W, 3) or list of RGB images
        
    Returns:
        gray_frames: numpy array of shape (N, H, W) - Grayscale images
    """
    gray_frames = []
    
    for frame in frames:
        gray = convert_to_grayscale(frame)
        gray_frames.append(gray)
    
    return np.array(gray_frames)


if __name__ == "__main__":
    # Test the function
    print("Testing Grayscale Conversion...")
    
    # Create a dummy RGB frame
    test_frame = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)
    
    # Convert to grayscale
    gray = convert_to_grayscale(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"Output shape: {gray.shape}")
    print(f"Output dtype: {gray.dtype}")
    print("[OK] Grayscale conversion working!")
