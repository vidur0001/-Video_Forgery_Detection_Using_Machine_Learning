"""
Eigen Vectors Module
Extracts statistical patterns and principal components
"""

import numpy as np
import cv2


def extract_eigen_features(gray_frame, num_components=10):
    """
    Extract eigen vector features from a grayscale frame using PCA.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        num_components: int - Number of principal components to extract
        
    Returns:
        eigen_image: numpy array of shape (H, W) - Reconstructed from top components
    """
    # Flatten the image
    h, w = gray_frame.shape
    flat_image = gray_frame.flatten().astype(np.float32)
    
    # Reshape for covariance computation
    # Use patches instead of full image for computational efficiency
    patch_size = 8
    patches = []
    
    for i in range(0, h - patch_size + 1, patch_size):
        for j in range(0, w - patch_size + 1, patch_size):
            patch = gray_frame[i:i+patch_size, j:j+patch_size]
            patches.append(patch.flatten())
    
    patches = np.array(patches, dtype=np.float32)
    
    # Compute mean and center the data
    mean_patch = np.mean(patches, axis=0)
    centered_patches = patches - mean_patch
    
    # Compute covariance matrix
    cov_matrix = np.cov(centered_patches.T)
    
    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # Sort by eigenvalues (descending)
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Take top components
    top_eigenvectors = eigenvectors[:, :num_components]
    
    # Project patches onto principal components
    projected = np.dot(centered_patches, top_eigenvectors)
    
    # Reconstruct patches
    reconstructed = np.dot(projected, top_eigenvectors.T) + mean_patch
    
    # Reshape back to image
    eigen_image = np.zeros((h, w), dtype=np.float32)
    patch_idx = 0
    
    for i in range(0, h - patch_size + 1, patch_size):
        for j in range(0, w - patch_size + 1, patch_size):
            if patch_idx < len(reconstructed):
                patch = reconstructed[patch_idx].reshape((patch_size, patch_size))
                eigen_image[i:i+patch_size, j:j+patch_size] = patch
                patch_idx += 1
    
    # Normalize to 0-255
    eigen_image = cv2.normalize(eigen_image, None, 0, 255, cv2.NORM_MINMAX)
    eigen_image = np.uint8(eigen_image)
    
    return eigen_image


def batch_extract_eigen(gray_frames, num_components=10):
    """
    Extract eigen features from multiple grayscale frames.
    
    Args:
        gray_frames: numpy array of shape (N, H, W) - Grayscale images
        num_components: int - Number of principal components
        
    Returns:
        eigen_features: numpy array of shape (N, H, W) - Eigen features
    """
    eigen_features = []
    
    for frame in gray_frames:
        eigen = extract_eigen_features(frame, num_components)
        eigen_features.append(eigen)
    
    return np.array(eigen_features)


def compute_eigen_energy(gray_frame):
    """
    Compute energy of eigenvalues (useful for forgery detection).
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        energy: float - Total energy of eigenvalues
    """
    # Flatten and compute covariance
    flat = gray_frame.flatten().astype(np.float32)
    
    # Use a subset for efficiency
    subset_size = min(1000, len(flat))
    subset = np.random.choice(flat, subset_size, replace=False)
    
    # Compute covariance
    cov = np.cov(subset.reshape(1, -1))
    
    # Compute eigenvalues
    eigenvalues = np.linalg.eigvalsh(cov)
    
    # Total energy
    energy = np.sum(eigenvalues)
    
    return energy


def detect_statistical_anomalies(gray_frame):
    """
    Detect statistical anomalies using eigen analysis.
    
    Args:
        gray_frame: numpy array of shape (H, W) - Grayscale image
        
    Returns:
        anomaly_score: float - Statistical anomaly score
    """
    # Extract eigen features
    eigen_image = extract_eigen_features(gray_frame)
    
    # Compute difference between original and reconstructed
    diff = cv2.absdiff(gray_frame, eigen_image)
    
    # Anomaly score = mean reconstruction error
    anomaly_score = np.mean(diff)
    
    return anomaly_score


if __name__ == "__main__":
    # Test the function
    print("Testing Eigen Vector Features...")
    
    # Create a dummy grayscale frame
    test_frame = np.random.randint(0, 256, (240, 320), dtype=np.uint8)
    
    # Extract eigen features
    eigen_image = extract_eigen_features(test_frame, num_components=10)
    energy = compute_eigen_energy(test_frame)
    anomaly = detect_statistical_anomalies(test_frame)
    
    print(f"Input shape: {test_frame.shape}")
    print(f"Eigen image shape: {eigen_image.shape}")
    print(f"Eigen energy: {energy:.2f}")
    print(f"Anomaly score: {anomaly:.2f}")
    print("✅ Eigen vector features working!")
