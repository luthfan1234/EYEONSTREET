# cctv_config.py
# Konfigurasi CCTV untuk sistem monitoring

import os
from typing import Dict, List

class CCTVConfig:
    """
    Konfigurasi CCTV untuk sistem deteksi kecelakaan
    """
    
    def __init__(self):
        self.cctv_cameras = {
            'CCTV-001': {
                'name': 'Jl. Slamet Riyadi - Perempatan',
                'url': 'rtsp://admin:password123@192.168.1.101:554/stream1',
                'location': {'lat': -7.5665, 'lng': 110.8167},
                'status': 'active',
                'priority': 'high'
            },
            'CCTV-002': {
                'name': 'Jl. Ahmad Yani - Simpang Lima',
                'url': 'rtsp://admin:password123@192.168.1.102:554/stream1',
                'location': {'lat': -7.5599, 'lng': 110.8074},
                'status': 'active',
                'priority': 'high'
            },
            'CCTV-003': {
                'name': 'Jl. Dr. Radjiman - Pasar Klewer',
                'url': 'rtsp://admin:password123@192.168.1.103:554/stream1',
                'location': {'lat': -7.5703, 'lng': 110.8230},
                'status': 'active',
                'priority': 'medium'
            },
            'CCTV-004': {
                'name': 'Jl. Brigjen Sudiarto - RS Dr. Moewardi',
                'url': 'rtsp://admin:password123@192.168.1.104:554/stream1',
                'location': {'lat': -7.5521, 'lng': 110.7926},
                'status': 'active',
                'priority': 'medium'
            },
            'CCTV-005': {
                'name': 'Jl. Veteran - Kantor Gubernur',
                'url': 'rtsp://admin:password123@192.168.1.105:554/stream1',
                'location': {'lat': -7.5678, 'lng': 110.8134},
                'status': 'active',
                'priority': 'low'
            },
            'CCTV-006': {
                'name': 'Jl. Raya Solo-Yogya - Exit Tol',
                'url': 'rtsp://admin:password123@192.168.1.106:554/stream1',
                'location': {'lat': -7.5445, 'lng': 110.7789},
                'status': 'active',
                'priority': 'high'
            }
        }
        
        # Untuk development/testing - gunakan webcam atau video sample
        self.development_mode = True
        if self.development_mode:
            self.cctv_cameras.update({
                'CCTV-DEV-001': {
                    'name': 'Development Camera 1',
                    'url': 0,  # Webcam default
                    'location': {'lat': -7.5665, 'lng': 110.8167},
                    'status': 'active',
                    'priority': 'high'
                },
                'CCTV-DEV-002': {
                    'name': 'Development Camera 2',
                    'url': 'sample_traffic.mp4',  # Video sample untuk testing
                    'location': {'lat': -7.5599, 'lng': 110.8074},
                    'status': 'active',
                    'priority': 'high'
                }
            })
    
    def get_all_cameras(self) -> Dict:
        """Mendapatkan semua kamera yang tersedia"""
        return self.cctv_cameras
    
    def get_active_cameras(self) -> List[str]:
        """Mendapatkan daftar CCTV ID yang aktif"""
        return [cctv_id for cctv_id, config in self.cctv_cameras.items() 
                if config.get('status') == 'active']
    
    def get_camera_config(self, cctv_id: str) -> Dict:
        """Mendapatkan konfigurasi kamera berdasarkan ID"""
        return self.cctv_cameras.get(cctv_id, {})
    
    def get_camera_url(self, cctv_id: str) -> str:
        """Mendapatkan URL streaming kamera"""
        config = self.get_camera_config(cctv_id)
        return config.get('url', '')
    
    def is_camera_active(self, cctv_id: str) -> bool:
        """Mengecek apakah kamera aktif"""
        config = self.get_camera_config(cctv_id)
        return config.get('status') == 'active'
    
    def get_priority_cameras(self, priority: str = 'high') -> List[str]:
        """Mendapatkan kamera berdasarkan prioritas"""
        return [cctv_id for cctv_id, config in self.cctv_cameras.items() 
                if config.get('priority') == priority and config.get('status') == 'active']
    
    def update_camera_status(self, cctv_id: str, status: str) -> bool:
        """Update status kamera"""
        if cctv_id in self.cctv_cameras:
            self.cctv_cameras[cctv_id]['status'] = status
            return True
        return False

# Konfigurasi deteksi
DETECTION_CONFIG = {
    'confidence_threshold': 0.5,  # Minimum confidence untuk deteksi
    'model_path': 'accident.pt',  # Path ke model YOLOv8 custom
    'classes_to_detect': [
        'accident',     # Kecelakaan kendaraan
        'crowd',        # Kerumunan orang
        'fire',         # Kebakaran
        'flood'         # Banjir
    ],
    'detection_interval': 1.0,    # Interval deteksi dalam detik
    'max_detection_per_minute': 3,  # Maksimal deteksi per menit untuk menghindari spam
    'screenshot_quality': 90,     # Kualitas screenshot (0-100)
    'auto_rotation_interval': 300,  # 5 menit dalam detik
    'cameras_per_rotation': 2,    # Jumlah kamera yang dimonitor bersamaan
}

# Konfigurasi API Laravel
LARAVEL_API_CONFIG = {
    'base_url': 'http://localhost:8000/api',
    'incidents_endpoint': '/incidents',
    'timeout': 30,
    'retry_attempts': 3,
    'retry_delay': 5  # detik
}

# Konfigurasi Flask
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'cors_origins': [
        'http://localhost:3000',  # Next.js frontend
        'http://localhost:8000',  # Laravel backend
        'http://127.0.0.1:3000',
        'http://127.0.0.1:8000'
    ]
}

# Path untuk menyimpan screenshot
SCREENSHOT_PATH = os.path.join(os.path.dirname(__file__), 'static', 'screenshots')
if not os.path.exists(SCREENSHOT_PATH):
    os.makedirs(SCREENSHOT_PATH)

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'detection_system.log'
}
