"""
Video Forgery Prediction Script
Predicts if a video is FORGED or AUTHENTIC using the trained model
"""

import numpy as np
import cv2
import os
import sys
from keras.models import load_model

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from model.feature_combiner import extract_all_features


def extract_frames_from_video(video_path, max_frames=100):
    """
    Extract frames from video file.
    
    Args:
        video_path: str - Path to video file
        max_frames: int - Maximum frames to extract
        
    Returns:
        frames: list - List of RGB frames
    """
    print(f"\n[*] Extracting frames from video...")

    if not os.path.exists(video_path):
        print(f"[X] Error: Video file not found: {video_path}")
        return None

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[X] Error: Cannot open video file: {video_path}")
        return None
    
    frames = []
    frame_count = 0
    
    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize to 240x320 if needed
        if frame.shape[:2] != (240, 320):
            frame = cv2.resize(frame, (320, 240))
        
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)
        frame_count += 1
    
    cap.release()

    print(f"[OK] Extracted {len(frames)} frames")
    return frames


def predict_video_forgery(video_path, model_path='forgery_model_enhanced.keras'):
    """
    Predict if a video is forged or authentic.
    
    Args:
        video_path: str - Path to video file
        model_path: str - Path to trained model
        
    Returns:
        result: str - "FORGED" or "AUTHENTIC"
        confidence: float - Confidence score (0-1)
    """
    print("\n" + "="*60)
    print("VIDEO FORGERY DETECTION")
    print("="*60)
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"\n[X] Error: Model file not found: {model_path}")
        print("Please train the model first using: python run_complete_pipeline.py")
        return None, None

    # Load model
    print(f"\n[*] Loading model from {model_path}...")
    model = load_model(model_path)
    print("[OK] Model loaded successfully!")
    
    # Extract frames
    frames = extract_frames_from_video(video_path, max_frames=50)
    if frames is None or len(frames) == 0:
        return None, None
    
    # Extract features from frames
    print(f"\n[*] Extracting features from {len(frames)} frames...")
    print("This may take a minute...")

    all_features = []
    for i, frame in enumerate(frames):
        if (i + 1) % 10 == 0:
            print(f"  Processed {i+1}/{len(frames)} frames...")

        features = extract_all_features(frame)
        all_features.append(features)

    features_array = np.array(all_features)
    print(f"[OK] Features extracted! Shape: {features_array.shape}")

    # Make predictions
    print(f"\n[*] Making predictions...")
    predictions = model.predict(features_array, verbose=0)
    
    # Average predictions across all frames
    avg_prediction = np.mean(predictions)
    
    # Determine result
    if avg_prediction > 0.5:
        result = "FORGED"
        confidence = avg_prediction
    else:
        result = "AUTHENTIC"
        confidence = 1 - avg_prediction
    
    return result, confidence


def main():
    """Main function for command-line usage."""
    print("\n" + "="*60)
    print("VIDEO FORGERY DETECTION SYSTEM")
    print("="*60)
    
    # Get video path from user
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = input("\nEnter video file path: ").strip()
        # Remove quotes if present
        video_path = video_path.strip('"').strip("'")
    
    # Predict
    result, confidence = predict_video_forgery(video_path)
    
    if result is not None:
        # Display results
        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)
        print(f"[*] Video: {os.path.basename(video_path)}")
        print(f"[*] Result: {result}")
        print(f"[*] Confidence: {confidence*100:.2f}%")
        print("="*60)

        # Visual indicator
        if result == "FORGED":
            print("\n[X] WARNING: This video appears to be FORGED!")
        else:
            print("\n[OK] This video appears to be AUTHENTIC!")
    else:
        print("\n[X] Prediction failed!")


if __name__ == "__main__":
    main()
