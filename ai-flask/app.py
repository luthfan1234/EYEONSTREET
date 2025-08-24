# app.py
# Flask API untuk sistem deteksi kecelakaan

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import signal
import sys
from datetime import datetime
import threading
import time

from yolo_detect import get_detector
from cctv_config import CCTVConfig, FLASK_CONFIG

# Inisialisasi Flask app
app = Flask(__name__)

# Setup CORS
CORS(app, origins=FLASK_CONFIG['cors_origins'], supports_credentials=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flask_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global variables
detector = None
cctv_config = None

def init_system():
    """
    Inisialisasi sistem deteksi
    """
    global detector, cctv_config
    
    logger.info("🚀 Initializing YOLO Detection System...")
    
    try:
        # Initialize CCTV config
        cctv_config = CCTVConfig()
        
        # Initialize detector
        detector = get_detector()
        
        logger.info("✅ System initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize system: {e}")
        return False

def cleanup_system():
    """
    Cleanup sistem saat shutdown
    """
    global detector
    logger.info("🧹 Cleaning up system...")
    
    if detector:
        detector.cleanup()
    
    logger.info("✅ Cleanup completed")

# Signal handlers untuk graceful shutdown
def signal_handler(sig, frame):
    logger.info(f"📡 Received signal {sig}, shutting down...")
    cleanup_system()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ====== API ENDPOINTS ======

@app.route('/', methods=['GET'])
def home():
    """
    Endpoint utama untuk cek status sistem
    """
    return jsonify({
        'status': 'success',
        'message': 'YOLO Detection System is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/status', methods=['GET'])
def get_status():
    """
    Endpoint untuk mendapatkan status sistem
    """
    try:
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        status = detector.get_status()
        cameras = cctv_config.get_all_cameras()
        
        return jsonify({
            'status': 'success',
            'data': {
                'system_status': status,
                'available_cameras': list(cameras.keys()),
                'active_cameras': [cid for cid, config in cameras.items() if config.get('status') == 'active'],
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/cameras', methods=['GET'])
def get_cameras():
    """
    Endpoint untuk mendapatkan daftar kamera
    """
    try:
        cameras = cctv_config.get_all_cameras()
        
        # Format response
        camera_list = []
        for cctv_id, config in cameras.items():
            camera_info = {
                'id': cctv_id,
                'name': config.get('name', 'Unknown'),
                'status': config.get('status', 'inactive'),
                'priority': config.get('priority', 'low'),
                'location': config.get('location', {}),
                'is_detection_running': detector.running_detections.get(cctv_id, False) if detector else False
            }
            camera_list.append(camera_info)
        
        return jsonify({
            'status': 'success',
            'data': {
                'cameras': camera_list,
                'total': len(camera_list),
                'active': len([c for c in camera_list if c['status'] == 'active'])
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting cameras: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/start/<cctv_id>', methods=['POST'])
def start_detection(cctv_id):
    """
    Endpoint untuk memulai deteksi pada kamera tertentu
    """
    try:
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        if not cctv_config.is_camera_active(cctv_id):
            return jsonify({
                'status': 'error',
                'message': f'Camera {cctv_id} is not active or does not exist'
            }), 400
        
        success = detector.start_detection(cctv_id)
        
        if success:
            logger.info(f"✅ Detection started for {cctv_id}")
            return jsonify({
                'status': 'success',
                'message': f'Detection started for camera {cctv_id}',
                'cctv_id': cctv_id,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to start detection for camera {cctv_id}'
            }), 500
    
    except Exception as e:
        logger.error(f"Error starting detection for {cctv_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/stop/<cctv_id>', methods=['POST'])
def stop_detection(cctv_id):
    """
    Endpoint untuk menghentikan deteksi pada kamera tertentu
    """
    try:
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        success = detector.stop_detection(cctv_id)
        
        if success:
            logger.info(f"🛑 Detection stopped for {cctv_id}")
            return jsonify({
                'status': 'success',
                'message': f'Detection stopped for camera {cctv_id}',
                'cctv_id': cctv_id,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f'Failed to stop detection for camera {cctv_id}'
            }), 500
    
    except Exception as e:
        logger.error(f"Error stopping detection for {cctv_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/start-auto-rotation', methods=['POST'])
def start_auto_rotation():
    """
    Endpoint untuk memulai rotasi otomatis kamera
    """
    try:
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        success = detector.start_auto_rotation()
        
        if success:
            logger.info("🔄 Auto rotation started")
            return jsonify({
                'status': 'success',
                'message': 'Auto rotation started successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Auto rotation is already running'
            }), 400
    
    except Exception as e:
        logger.error(f"Error starting auto rotation: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/stop-auto-rotation', methods=['POST'])
def stop_auto_rotation():
    """
    Endpoint untuk menghentikan rotasi otomatis kamera
    """
    try:
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        success = detector.stop_auto_rotation()
        
        if success:
            logger.info("🔄 Auto rotation stopped")
            return jsonify({
                'status': 'success',
                'message': 'Auto rotation stopped successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to stop auto rotation'
            }), 500
    
    except Exception as e:
        logger.error(f"Error stopping auto rotation: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/detection-stats', methods=['GET'])
def get_detection_stats():
    """
    Endpoint untuk mendapatkan statistik deteksi
    """
    try:
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        stats = {
            'active_detections': len(detector.running_detections),
            'detection_counters': detector.detection_counters,
            'auto_rotation_status': detector.auto_rotation_running,
            'current_rotation_cameras': detector.current_rotation_cameras,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting detection stats: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/test-detection', methods=['POST'])
def test_detection():
    """
    Endpoint untuk testing deteksi (development only)
    """
    try:
        data = request.get_json()
        cctv_id = data.get('cctv_id', 'CCTV-DEV-001')
        incident_type = data.get('incident_type', 'accident')
        
        if not detector:
            return jsonify({
                'status': 'error',
                'message': 'Detector not initialized'
            }), 500
        
        # Simulate detection
        fake_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        success = detector.send_to_laravel(cctv_id, incident_type, fake_image_base64)
        
        return jsonify({
            'status': 'success' if success else 'error',
            'message': f'Test detection sent: {incident_type} from {cctv_id}',
            'sent_to_laravel': success,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in test detection: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'status': 'error',
        'message': 'Bad request'
    }), 400

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': time.time()
    })

if __name__ == '__main__':
    # Initialize system
    if not init_system():
        logger.error("❌ Failed to initialize system, exiting...")
        sys.exit(1)
    
    try:
        logger.info(f"🚀 Starting Flask server on {FLASK_CONFIG['host']}:{FLASK_CONFIG['port']}")
        
        # Start Flask app
        app.run(
            host=FLASK_CONFIG['host'],
            port=FLASK_CONFIG['port'],
            debug=FLASK_CONFIG['debug'],
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Shutting down gracefully...")
        cleanup_system()
    except Exception as e:
        logger.error(f"❌ Error running Flask app: {e}")
        cleanup_system()
        sys.exit(1)
