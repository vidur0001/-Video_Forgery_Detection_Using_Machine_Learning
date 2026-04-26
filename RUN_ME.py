"""
ONE-CLICK VIDEO FORGERY DETECTION SYSTEM
=========================================

This script runs the complete video forgery detection system:
1. Auto-generates training data (no external dataset needed)
2. Trains the model automatically
3. Saves the trained model
4. Ready for predictions

NO MANUAL INPUT REQUIRED - Just run this file!

Usage:
    python RUN_ME.py
"""

import os
import sys
import subprocess


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*70)
    print(" VIDEO FORGERY DETECTION SYSTEM ".center(70, "="))
    print("="*70)
    print("\n[*] Multi-Feature Fusion + Deep Learning Approach")
    print("[*] Automated Training & Prediction Pipeline")
    print("\n" + "="*70 + "\n")


def check_dependencies():
    """Check if required libraries are installed."""
    print("[*] Checking dependencies...\n")

    required = {
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
    for pkg, module in required.items():
        try:
            __import__(module)
            print(f"   [OK] {pkg}")
        except ImportError:
            print(f"   [X] {pkg}")
            missing.append(pkg)

    if missing:
        print(f"\n[X] Missing: {', '.join(missing)}")
        print(f"\n[*] Install with:")
        print(f"   pip install {' '.join(missing)}\n")
        return False

    print("\n[OK] All dependencies installed!\n")
    return True


def run_system():
    """Run the complete system."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("[*] Starting automated training...\n")
    print("="*70)
    print("WHAT WILL HAPPEN:")
    print("="*70)
    print("1. Generate synthetic training data (1,000 frames)")
    print("2. Extract 12-channel features (7 methods)")
    print("3. Train ResNet50 + CNN model")
    print("4. Save trained model")
    print("5. Generate training visualizations")
    print("\n[*] Estimated time: 10-15 minutes")
    print("="*70 + "\n")

    # Auto-run with default settings
    print("[>] Running training pipeline...\n")
    
    # Create automated input
    auto_input = "1\ny\n"  # Option 1 (small dataset), then 'y' to train
    
    # Run pipeline with automated input
    process = subprocess.Popen(
        [sys.executable, 'run_complete_pipeline.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=script_dir
    )
    
    # Send automated input
    output, _ = process.communicate(input=auto_input)
    
    # Print output
    print(output)
    
    if process.returncode == 0:
        print("\n" + "="*70)
        print(" TRAINING COMPLETE! ".center(70, "="))
        print("="*70)
        print("\n[OK] Model saved as: forgery_model_enhanced.keras")
        print("[OK] Training plot: training_history.png")
        print("\n[*] Ready to predict videos!")
        print("\nUsage:")
        print("   python predict_video.py path/to/video.mp4")
        print("\n" + "="*70 + "\n")
        return True
    else:
        print("\n[X] Training failed!")
        return False


def main():
    """Main entry point."""
    print_banner()

    # Check dependencies
    if not check_dependencies():
        print("[X] Please install missing dependencies first.\n")
        sys.exit(1)

    # Run system
    success = run_system()

    if success:
        print("[OK] System ready! You can now detect video forgeries.")
        print("\nNext step: Test with a video")
        print("   python predict_video.py your_video.mp4\n")
    else:
        print("[X] Setup failed. Please check errors above.\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[X] Process interrupted by user.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[X] Error: {str(e)}\n")
        sys.exit(1)
