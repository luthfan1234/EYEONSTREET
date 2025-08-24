# yolo_detect.py
# Logic deteksi menggunakan YOLOv8

import cv2
import numpy as np
import base64
import logging
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from ultralytics import YOLO
from PIL import Image
import io
import requests
import json

from cctv_config import CCTVConfig, DETECTION_CONFIG, LARAVEL_API_CONFIG, SCREENSHOT_PATH

class YOLODetector:
    """
    Kelas untuk deteksi menggunakan YOLOv8
    """
    
    def __init__(self):
        self.model = None
        self.cctv_config = CCTVConfig()
        self.active_streams = {}  # Dict untuk menyimpan stream yang aktif
        self.detection_counters = {}  # Counter untuk membatasi deteksi spam
        self.running_detections = {}  # Status running untuk setiap kamera
        self.auto_rotation_thread = None
        self.auto_rotation_running = False
        self.current_rotation_cameras = []
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, 'INFO'),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('detection_system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load YOLO model
        self.load_model()
    
    def load_model(self):
        """Load YOLOv8 model"""
        try:
            model_path = DETECTION_CONFIG['model_path']
            if model_path and model_path != 'accident.pt':
                self.model = YOLO(model_path)
                self.logger.info(f"✅ Model loaded successfully: {model_path}")
            else:
                # Jika tidak ada model custom, gunakan model pre-trained YOLOv8
                self.model = YOLO('yolov8n.pt')  # Akan download otomatis jika belum ada
                self.logger.info("✅ Using YOLOv8n pre-trained model")
        except Exception as e:
            self.logger.error(f"❌ Error loading model: {e}")
            # Fallback ke model pre-trained
            try:
                self.model = YOLO('yolov8n.pt')
                self.logger.info("✅ Fallback to YOLOv8n pre-trained model")
            except Exception as fallback_error:
                self.logger.error(f"❌ Failed to load fallback model: {fallback_error}")
                self.model = None
    
    def detect_objects(self, frame: np.ndarray) -> List[Dict]:
        """
        Deteksi objek dalam frame
        """
        if self.model is None:
            return []
        
        try:
            results = self.model(frame, verbose=False)
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Mendapatkan confidence dan class
                        conf = float(box.conf.cpu().numpy()[0])
                        cls_id = int(box.cls.cpu().numpy()[0])
                        class_name = self.model.names[cls_id]
                        
                        # Filter berdasarkan confidence threshold
                        if conf >= DETECTION_CONFIG['confidence_threshold']:
                            # Mendapatkan koordinat bounding box
                            x1, y1, x2, y2 = box.xyxy.cpu().numpy()[0]
                            
                            detection = {
                                'class': class_name,
                                'confidence': conf,
                                'bbox': [int(x1), int(y1), int(x2), int(y2)]
                            }
                            
                            # Klasifikasi incident type berdasarkan detected class
                            incident_type = self._classify_incident_type(class_name, conf)
                            if incident_type:
                                detection['incident_type'] = incident_type
                                detections.append(detection)
            
            return detections
        except Exception as e:
            self.logger.error(f"Error in object detection: {e}")
            return []
    
    def _classify_incident_type(self, class_name: str, confidence: float) -> Optional[str]:
        """
        Klasifikasi tipe incident berdasarkan detected class
        """
        # Mapping class names ke incident types
        incident_mapping = {
            # Kendaraan dan kecelakaan
            'car': 'traffic' if confidence < 0.8 else None,
            'truck': 'traffic' if confidence < 0.8 else None,
            'bus': 'traffic' if confidence < 0.8 else None,
            'motorcycle': 'traffic' if confidence < 0.8 else None,
            
            # Deteksi kecelakaan (jika ada model custom)
            'accident': 'accident',
            'crash': 'accident',
            'collision': 'accident',
            
            # Deteksi kerumunan
            'person': 'crowd' if confidence > 0.7 else None,
            'crowd': 'crowd',
            
            # Situasi darurat lainnya
            'fire': 'fire',
            'smoke': 'fire',
            'flood': 'flood',
            'debris': 'accident'
        }
        
        # Heuristic untuk deteksi kecelakaan berdasarkan multiple objects
        if class_name in ['car', 'truck', 'bus', 'motorcycle'] and confidence > 0.9:
            return 'accident'  # High confidence vehicle detection might indicate accident
        
        return incident_mapping.get(class_name.lower())
    
    def capture_screenshot(self, frame: np.ndarray, cctv_id: str) -> str:
        """
        Capture screenshot dan konversi ke base64
        """
        try:
            # Convert frame ke PIL Image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Save screenshot to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{cctv_id}_{timestamp}.jpg"
            filepath = os.path.join(SCREENSHOT_PATH, filename)
            pil_image.save(filepath, quality=DETECTION_CONFIG['screenshot_quality'])
            
            # Convert to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=DETECTION_CONFIG['screenshot_quality'])
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            self.logger.info(f"📸 Screenshot captured: {filename}")
            return img_base64
        except Exception as e:
            self.logger.error(f"Error capturing screenshot: {e}")
            return ""
    
    def send_to_laravel(self, cctv_id: str, incident_type: str, image_base64: str) -> bool:
        """
        Kirim data deteksi ke API Laravel
        """
        try:
            url = LARAVEL_API_CONFIG['base_url'] + LARAVEL_API_CONFIG['incidents_endpoint']
            
            data = {
                'cctv_id': cctv_id,
                'type': incident_type,
                'image_base64': image_base64,
                'detected_at': datetime.now().isoformat(),
                'confidence': 0.85  # Could be passed from detection
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Retry mechanism
            for attempt in range(LARAVEL_API_CONFIG['retry_attempts']):
                try:
                    response = requests.post(
                        url, 
                        json=data, 
                        headers=headers,
                        timeout=LARAVEL_API_CONFIG['timeout']
                    )
                    
                    if response.status_code in [200, 201]:
                        self.logger.info(f"✅ Incident sent to Laravel: {cctv_id} - {incident_type}")
                        return True
                    else:
                        self.logger.warning(f"⚠️ Laravel API response: {response.status_code} - {response.text}")
                        
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"❌ Request error (attempt {attempt + 1}): {e}")
                    
                if attempt < LARAVEL_API_CONFIG['retry_attempts'] - 1:
                    time.sleep(LARAVEL_API_CONFIG['retry_delay'])
            
            return False
        except Exception as e:
            self.logger.error(f"Error sending to Laravel: {e}")
            return False
    
    def _should_detect(self, cctv_id: str) -> bool:
        """
        Cek apakah boleh melakukan deteksi (untuk menghindari spam)
        """
        current_time = datetime.now()
        
        if cctv_id not in self.detection_counters:
            self.detection_counters[cctv_id] = {
                'count': 0,
                'reset_time': current_time + timedelta(minutes=1)
            }
        
        counter = self.detection_counters[cctv_id]
        
        # Reset counter setiap menit
        if current_time >= counter['reset_time']:
            counter['count'] = 0
            counter['reset_time'] = current_time + timedelta(minutes=1)
        
        # Cek apakah masih di bawah limit
        if counter['count'] >= DETECTION_CONFIG['max_detection_per_minute']:
            return False
        
        return True
    
    def start_detection(self, cctv_id: str) -> bool:
        """
        Mulai deteksi untuk kamera tertentu
        """
        if cctv_id in self.running_detections and self.running_detections[cctv_id]:
            self.logger.warning(f"⚠️ Detection already running for {cctv_id}")
            return False
        
        if not self.cctv_config.is_camera_active(cctv_id):
            self.logger.error(f"❌ Camera {cctv_id} is not active")
            return False
        
        try:
            camera_url = self.cctv_config.get_camera_url(cctv_id)
            cap = cv2.VideoCapture(camera_url)
            
            if not cap.isOpened():
                self.logger.error(f"❌ Cannot open camera {cctv_id}: {camera_url}")
                return False
            
            self.active_streams[cctv_id] = cap
            self.running_detections[cctv_id] = True
            
            # Start detection thread
            detection_thread = threading.Thread(
                target=self._detection_loop,
                args=(cctv_id,),
                daemon=True
            )
            detection_thread.start()
            
            self.logger.info(f"🎥 Started detection for {cctv_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting detection for {cctv_id}: {e}")
            return False
    
    def stop_detection(self, cctv_id: str) -> bool:
        """
        Hentikan deteksi untuk kamera tertentu
        """
        try:
            self.running_detections[cctv_id] = False
            
            if cctv_id in self.active_streams:
                self.active_streams[cctv_id].release()
                del self.active_streams[cctv_id]
            
            self.logger.info(f"🛑 Stopped detection for {cctv_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping detection for {cctv_id}: {e}")
            return False
    
    def _detection_loop(self, cctv_id: str):
        """
        Main detection loop untuk satu kamera
        """
        cap = self.active_streams.get(cctv_id)
        if not cap:
            return
        
        self.logger.info(f"🔍 Detection loop started for {cctv_id}")
        
        frame_count = 0
        last_detection_time = 0
        
        while self.running_detections.get(cctv_id, False):
            try:
                ret, frame = cap.read()
                if not ret:
                    self.logger.warning(f"⚠️ Cannot read frame from {cctv_id}")
                    time.sleep(1)
                    continue
                
                frame_count += 1
                current_time = time.time()
                
                # Deteksi setiap N frame atau setelah interval tertentu
                if (current_time - last_detection_time) >= DETECTION_CONFIG['detection_interval']:
                    if self._should_detect(cctv_id):
                        detections = self.detect_objects(frame)
                        
                        for detection in detections:
                            if 'incident_type' in detection:
                                incident_type = detection['incident_type']
                                confidence = detection['confidence']
                                
                                self.logger.info(f"🚨 DETECTED: {incident_type} at {cctv_id} (confidence: {confidence:.2f})")
                                
                                # Capture screenshot
                                screenshot_base64 = self.capture_screenshot(frame, cctv_id)
                                
                                # Send to Laravel
                                success = self.send_to_laravel(cctv_id, incident_type, screenshot_base64)
                                
                                if success:
                                    # Update counter
                                    if cctv_id in self.detection_counters:
                                        self.detection_counters[cctv_id]['count'] += 1
                    
                    last_detection_time = current_time
                
                # Small delay untuk mengurangi beban CPU
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error in detection loop for {cctv_id}: {e}")
                time.sleep(1)
        
        # Cleanup
        if cap:
            cap.release()
        self.logger.info(f"🔚 Detection loop ended for {cctv_id}")
    
    def start_auto_rotation(self) -> bool:
        """
        Mulai sistem rotasi otomatis kamera
        """
        if self.auto_rotation_running:
            self.logger.warning("⚠️ Auto rotation already running")
            return False
        
        self.auto_rotation_running = True
        self.auto_rotation_thread = threading.Thread(
            target=self._auto_rotation_loop,
            daemon=True
        )
        self.auto_rotation_thread.start()
        
        self.logger.info("🔄 Auto rotation started")
        return True
    
    def stop_auto_rotation(self) -> bool:
        """
        Hentikan sistem rotasi otomatis
        """
        self.auto_rotation_running = False
        
        # Stop semua kamera yang sedang dimonitor
        for cctv_id in self.current_rotation_cameras:
            self.stop_detection(cctv_id)
        
        self.current_rotation_cameras = []
        self.logger.info("🔄 Auto rotation stopped")
        return True
    
    def _auto_rotation_loop(self):
        """
        Loop untuk rotasi otomatis kamera
        """
        active_cameras = self.cctv_config.get_active_cameras()
        camera_index = 0
        
        self.logger.info(f"🔄 Auto rotation loop started with {len(active_cameras)} cameras")
        
        while self.auto_rotation_running:
            try:
                # Stop kamera sebelumnya
                for cctv_id in self.current_rotation_cameras:
                    self.stop_detection(cctv_id)
                
                # Pilih kamera berikutnya
                cameras_per_rotation = DETECTION_CONFIG['cameras_per_rotation']
                self.current_rotation_cameras = []
                
                for i in range(cameras_per_rotation):
                    if camera_index < len(active_cameras):
                        camera_id = active_cameras[camera_index]
                        self.current_rotation_cameras.append(camera_id)
                        camera_index += 1
                    else:
                        # Reset ke awal jika sudah mencapai akhir
                        camera_index = 0
                        if active_cameras:
                            camera_id = active_cameras[camera_index]
                            self.current_rotation_cameras.append(camera_id)
                            camera_index += 1
                
                # Start deteksi untuk kamera terpilih
                for cctv_id in self.current_rotation_cameras:
                    self.start_detection(cctv_id)
                
                self.logger.info(f"🔄 Rotation: monitoring {self.current_rotation_cameras}")
                
                # Tunggu sesuai interval
                time.sleep(DETECTION_CONFIG['auto_rotation_interval'])
                
            except Exception as e:
                self.logger.error(f"Error in auto rotation loop: {e}")
                time.sleep(10)  # Wait before retry
    
    def get_status(self) -> Dict:
        """
        Mendapatkan status sistem deteksi
        """
        return {
            'model_loaded': self.model is not None,
            'active_detections': list(self.running_detections.keys()),
            'auto_rotation_running': self.auto_rotation_running,
            'current_rotation_cameras': self.current_rotation_cameras,
            'total_cameras': len(self.cctv_config.get_active_cameras()),
            'detection_counters': self.detection_counters
        }
    
    def cleanup(self):
        """
        Cleanup resources
        """
        # Stop auto rotation
        self.stop_auto_rotation()
        
        # Stop all detections
        for cctv_id in list(self.running_detections.keys()):
            self.stop_detection(cctv_id)
        
        # Close all streams
        for cap in self.active_streams.values():
            cap.release()
        
        self.active_streams.clear()
        self.running_detections.clear()
        
        self.logger.info("🧹 Cleanup completed")

# Global detector instance
detector = None

def get_detector() -> YOLODetector:
    """
    Get global detector instance (singleton pattern)
    """
    global detector
    if detector is None:
        detector = YOLODetector()
    return detector
