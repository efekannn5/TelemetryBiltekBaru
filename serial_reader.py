import serial
import json
import time
import os
import csv
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

class SerialReader(QThread):
    """Arduino'dan CAN-BUS üzerinden gelen telemetri verilerini okuyan sınıf"""
    
    # Veri sinyalleri
    data_received = pyqtSignal(dict)
    connection_error = pyqtSignal(str)
    
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.is_running = True
        self.connected = False
        self.serial_port = None
        
        # Log dosyası ayarları
        self.log_dir = "logs"
        self.current_log_file = None
        self.csv_writer = None
        self.setup_logging()
        
    def setup_logging(self):
        """Log dizinini ve dosyasını oluşturur"""
        # Log dizinini oluştur
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # Yeni log dosyası adı (tarih-saat formatında)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = os.path.join(self.log_dir, f"vehicle_data_{timestamp}.csv")
        
        # CSV dosyasını oluştur ve başlıkları yaz
        with open(self.current_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Timestamp",
                "AKS_Durumu",
                "Hiz",
                "Batarya_Yuzdesi",
                "Batarya_Sicaklik",
                "Motor_Sicaklik",
                "Guc_Kullanimi",
                "Rejeneratif_Guc",
                "Farlar",
                "Sol_Kor_Nokta",
                "Sag_Kor_Nokta",
                "Kilometre",
                "Paket_Voltaj",
                "Min_Hucre_Voltaj",
                "Max_Hucre_Voltaj",
                "Anlik_Guc",
                "Ortalama_Guc",
                "Vites"
            ])
    
    def log_data(self, data):
        """Gelen veriyi CSV dosyasına kaydeder"""
        try:
            with open(self.current_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    data.get("aks_enabled", False),
                    data.get("speed", 0),
                    data.get("battery_level", 0),
                    data.get("battery_temp", 0),
                    data.get("motor_temp", 0),
                    data.get("power_usage", 0),
                    data.get("regen_power", 0),
                    data.get("headlights", 0),
                    data.get("left_blind_spot", False),
                    data.get("right_blind_spot", False),
                    data.get("odometer", 0),
                    data.get("pack_voltage", 0),
                    data.get("min_cell_voltage", 0),
                    data.get("max_cell_voltage", 0),
                    data.get("instant_power", 0),
                    data.get("average_power", 0),
                    data.get("gear", "N")
                ])
        except Exception as e:
            print(f"Log kayıt hatası: {str(e)}")
    
    def connect(self):
        """Seri port bağlantısını açar"""
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            time.sleep(2)
            self.connected = True
            return True
        except serial.SerialException as e:
            self.connection_error.emit(f"Seri port bağlantı hatası: {str(e)}")
            self.connected = False
            return False
            
    def disconnect(self):
        """Seri port bağlantısını kapatır"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.connected = False
        
    def run(self):
        """Thread çalıştırma metodu"""
        if not self.connect():
            # 5 saniyede bir yeniden bağlanmayı dene
            while self.is_running and not self.connected:
                time.sleep(5)
                self.connect()
                
        buffer = ""
        while self.is_running:
            try:
                if self.serial_port and self.serial_port.is_open:
                    try:
                        # Verinin tam olarak okunabilmesi için bir satır oku
                        line = self.serial_port.readline().decode('ascii', errors='ignore').strip()
                        
                        # Boş satırları atla
                        if not line:
                            continue

                        # Buffer'a ekle
                        buffer += line
                        
                        # "DATA:" önekini kontrol et
                        if "DATA:" in buffer:
                            # En son "DATA:" önekinden sonraki veriyi al
                            parts = buffer.split("DATA:")
                            if len(parts) > 1:
                                json_str = parts[-1]
                                try:
                                    # JSON verisini parse et
                                    data = json.loads(json_str)
                                    
                                    # Veriyi gönder
                                    self.data_received.emit(data)
                                    # Veriyi kaydet
                                    self.log_data(data)
                                    
                                    # Buffer'ı temizle
                                    buffer = ""
                                except json.JSONDecodeError as e:
                                    print(f"JSON parse hatası: {e}")
                                    # Hatalı veriyi buffer'dan temizle
                                    buffer = ""
                                    continue
                    except Exception as e:
                        print(f"Veri okuma hatası: {str(e)}")
                        buffer = ""  # Hata durumunda buffer'ı temizle
                        continue
                else:
                    # Bağlantı kopmuşsa yeniden bağlanmayı dene
                    self.connect()
                    time.sleep(1)
                    
            except Exception as e:
                self.connection_error.emit(f"Veri okuma hatası: {str(e)}")
                self.disconnect()
                time.sleep(1)
                
    def stop(self):
        """Thread'i durdur"""
        self.is_running = False
        self.disconnect()
        self.wait()
        
# Sanal veri üreteci (test için)
class DummyDataGenerator(QThread):
    """Test için sahte telemetri verileri üreten sınıf"""
    
    data_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.is_running = True
        self.current_gear = 'N'
        self.last_gear_change = time.time()
        
    def run(self):
        import random
        while self.is_running:
            # Vites değişimi simülasyonu (her 5 saniyede bir)
            current_time = time.time()
            if current_time - self.last_gear_change >= 5:
                if self.current_gear == 'N':
                    self.current_gear = 'D'
                elif self.current_gear == 'D':
                    self.current_gear = 'N'
                elif self.current_gear == 'R':
                    self.current_gear = 'N'
                self.last_gear_change = current_time
            
            # Rastgele test verileri oluştur
            data = {
                "speed": random.randint(0, 160),
                "battery_level": random.randint(10, 100),
                "battery_temp": random.randint(20, 70),
                "motor_temp": random.randint(30, 90),
                "power_usage": random.randint(5, 60),
                "regen_power": random.randint(0, 30),
                "left_blinker": random.choice([True, False]),
                "right_blinker": random.choice([True, False]),
                "headlights": random.choice([0, 1, 2]),  # 0: Kapalı, 1: Kısa, 2: Uzun
                "left_blind_spot": random.choice([True, False]),
                "right_blind_spot": random.choice([True, False]),
                "drive_mode": random.choice(["ECO", "NORMAL", "SPORT"]),
                "range_estimate": random.randint(50, 350),
                "odometer": random.randint(0, 50000),
                "regen_level": random.randint(0, 3),
                "climate_temp": random.randint(16, 28),
                "climate_fan": random.randint(0, 5),
                "time": time.strftime("%H:%M"),
                "date": time.strftime("%d.%m.%Y"),
                "gear": self.current_gear
            }
            self.data_received.emit(data)
            time.sleep(0.5)
            
    def stop(self):
        self.is_running = False
        self.wait()
