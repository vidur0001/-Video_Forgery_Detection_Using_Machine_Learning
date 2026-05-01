"""
Evaluation Script for Enhanced Video Forgery Detection Model
"""

import numpy as np
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from keras.models import load_model
from model.feature_combiner import batch_extract_all_features
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                            f1_score, confusion_matrix, classification_report)
import matplotlib.pyplot as plt
import seaborn as sns


def load_test_data(data_path=None):
    """
    Load test data.

    Args:
        data_path: str - Path to dataset directory

    Returns:
        Xtest: numpy array - RGB frames
        Ytest: numpy array - Labels
    """
    print("Loading test data...")

    if data_path is None:
        data_path = os.path.join(parent_dir, 'video_tampering_dataset')

    # For now, use training data as test (in real scenario, use separate test set)
    Xtest_path = os.path.join(data_path, 'Xtrain.npy')
    Ytest_path = os.path.join(data_path, 'Ytrain.npy')
    
    if not os.path.exists(Xtest_path) or not os.path.exists(Ytest_path):
        print(f"[ERROR] Data files not found in {data_path}")
        return None, None
    
    Xtest = np.load(Xtest_path)
    Ytest = np.load(Ytest_path)
    
    print(f"[OK] Loaded {len(Xtest)} test samples")
    
    return Xtest, Ytest


def evaluate_model(model_path='forgery_model_enhanced.keras', use_subset=100):
    """
    Evaluate the trained model.
    
    Args:
        model_path: str - Path to saved model
        use_subset: int - Number of samples to use for evaluation
        
    Returns:
        results: dict - Evaluation metrics
    """
    # Load model
    print(f"\nLoading model from {model_path}...")
    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found: {model_path}")
        print("Please train the model first using train_enhanced_model.py")
        return None
    
    model = load_model(model_path)
    print("[OK] Model loaded successfully!")
    
    # Load test data
    Xtest, Ytest = load_test_data()
    if Xtest is None:
        return None
    
    # Use subset for quick evaluation
    if use_subset is not None:
        Xtest = Xtest[:use_subset]
        Ytest = Ytest[:use_subset]
        print(f"Using {use_subset} samples for evaluation...")
    
    # Extract features
    print("\nExtracting features from test frames...")
    X_features = batch_extract_all_features(Xtest)
    
    # Make predictions
    print("\nMaking predictions...")
    y_pred_prob = model.predict(X_features)
    y_pred = (y_pred_prob > 0.5).astype(int).flatten()
    
    # Calculate metrics
    print("\nCalculating metrics...")
    accuracy = accuracy_score(Ytest, y_pred)
    precision = precision_score(Ytest, y_pred, zero_division=0)
    recall = recall_score(Ytest, y_pred, zero_division=0)
    f1 = f1_score(Ytest, y_pred, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(Ytest, y_pred)
    
    # Store results
    results = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'y_true': Ytest,
        'y_pred': y_pred,
        'y_pred_prob': y_pred_prob
    }
    
    return results


def print_results(results):
    """
    Print evaluation results.
    
    Args:
        results: dict - Evaluation metrics
    """
    print("\n" + "="*60)
    print("EVALUATION RESULTS")
    print("="*60)
    print(f"Accuracy:  {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
    print(f"Precision: {results['precision']:.4f} ({results['precision']*100:.2f}%)")
    print(f"Recall:    {results['recall']:.4f} ({results['recall']*100:.2f}%)")
    print(f"F1-Score:  {results['f1_score']:.4f}")
    print("="*60)
    
    print("\nConfusion Matrix:")
    print(results['confusion_matrix'])
    print("\nClassification Report:")
    print(classification_report(results['y_true'], results['y_pred'], 
                                target_names=['Authentic', 'Forged']))


def plot_confusion_matrix(cm, save_path='confusion_matrix.png'):
    """
    Plot confusion matrix.
    
    Args:
        cm: numpy array - Confusion matrix
        save_path: str - Path to save plot
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Authentic', 'Forged'],
                yticklabels=['Authentic', 'Forged'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Confusion matrix saved as '{save_path}'")
    plt.show()


def plot_roc_curve(y_true, y_pred_prob, save_path='roc_curve.png'):
    """
    Plot ROC curve.
    
    Args:
        y_true: numpy array - True labels
        y_pred_prob: numpy array - Predicted probabilities
        save_path: str - Path to save plot
    """
    from sklearn.metrics import roc_curve, auc
    
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[OK] ROC curve saved as '{save_path}'")
    plt.show()


if __name__ == "__main__":
    print("="*60)
    print("ENHANCED VIDEO FORGERY DETECTION - EVALUATION")
    print("="*60)
    
    # Evaluate model
    results = evaluate_model(
        model_path='forgery_model_enhanced.keras',
        use_subset=100  # Change to None for full evaluation
    )
    
    if results is None:
        print("\n[ERROR] Evaluation failed.")
        exit(1)
    
    # Print results
    print_results(results)
    
    # Plot confusion matrix
    plot_confusion_matrix(results['confusion_matrix'])
    
    # Plot ROC curve
    plot_roc_curve(results['y_true'], results['y_pred_prob'])
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE!")
    print("="*60)
