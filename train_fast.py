"""
FAST TRAINING - Lightweight version
Trains in 10-15 minutes with good accuracy

Usage:
    python train_fast.py
"""

import os
import sys
import numpy as np
import cv2
from pathlib import Path
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.feature_combiner import extract_all_features
from model.enhanced_model import build_enhanced_model, compile_model

def load_videos_fast(folder_path, label, max_videos=10, frames_per_video=5):
    """Load videos quickly - fewer videos, fewer frames."""
    print(f"\nLoading from: {folder_path}")

    video_files = list(Path(folder_path).glob("*.mp4"))[:max_videos]

    print(f"   Found {len(video_files)} videos (taking first {max_videos})")

    all_features = []
    all_labels = []

    for i, video_path in enumerate(video_files):
        print(f"   Processing {i+1}/{len(video_files)}: {video_path.name}")

        cap = cv2.VideoCapture(str(video_path))

        frame_count = 0
        while cap.isOpened() and frame_count < frames_per_video:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize to 240x320
            frame_resized = cv2.resize(frame, (320, 240))

            # Extract features
            features = extract_all_features(frame_resized)
            all_features.append(features)
            all_labels.append(label)

            frame_count += 1

        cap.release()

    print(f"   Extracted {len(all_features)} frames")

    return np.array(all_features), np.array(all_labels)

def main():
    """Fast training."""
    print("\n" + "=" * 70)
    print(" " * 15 + "FAST TRAINING MODE")
    print(" " * 12 + "(10-15 minutes, Good Accuracy)")
    print("=" * 70)

    # Load LESS data for faster training
    print("\nLoading FAKE videos...")
    X_fake, Y_fake = load_videos_fast("SDFVD/SDFVD/videos_fake", label=1,
                                       max_videos=15, frames_per_video=4)

    print("\nLoading REAL videos...")
    X_real, Y_real = load_videos_fast("SDFVD/SDFVD/videos_real", label=0,
                                       max_videos=15, frames_per_video=4)

    # Combine
    X = np.concatenate([X_fake, X_real], axis=0)
    Y = np.concatenate([Y_fake, Y_real], axis=0)

    print(f"\nDataset: {len(X)} samples ({np.sum(Y==1)} fake, {np.sum(Y==0)} real)")

    # Shuffle
    indices = np.random.permutation(len(X))
    X = X[indices]
    Y = Y[indices]

    # Split
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42, stratify=Y
    )

    print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")

    # Build model
    print("\nBuilding model...")
    model = build_enhanced_model(input_shape=(240, 320, 12))
    model = compile_model(model, learning_rate=0.001)  # Higher learning rate

    # Train FASTER
    print("\nTraining (10 epochs, this will take ~10-15 min)...")
    print("=" * 70)

    history = model.fit(
        X_train,
        Y_train,
        validation_data=(X_test, Y_test),
        epochs=10,  # Fewer epochs
        batch_size=8,  # Smaller batch = faster
        verbose=1
    )

    # Evaluate
    test_loss, test_acc = model.evaluate(X_test, Y_test, verbose=0)

    print("\n" + "=" * 70)
    print(" " * 20 + "TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\nTest Accuracy: {test_acc * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")

    # Save
    model.save("forgery_model_enhanced.keras")

    print(f"\nModel saved: forgery_model_enhanced.keras")
    print(f"\nTest it:")
    print(f"   python main.py SDFVD/SDFVD/videos_fake/vs1.mp4")
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
