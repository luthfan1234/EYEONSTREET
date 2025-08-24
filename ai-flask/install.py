# Installation Script untuk YOLO Detection System
# Jalankan script ini untuk setup lengkap sistem

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def install_requirements():
    """Install Python packages from requirements.txt"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )

def download_yolo_model():
    """Download YOLOv8 model if not exists"""
    model_file = Path("yolov8n.pt")
    if model_file.exists():
        print("✅ YOLOv8 model already exists")
        return True
    
    print("📥 Downloading YOLOv8 model...")
    try:
        from ultralytics import YOLO
        model = YOLO('yolov8n.pt')  # This will download the model
        print("✅ YOLOv8 model downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download YOLOv8 model: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "static/screenshots",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def test_installation():
    """Test if installation is working"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import cv2
        import ultralytics
        import flask
        import flask_cors
        import requests
        
        print("✅ All packages imported successfully")
        
        # Test basic functionality
        return run_command(
            f"{sys.executable} main.py --check-deps",
            "Running dependency check"
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main installation function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                🚀 YOLO Detection System Setup 🚀             ║
    ║                                                              ║
    ║  This script will install all dependencies and setup        ║
    ║  the YOLO Detection System for traffic accident detection   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Create Directories", create_directories),
        ("Install Requirements", install_requirements),
        ("Download YOLO Model", download_yolo_model),
        ("Test Installation", test_installation)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_function():
            failed_steps.append(step_name)
    
    print("\n" + "="*60)
    
    if not failed_steps:
        print("🎉 INSTALLATION COMPLETE!")
        print("\n✅ All steps completed successfully")
        print("\n🚀 You can now run the system:")
        print("   python main.py --mode demo")
        print("   python main.py --mode server")
        print("\n📚 Read README.md for detailed usage instructions")
    else:
        print("❌ INSTALLATION FAILED!")
        print(f"\n💥 Failed steps: {', '.join(failed_steps)}")
        print("\n🔍 Please check the error messages above and:")
        print("   1. Make sure you have Python 3.8+ installed")
        print("   2. Check your internet connection")
        print("   3. Try running: pip install --upgrade pip")
        print("   4. For Windows: pip install --upgrade setuptools wheel")
        
    print("\n📞 Need help? Check README.md or contact the development team")

if __name__ == "__main__":
    main()
