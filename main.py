"""
VIDEO FORGERY DETECTION SYSTEM
Main execution file for final evaluation

Usage:
    python main.py path/to/video.mp4

Example:
    python main.py test_video.mp4
    python main.py C:\\Videos\\sample.avi
"""

import sys
import os
import time
import numpy as np
import cv2
from tensorflow import keras

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.feature_combiner import extract_all_features


def print_header():
    """Print system header."""
    print("\n" + "=" * 70)
    print(" " * 15 + "VIDEO FORGERY DETECTION SYSTEM")
    print(" " * 10 + "7-Feature Multi-Modal Analysis + ResNet50")
    print("=" * 70)


def load_model():
    """Load pre-trained ResNet50 model."""
    model_path = "forgery_model_enhanced.keras"

    if not os.path.exists(model_path):
        print("\nERROR: Trained model not found!")
        print(f"   Expected location: {model_path}")
        print("\nSOLUTION: Train the model first:")
        print("   python train_fast.py")
        print("\n   This will take 10-15 minutes (one-time setup)")
        sys.exit(1)

    print("\nLoading pre-trained model...")
    print("   Model: ResNet50 (24.8M parameters)")
    model = keras.models.load_model(model_path)
    print("   Model loaded successfully!")
    return model


def extract_features(video_path):
    """Extract 7-method features from video."""
    print(f"\nProcessing Video: {os.path.basename(video_path)}")
    print("-" * 70)

    # Check if file exists
    if not os.path.exists(video_path):
        print(f"ERROR: Video file not found!")
        print(f"   Path: {video_path}")
        sys.exit(1)

    # Read video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video file!")
        print(f"   Supported formats: MP4, AVI, MOV, MKV")
        sys.exit(1)

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame to 240x320 (model's expected input size)
        frame_resized = cv2.resize(frame, (320, 240))
        frames.append(frame_resized)
    cap.release()

    if len(frames) == 0:
        print("ERROR: No frames extracted from video!")
        sys.exit(1)

    print(f"   Total Frames: {len(frames)}")
    print(f"   Resolution: {frames[0].shape[1]}x{frames[0].shape[0]}")

    # Extract features using the feature combiner
    print("\nExtracting Features (7 Methods):")
    all_features = []

    for i, frame in enumerate(frames):
        # Use the existing extract_all_features function
        combined = extract_all_features(frame)
        all_features.append(combined)

        # Progress indicator
        if (i + 1) % 20 == 0 or (i + 1) == len(frames):
            print(f"   Progress: {i + 1}/{len(frames)} frames", end="\r")

    print(f"\n   Feature extraction complete!")
    print(f"   Output shape: {np.array(all_features).shape} (12-channel tensor)")

    return np.array(all_features)


def predict(model, features):
    """Predict if video is forged or authentic."""
    print("\nRunning Deep Learning Analysis...")
    print("   Network: ResNet50 (50 layers)")
    print("   Processing 12-channel feature tensor...")

    predictions = model.predict(features, verbose=0)
    avg_prediction = np.mean(predictions)

    is_forged = avg_prediction >= 0.5
    confidence = avg_prediction * 100 if is_forged else (1 - avg_prediction) * 100

    return is_forged, confidence


def print_results(video_path, is_forged, confidence, elapsed_time):
    """Print final results."""
    print("\n" + "=" * 70)
    print(" " * 25 + "ANALYSIS RESULTS")
    print("=" * 70)

    print(f"\nVideo File: {os.path.basename(video_path)}")
    print(f"Full Path: {os.path.abspath(video_path)}")

    print(f"\nClassification: ", end="")
    if is_forged:
        print("FORGED")
    else:
        print("AUTHENTIC")

    print(f"Confidence: {confidence:.2f}%")
    print(f"Processing Time: {elapsed_time:.2f} seconds")

    print("\nAnalysis Methodology:")
    print("   - Frame Difference (Temporal Analysis)")
    print("   - DCT (Compression Artifacts)")
    print("   - DWT (Multi-Resolution Texture)")
    print("   - LBP (Local Binary Patterns)")
    print("   - Binarization (Shape Analysis)")
    print("   - Morphology (Structural Patterns)")
    print("   - Eigen Vectors (Statistical Analysis)")

    print("\nDeep Learning Model: ResNet50 (24.8M parameters)")
    print("=" * 70 + "\n")


def main():
    """Main execution function."""
    # Print header
    print_header()

    # Check command line arguments
    if len(sys.argv) < 2:
        print("\nERROR: No video file provided!")
        print("\nUSAGE:")
        print("   python main.py <video_path>")
        print("\nEXAMPLES:")
        print("   python main.py test_video.mp4")
        print("   python main.py C:\\Videos\\sample.avi")
        print("   python main.py /path/to/video.mov")
        print("\n" + "=" * 70 + "\n")
        sys.exit(1)

    video_path = sys.argv[1]
    start_time = time.time()

    # Step 1: Load model
    model = load_model()

    # Step 2: Extract features
    features = extract_features(video_path)

    # Step 3: Predict
    is_forged, confidence = predict(model, features)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Step 4: Display results
    print_results(video_path, is_forged, confidence, elapsed_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUNEXPECTED ERROR: {str(e)}")
        print("\nIf problem persists, please check:")
        print("   1. Video file is valid and not corrupted")
        print("   2. All dependencies are installed: pip install -r requirements.txt")
        print("   3. Model file exists: forgery_model_enhanced.keras")
        sys.exit(1)
