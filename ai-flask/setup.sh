#!/bin/bash

echo "==============================================="
echo "       YOLO Detection System - Linux/Mac Setup"
echo "==============================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python 3.8+ first"
    exit 1
fi

echo "✅ Python3 found"
echo

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: $python_version"

# Upgrade pip
echo "🔧 Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi
echo

# Run installation script
echo "🚀 Running installation script..."
python3 install.py
echo

# Check if everything is working
echo "🧪 Testing system..."
python3 main.py --check-deps
if [ $? -ne 0 ]; then
    echo "❌ System test failed"
    exit 1
fi
echo

echo "==============================================="
echo "             🎉 Setup Complete! 🎉"
echo "==============================================="
echo
echo "You can now run the system:"
echo "  python3 main.py --mode demo    (Demo with auto rotation)"
echo "  python3 main.py --mode server  (API server only)"
echo "  python3 main.py --mode test    (Test mode)"
echo
echo "For detailed usage, read README.md"
echo
