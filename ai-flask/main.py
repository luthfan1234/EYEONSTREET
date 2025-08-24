# main.py
# Entry point untuk menjalankan sistem deteksi

import sys
import os
import argparse
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_system, cleanup_system
from yolo_detect import get_detector
from cctv_config import FLASK_CONFIG

def setup_logging():
    """Setup logging configuration"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f'detection_system_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def print_banner():
    """Print system banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚨 YOLO Detection System 🚨                ║
    ║                                                              ║
    ║  🎯 Traffic Accident Detection with YOLOv8                   ║
    ║  🔄 Auto Camera Rotation                                     ║
    ║  📡 Flask API Integration                                    ║
    ║  🌐 Laravel/Next.js Compatible                               ║
    ║                                                              ║
    ║  Version: 1.0.0                                              ║
    ║  Author: EyeOnStreets Team                                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_available_endpoints():
    """Show available API endpoints"""
    endpoints = [
        "📡 Available API Endpoints:",
        "",
        "🔍 System Status:",
        f"  GET  http://localhost:{FLASK_CONFIG['port']}/",
        f"  GET  http://localhost:{FLASK_CONFIG['port']}/status",
        f"  GET  http://localhost:{FLASK_CONFIG['port']}/health",
        "",
        "📹 Camera Management:",
        f"  GET  http://localhost:{FLASK_CONFIG['port']}/cameras",
        f"  POST http://localhost:{FLASK_CONFIG['port']}/start/<cctv_id>",
        f"  POST http://localhost:{FLASK_CONFIG['port']}/stop/<cctv_id>",
        "",
        "🔄 Auto Rotation:",
        f"  POST http://localhost:{FLASK_CONFIG['port']}/start-auto-rotation",
        f"  POST http://localhost:{FLASK_CONFIG['port']}/stop-auto-rotation",
        "",
        "📊 Statistics:",
        f"  GET  http://localhost:{FLASK_CONFIG['port']}/detection-stats",
        "",
        "🧪 Testing:",
        f"  POST http://localhost:{FLASK_CONFIG['port']}/test-detection",
        "",
        "📝 Example CURL commands:",
        f"  curl http://localhost:{FLASK_CONFIG['port']}/status",
        f"  curl -X POST http://localhost:{FLASK_CONFIG['port']}/start/CCTV-DEV-001",
        f"  curl -X POST http://localhost:{FLASK_CONFIG['port']}/start-auto-rotation"
    ]
    
    for line in endpoints:
        print(line)

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    try:
        import cv2
        print("✅ OpenCV available")
    except ImportError:
        print("❌ OpenCV not found. Install with: pip install opencv-python")
        return False
    
    try:
        import ultralytics
        print("✅ Ultralytics (YOLOv8) available")
    except ImportError:
        print("❌ Ultralytics not found. Install with: pip install ultralytics")
        return False
    
    try:
        import flask
        print("✅ Flask available")
    except ImportError:
        print("❌ Flask not found. Install with: pip install flask")
        return False
    
    try:
        import flask_cors
        print("✅ Flask-CORS available")
    except ImportError:
        print("❌ Flask-CORS not found. Install with: pip install flask-cors")
        return False
    
    try:
        import requests
        print("✅ Requests available")
    except ImportError:
        print("❌ Requests not found. Install with: pip install requests")
        return False
    
    print("✅ All dependencies available")
    return True

def quick_start_demo():
    """Start quick demo with auto rotation"""
    print("\n🚀 Starting Quick Demo...")
    
    try:
        detector = get_detector()
        
        print("📋 Demo will:")
        print("  1. Start auto rotation (2 cameras every 5 minutes)")
        print("  2. Monitor for accidents/incidents")
        print("  3. Send detections to Laravel API")
        print("  4. Run Flask API server")
        print("")
        
        # Start auto rotation
        detector.start_auto_rotation()
        print("✅ Auto rotation started")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting demo: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='YOLO Detection System')
    parser.add_argument('--mode', choices=['server', 'demo', 'test'], default='server',
                      help='Run mode: server (API only), demo (with auto rotation), test (run tests)')
    parser.add_argument('--port', type=int, default=FLASK_CONFIG['port'],
                      help=f'Port to run server (default: {FLASK_CONFIG["port"]})')
    parser.add_argument('--host', default=FLASK_CONFIG['host'],
                      help=f'Host to bind server (default: {FLASK_CONFIG["host"]})')
    parser.add_argument('--check-deps', action='store_true',
                      help='Check dependencies and exit')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Print banner
    print_banner()
    
    # Check dependencies
    if args.check_deps:
        if check_dependencies():
            print("\n✅ All dependencies satisfied!")
            sys.exit(0)
        else:
            print("\n❌ Missing dependencies!")
            sys.exit(1)
    
    if not check_dependencies():
        print("\n❌ Missing dependencies! Use --check-deps to see details.")
        sys.exit(1)
    
    # Initialize system
    print("🔧 Initializing system...")
    if not init_system():
        print("❌ Failed to initialize system!")
        sys.exit(1)
    
    print("✅ System initialized successfully")
    
    # Show endpoints
    show_available_endpoints()
    
    try:
        if args.mode == 'demo':
            # Quick start demo
            if quick_start_demo():
                print("\n🎯 Demo mode: Auto rotation enabled")
            else:
                print("\n❌ Failed to start demo")
                sys.exit(1)
        elif args.mode == 'test':
            # Test mode
            print("\n🧪 Test mode")
            detector = get_detector()
            
            # Test API endpoint
            success = detector.send_to_laravel('CCTV-TEST-001', 'accident', 'test_image_base64')
            if success:
                print("✅ Laravel API connection test passed")
            else:
                print("⚠️  Laravel API connection test failed (this is normal if Laravel is not running)")
        
        # Start Flask server
        print(f"\n🚀 Starting Flask server on http://{args.host}:{args.port}")
        print("🔗 You can now:")
        print("  - Access the API endpoints shown above")
        print("  - Integrate with Laravel/Next.js frontend")
        print("  - Monitor detection logs in real-time")
        print("\n👋 Press Ctrl+C to stop the server")
        
        # Update Flask config
        FLASK_CONFIG['host'] = args.host
        FLASK_CONFIG['port'] = args.port
        
        # Run Flask app
        app.run(
            host=args.host,
            port=args.port,
            debug=FLASK_CONFIG.get('debug', False),
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        cleanup_system()
        print("✅ Goodbye!")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        cleanup_system()
        sys.exit(1)

if __name__ == '__main__':
    main()