import cv2
import threading
import time
from pyzbar import pyzbar
from database import Database

class BarcodeReader:
    def __init__(self, camera_url="http://192.168.1.244:8080/video"):
        self.camera_url = camera_url
        self.cap = None
        self.running = False
        self.db = Database()
        self.code_states = {}  # {codigo: {status: bool, last_seen: float, last_read: float}}
        self.callback = None
        self.debounce_time = 0.5  # 500ms debounce
        self.timeout_lost = 1.0   # 1s timeout para marcar como não detectado
    
    def set_callback(self, callback):
        self.callback = callback
    
    def start_reading(self):
        if self.running:
            return False
        
        try:
            self.cap = cv2.VideoCapture(self.camera_url)
            if not self.cap.isOpened():
                return False
            
            self.code_states.clear()  # Limpar estados
            self.running = True
            self.thread = threading.Thread(target=self._read_loop)
            self.thread.daemon = True
            self.thread.start()
            return True
        except Exception:
            return False
    
    def stop_reading(self):
        self.running = False
        if self.cap:
            self.cap.release()
    
    def _read_loop(self):
        while self.running:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                current_time = time.time()
                detected_codes = set()
                
                # Decodificar códigos de barras
                barcodes = pyzbar.decode(frame)
                
                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')
                    detected_codes.add(barcode_data)
                    
                    # Inicializar estado se não existe
                    if barcode_data not in self.code_states:
                        self.code_states[barcode_data] = {
                            'detected': False,
                            'last_seen': current_time,
                            'last_read': 0
                        }
                    
                    state = self.code_states[barcode_data]
                    state['last_seen'] = current_time
                    
                    # Transição: não detectado -> detectado
                    if not state['detected']:
                        # Aplicar debounce
                        if current_time - state['last_read'] >= self.debounce_time:
                            state['detected'] = True
                            state['last_read'] = current_time
                            
                            # Registrar leitura
                            if self.db.produto_exists(barcode_data):
                                self.db.add_leitura(barcode_data)
                                if self.callback:
                                    self.callback(f"Código lido: {barcode_data}", "success")
                            else:
                                if self.callback:
                                    self.callback(f"Código não cadastrado: {barcode_data}", "warning")
                
                # Marcar como não detectado os códigos que não foram vistos
                for code, state in self.code_states.items():
                    if code not in detected_codes:
                        if current_time - state['last_seen'] >= self.timeout_lost:
                            state['detected'] = False
                
            except Exception as e:
                if self.callback:
                    self.callback(f"Erro na leitura: {str(e)}", "error")
                break
    
    def is_running(self):
        return self.running