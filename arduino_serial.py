#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import json
import time
import threading
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class ArduinoSerial(QObject):
    """Arduino ile seri haberleşme sağlayan sınıf"""
    
    # Arduino'dan veri alındığında yayınlanacak sinyal
    data_received = pyqtSignal(dict)
    connection_status = pyqtSignal(bool, str)
    
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.running = False
        self.thread = None
        self.connected = False
        self.reconnect_delay = 1.0  # Yeniden bağlanma gecikmesi
        self.max_reconnect_delay = 30.0  # Maksimum yeniden bağlanma gecikmesi
        
    def connect(self):
        """Arduino ile bağlantı kurar"""
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
                
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Arduino'nun sıfırlanması için bekle
            self.connected = True
            self.reconnect_delay = 1.0  # Başarılı bağlantıda gecikmeyi sıfırla
            self.connection_status.emit(True, f"Bağlantı kuruldu: {self.port}")
            return True
        except serial.SerialException as e:
            self.connected = False
            self.connection_status.emit(False, f"Bağlantı hatası: {str(e)}")
            return False
            
    def start(self):
        """Veri okuma iş parçacığını başlatır"""
        if not self.connected and not self.connect():
            return False
            
        self.running = True
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.daemon = True
        self.thread.start()
        return True
        
    def stop(self):
        """Veri okuma iş parçacığını durdurur"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.serial:
            self.serial.close()
        self.connected = False
        
    def try_reconnect(self):
        """Yeniden bağlanmayı dener"""
        if self.connect():
            return True
        else:
            # Bağlantı başarısız olursa gecikmeyi artır
            self.reconnect_delay = min(self.reconnect_delay * 1.5, self.max_reconnect_delay)
            return False
            
    def _read_loop(self):
        """Sürekli olarak Arduino'dan veri okur"""
        buffer = ""
        last_data_time = time.time()
        data_timeout = 5.0  # 5 saniye veri gelmezse bağlantıyı kontrol et
        
        while self.running:
            try:
                if not self.connected:
                    if self.try_reconnect():
                        buffer = ""  # Buffer'ı temizle
                        last_data_time = time.time()
                    else:
                        time.sleep(self.reconnect_delay)
                    continue
                    
                if self.serial.in_waiting > 0:
                    # Yeni veri var, oku
                    try:
                        new_data = self.serial.readline().decode('ascii', errors='ignore').strip()
                        last_data_time = time.time()
                        
                        # Buffer'a ekle
                        buffer += new_data
                        
                        # Veri sonu işaretini kontrol et
                        if "#END#" in buffer:
                            # Veriyi parçala
                            parts = buffer.split("#END#")
                            for part in parts[:-1]:  # Son parçayı atla (tamamlanmamış olabilir)
                                if "DATA:" in part:
                                    try:
                                        # JSON verisini ayıkla
                                        json_str = part.split("DATA:")[1]
                                        # JSON'u parse et
                                        data = json.loads(json_str)
                                        # Veriyi yayınla
                                        self.data_received.emit(data)
                                    except json.JSONDecodeError as e:
                                        print(f"JSON parse hatası: {e} - Satır: {json_str}")
                                        continue  # Hatalı satırı atla, buffer'ı temizlemeden devam et
                            
                            # Buffer'ı temizle, sadece son parçayı tut
                            buffer = parts[-1]  # Sadece tamamlanmamış kısmı bırak
                    except Exception as e:
                        print(f"Veri okuma hatası: {str(e)}")
                        buffer = ""  # Hata durumunda buffer'ı temizle
                        continue
                else:
                    # Belirli bir süre veri gelmezse bağlantıyı kontrol et
                    if time.time() - last_data_time > data_timeout:
                        print("Veri zaman aşımı - bağlantı kontrol ediliyor")
                        self.connected = False
                        self.connection_status.emit(False, "Veri alınamıyor, bağlantı kontrol ediliyor...")
                        continue
                        
                    # Yeni veri yok, biraz bekle
                    time.sleep(0.01)
                    
            except serial.SerialException as e:
                print(f"Seri port hatası: {str(e)}")
                self.connected = False
                self.connection_status.emit(False, f"Seri port hatası: {str(e)}")
                time.sleep(self.reconnect_delay)
                
            except Exception as e:
                print(f"Beklenmeyen hata: {str(e)}")
                self.connected = False
                self.connection_status.emit(False, f"Beklenmeyen hata: {str(e)}")
                time.sleep(self.reconnect_delay)
                
    def send_command(self, command):
        """Arduino'ya komut gönderir"""
        if not self.connected:
            return False
            
        try:
            self.serial.write(f"{command}\n".encode('utf-8'))
            return True
        except Exception as e:
            print(f"Komut gönderme hatası: {str(e)}")
            return False

# Test fonksiyonu
def test_arduino_serial():
    """Arduino bağlantısını test etmek için kullanılır"""
    arduino = ArduinoSerial()
    
    def on_data_received(data):
        print(f"Veri alındı: {data}")
    
    def on_connection_status(connected, message):
        print(f"Bağlantı durumu: {'Bağlı' if connected else 'Bağlı değil'} - {message}")
    
    arduino.data_received.connect(on_data_received)
    arduino.connection_status.connect(on_connection_status)
    
    if arduino.start():
        print("Veri okuma başlatıldı. 30 saniye boyunca verileri dinleyecek...")
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            pass
        finally:
            arduino.stop()
            print("Bağlantı kapatıldı.")
    else:
        print("Arduino ile bağlantı kurulamadı.")

if __name__ == "__main__":
    test_arduino_serial()
