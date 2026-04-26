"""
Generate SMALL synthetic training data for quick testing
This creates a smaller dataset for faster training/testing
"""

import numpy as np
import os

print("Generating SMALL synthetic training data for quick testing...")
print("This creates only 1000 frames instead of 6990.\n")

# Create directory if it doesn't exist
os.makedirs('video_tampering_dataset', exist_ok=True)

# SMALLER Dataset specifications for testing
NUM_FRAMES = 1000  # Much smaller for quick testing
HEIGHT = 240
WIDTH = 320
CHANNELS = 3

print(f"Creating {NUM_FRAMES} frames of size {HEIGHT}x{WIDTH}x{CHANNELS}...")

# Generate random image data
Xtrain = np.random.randint(0, 256, size=(NUM_FRAMES, HEIGHT, WIDTH, CHANNELS), dtype=np.uint8)

# Generate labels (50% forged, 50% original)
num_forged = NUM_FRAMES // 2
num_original = NUM_FRAMES - num_forged

Ytrain = np.concatenate([
    np.ones(num_forged, dtype=np.float32),
    np.zeros(num_original, dtype=np.float32)
])

# Shuffle
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

print("\n[OK] DONE! SMALL synthetic data generated!")
print(f"\nFiles created:")
print(f"  - video_tampering_dataset/Xtrain.npy ({Xtrain.nbytes / (1024**2):.2f} MB)")
print(f"  - video_tampering_dataset/Ytrain.npy ({Ytrain.nbytes / (1024**2):.2f} MB)")
print("\n[*] This smaller dataset will train MUCH faster (good for testing)!")
print("You can now proceed to Model_Training.ipynb!")
