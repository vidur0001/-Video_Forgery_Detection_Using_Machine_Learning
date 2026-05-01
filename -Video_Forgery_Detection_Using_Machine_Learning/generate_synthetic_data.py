"""
Generate synthetic training data for Video Forgery Detection
This creates dummy data with the same dimensions as the real dataset
"""

import numpy as np
import os

print("Generating synthetic training data...")
print("This will create fake video frames to test the model.\n")

# Create directory if it doesn't exist
os.makedirs('video_tampering_dataset', exist_ok=True)

# Dataset specifications
NUM_FRAMES = 6990  # Total frames (10 forged + 10 original videos)
HEIGHT = 240
WIDTH = 320
CHANNELS = 3

print(f"Creating {NUM_FRAMES} frames of size {HEIGHT}x{WIDTH}x{CHANNELS}...")

# Generate random image data (simulating video frames)
# Values between 0-255 (standard RGB range)
Xtrain = np.random.randint(0, 256, size=(NUM_FRAMES, HEIGHT, WIDTH, CHANNELS), dtype=np.uint8)

# Generate labels
# Approximately 50% forged (1) and 50% original (0)
num_forged = NUM_FRAMES // 2
num_original = NUM_FRAMES - num_forged

Ytrain = np.concatenate([
    np.ones(num_forged, dtype=np.float32),   # Forged frames
    np.zeros(num_original, dtype=np.float32)  # Original frames
])

# Shuffle to randomize
indices = np.random.permutation(NUM_FRAMES)
Xtrain = Xtrain[indices]
Ytrain = Ytrain[indices]

print(f"[OK] Generated Xtrain shape: {Xtrain.shape}")
print(f"[OK] Generated Ytrain shape: {Ytrain.shape}")
print(f"  - Forged frames: {np.sum(Ytrain == 1)}")
print(f"  - Original frames: {np.sum(Ytrain == 0)}")

# Save the data
print("\nSaving data...")
np.save('video_tampering_dataset/Xtrain.npy', Xtrain)
np.save('video_tampering_dataset/Ytrain.npy', Ytrain)

print("\n[OK] DONE! Synthetic data generated successfully!")
print(f"\nFiles created:")
print(f"  - video_tampering_dataset/Xtrain.npy ({Xtrain.nbytes / (1024**2):.2f} MB)")
print(f"  - video_tampering_dataset/Ytrain.npy ({Ytrain.nbytes / (1024**2):.2f} MB)")
print("\nYou can now proceed to Model_Training.ipynb!")
