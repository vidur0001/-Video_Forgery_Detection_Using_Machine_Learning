"""
Frame Difference Module
Detects temporal inconsistencies and active forgeries
"""

import cv2
import numpy as np


def compute_frame_difference(frame1, frame2):
    """
    Compute absolute difference between two consecutive frames.
    
    Args:
        frame1: numpy array - First frame (grayscale)
        frame2: numpy array - Second frame (grayscale)
        
    Returns:
        diff: numpy array - Absolute difference
    """
    diff = cv2.absdiff(frame1, frame2)
    return diff


def batch_frame_difference(frames):
    """
    Compute frame differences for a sequence of frames.
    For first frame, use zeros as there's no previous frame.
    
    Args:
        frames: numpy array of shape (N, H, W) - Sequence of grayscale frames
        
    Returns:
        diffs: numpy array of shape (N, H, W) - Frame differences
    """
    diffs = []
    
    # First frame: no previous frame, so use zeros
    first_diff = np.zeros_like(frames[0])
    diffs.append(first_diff)
    
    # Compute differences for remaining frames
    for i in range(1, len(frames)):
        diff = compute_frame_difference(frames[i-1], frames[i])
        diffs.append(diff)
    
    return np.array(diffs)


def temporal_difference_score(frames):
    """
    Compute temporal difference score for a sequence.
    Higher score indicates more temporal inconsistency (potential forgery).
    
    Args:
        frames: numpy array of shape (N, H, W) - Sequence of frames
        
    Returns:
        score: float - Average temporal difference
    """
    diffs = batch_frame_difference(frames)
    score = np.mean(diffs)
    return score


def detect_temporal_forgery(frames, threshold=30):
    """
    Detect potential temporal forgery based on frame differences.
    
    Args:
        frames: numpy array of shape (N, H, W) - Sequence of frames
        threshold: float - Threshold for forgery detection
        
    Returns:
        is_forged: bool - True if temporal forgery detected
        score: float - Temporal difference score
    """
    score = temporal_difference_score(frames)
    is_forged = score > threshold
    
    return is_forged, score


if __name__ == "__main__":
    # Test the function
    print("Testing Frame Difference...")
    
    # Create dummy frames
    frame1 = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    frame2 = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Compute difference
    diff = compute_frame_difference(frame1, frame2)
    
    # Test batch processing
    frames = np.random.randint(0, 256, (10, 240, 320), dtype=np.uint8)
    diffs = batch_frame_difference(frames)
    
    print(f"Single diff shape: {diff.shape}")
    print(f"Batch diffs shape: {diffs.shape}")
    print(f"Temporal score: {temporal_difference_score(frames):.2f}")
    print("✅ Frame difference working!")
