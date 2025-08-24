@echo off
echo ===============================================
echo       YOLO Detection System - Windows Setup
echo ===============================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

:: Upgrade pip
echo 🔧 Upgrading pip...
python -m pip install --upgrade pip
echo.

:: Install requirements
echo 📦 Installing requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)
echo.

:: Run installation script
echo 🚀 Running installation script...
python install.py
echo.

:: Check if everything is working
echo 🧪 Testing system...
python main.py --check-deps
if errorlevel 1 (
    echo ❌ System test failed
    pause
    exit /b 1
)
echo.

echo ===============================================
echo             🎉 Setup Complete! 🎉
echo ===============================================
echo.
echo You can now run the system:
echo   python main.py --mode demo    (Demo with auto rotation)
echo   python main.py --mode server  (API server only)
echo   python main.py --mode test    (Test mode)
echo.
echo For detailed usage, read README.md
echo.
pause
