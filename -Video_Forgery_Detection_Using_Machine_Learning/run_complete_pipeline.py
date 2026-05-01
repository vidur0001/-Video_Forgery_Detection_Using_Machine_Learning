"""
Complete Pipeline Script
Runs the entire video forgery detection system from data generation to evaluation
"""

import os
import sys
import subprocess


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")


def run_command(command, description, cwd=None):
    """
    Run a command and handle errors.

    Args:
        command: str - Command to run
        description: str - Description of the command
        cwd: str - Working directory for the command

    Returns:
        bool - True if successful, False otherwise
    """
    print(f"[>] {description}...")
    result = subprocess.run(command, shell=True, capture_output=False, cwd=cwd)

    if result.returncode == 0:
        print(f"[OK] {description} completed successfully!\n")
        return True
    else:
        print(f"[X] {description} failed!\n")
        return False


def check_installation():
    """Check if required libraries are installed."""
    print_header("CHECKING INSTALLATION")

    # Map package names to import names
    lib_map = {
        'numpy': 'numpy',
        'opencv-python': 'cv2',
        'keras': 'keras',
        'tensorflow': 'tensorflow',
        'matplotlib': 'matplotlib',
        'scipy': 'scipy',
        'scikit-learn': 'sklearn',
        'scikit-image': 'skimage',
        'PyWavelets': 'pywt'
    }

    missing = []
    for pkg_name, import_name in lib_map.items():
        try:
            __import__(import_name)
            print(f"[OK] {pkg_name}")
        except ImportError:
            print(f"[X] {pkg_name} - NOT INSTALLED")
            missing.append(pkg_name)

    if missing:
        print(f"\n[X] Missing libraries: {', '.join(missing)}")
        print(f"\nInstall with:")
        print(f"pip install {' '.join(missing)}")
        return False

    print("\n[OK] All required libraries are installed!")
    return True


def main():
    """Main pipeline execution."""
    print_header("ENHANCED VIDEO FORGERY DETECTION PIPELINE")

    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Check installation
    if not check_installation():
        print("\n[X] Please install missing libraries first.")
        return
    
    # Step 2: Generate synthetic data
    print_header("STEP 1: GENERATE SYNTHETIC DATA")
    print("Choose data generation option:")
    print("  1. Small dataset (1,000 frames) - Quick testing")
    print("  2. Full dataset (6,990 frames) - Full training")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == '1':
        data_script = 'generate_small_synthetic_data.py'
    else:
        data_script = 'generate_synthetic_data.py'

    if not run_command(f'python {data_script}', 'Data generation', cwd=script_dir):
        return
    
    # Step 3: Train model
    print_header("STEP 2: TRAIN ENHANCED MODEL")
    print("This will:")
    print("  - Extract 12-channel features from frames")
    print("  - Train ResNet50 + CNN classifier")
    print("  - Save best model as 'forgery_model_enhanced.keras'")

    proceed = input("\nProceed with training? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Training skipped.")
        return

    if not run_command('python training/train_enhanced_model.py', 'Model training', cwd=script_dir):
        return

    # Step 4: Evaluate model
    print_header("STEP 3: EVALUATE MODEL")
    print("This will:")
    print("  - Test the trained model")
    print("  - Calculate accuracy, precision, recall, F1")
    print("  - Generate confusion matrix and ROC curve")

    proceed = input("\nProceed with evaluation? (y/n): ").strip().lower()
    if proceed != 'y':
        print("Evaluation skipped.")
        return

    if not run_command('python training/evaluate_model.py', 'Model evaluation', cwd=script_dir):
        return
    
    # Done!
    print_header("PIPELINE COMPLETE!")
    print("[OK] All steps completed successfully!")
    print("\nGenerated files:")
    print("  - video_tampering_dataset/Xtrain.npy")
    print("  - video_tampering_dataset/Ytrain.npy")
    print("  - forgery_model_enhanced.keras")
    print("  - training_history.png")
    print("  - confusion_matrix.png")
    print("  - roc_curve.png")
    print("\nYou can now use the model to detect forgeries in new videos!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Pipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[X] Pipeline failed with error:")
        print(f"   {str(e)}")
        sys.exit(1)
