"""
Feature Combiner Module
Combines all 7 feature extraction methods into a single multi-channel tensor
"""

import numpy as np
import cv2
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from preprocessing.grayscale_conversion import convert_to_grayscale
from preprocessing.canny_edge_detection import apply_canny_edge
from feature_extraction.frame_difference import batch_frame_difference
from feature_extraction.dct_features import extract_dct_features
from feature_extraction.dwt_features import extract_dwt_features, resize_dwt_to_original
from feature_extraction.lbp_features import extract_lbp_features
from feature_extraction.binarization import apply_binarization
from feature_extraction.morphology import extract_morphology_features
from feature_extraction.eigen_vectors import extract_eigen_features


def extract_all_features(rgb_frame):
    """
    Extract all 7 types of features from a single RGB frame.
    
    Args:
        rgb_frame: numpy array of shape (H, W, 3) - RGB image
        
    Returns:
        combined_features: numpy array of shape (H, W, 12) - Combined features
    """
    h, w = rgb_frame.shape[:2]
    
    # Step 1: Convert to grayscale
    gray = convert_to_grayscale(rgb_frame)
    
    # Step 2: Extract features
    # Feature 1: Grayscale (1 channel)
    gray_feat = gray
    
    # Feature 2: Canny edges (1 channel)
    canny = apply_canny_edge(gray)
    
    # Feature 3: DCT (1 channel)
    dct = extract_dct_features(gray)
    
    # Feature 4: DWT (4 channels) - resize to original size
    dwt = extract_dwt_features(gray)
    dwt_resized = resize_dwt_to_original(dwt, (h, w))
    
    # Feature 5: LBP (1 channel)
    lbp = extract_lbp_features(gray)
    
    # Feature 6: Binarization (1 channel)
    binary = apply_binarization(gray, method='otsu')
    
    # Feature 7: Morphology (4 channels) - but we'll use just opening for now
    morph = extract_morphology_features(binary)
    morph_opening = morph[:, :, 2]  # Use opening channel
    
    # Feature 8: Eigen vectors (1 channel)
    eigen = extract_eigen_features(gray)
    
    # Combine all features
    # Total: 1 + 1 + 1 + 4 + 1 + 1 + 1 + 1 = 11 channels
    # We need 12, so let's add erosion from morphology
    morph_erosion = morph[:, :, 0]
    
    combined = np.stack([
        gray_feat,      # Channel 0: Grayscale
        canny,          # Channel 1: Edges
        dct,            # Channel 2: DCT
        dwt_resized[:, :, 0],  # Channel 3: DWT - Approximation
        dwt_resized[:, :, 1],  # Channel 4: DWT - Horizontal
        dwt_resized[:, :, 2],  # Channel 5: DWT - Vertical
        dwt_resized[:, :, 3],  # Channel 6: DWT - Diagonal
        lbp,            # Channel 7: LBP
        binary,         # Channel 8: Binary
        morph_opening,  # Channel 9: Morphology Opening
        morph_erosion,  # Channel 10: Morphology Erosion
        eigen           # Channel 11: Eigen
    ], axis=-1)
    
    return combined


def batch_extract_all_features(rgb_frames):
    """
    Extract all features from multiple RGB frames.
    
    Args:
        rgb_frames: numpy array of shape (N, H, W, 3) - RGB images
        
    Returns:
        all_features: numpy array of shape (N, H, W, 12) - Combined features
    """
    all_features = []
    
    print(f"Extracting features from {len(rgb_frames)} frames...")
    for i, frame in enumerate(rgb_frames):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(rgb_frames)} frames...")
        
        features = extract_all_features(frame)
        all_features.append(features)
    
    print("✅ Feature extraction complete!")
    return np.array(all_features)


def add_frame_difference_feature(features_sequence):
    """
    Add frame difference as temporal feature.
    This modifies the first channel (grayscale) with frame difference info.
    
    Args:
        features_sequence: numpy array of shape (N, H, W, 12) - Feature sequence
        
    Returns:
        enhanced_features: numpy array of shape (N, H, W, 12) - With temporal info
    """
    # Extract grayscale channel
    gray_frames = features_sequence[:, :, :, 0]
    
    # Compute frame differences
    frame_diffs = batch_frame_difference(gray_frames)
    
    # Replace or blend with original grayscale
    # Let's blend: 70% original + 30% frame difference
    enhanced = features_sequence.copy()
    for i in range(len(enhanced)):
        enhanced[i, :, :, 0] = (0.7 * gray_frames[i] + 0.3 * frame_diffs[i]).astype(np.uint8)
    
    return enhanced


if __name__ == "__main__":
    # Test the function
    print("Testing Feature Combiner...")
    
    # Create a dummy RGB frame
    test_frame = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)
    
    # Extract all features
    combined = extract_all_features(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"Combined features shape: {combined.shape}")
    print(f"Number of channels: {combined.shape[-1]}")
    print("\nChannel breakdown:")
    print("  0: Grayscale")
    print("  1: Canny Edges")
    print("  2: DCT")
    print("  3-6: DWT (4 channels)")
    print("  7: LBP")
    print("  8: Binary")
    print("  9-10: Morphology (2 channels)")
    print("  11: Eigen")
    print("✅ Feature combiner working!")
