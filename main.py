#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EV Dashboard - Ana Uygulama
===========================
EV (Elektrikli Araç) telemetri ekranı ana uygulaması.
Raspberry Pi 4B üzerinde 1480x320 ekranda, Arduino'dan seri port üzerinden veri alarak çalışır.

Bu uygulama, aracın elektrik sistemi, batarya durumu, sıcaklık verileri ve diğer telemetri 
verilerini gerçek zamanlı olarak görselleştirir.

Kullanım:
python main.py [-a/--auto]  # Otomatik Arduino bağlantısı için
python main.py [-p/--port PORT]  # Belirli bir seri port ile bağlanmak için
python main.py [-t/--test]  # Test modu (Arduino bağlantısı olmadan)
Powered by Efekan Nefesoglu
"""

import sys
import os
import argparse
import time
import signal
import json
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QIcon
import threading
from flask import Flask, jsonify
import subprocess

from dashboard_ui import Dashboard
from arduino_serial import ArduinoSerial

flask_app = Flask(__name__, static_folder='.')

@flask_app.route('/', methods=['GET'])
def index():
    return flask_app.send_static_file('index.html')

@flask_app.route('/telemetry', methods=['GET'])
def get_telemetry():
    if hasattr(flask_app, 'dashboard'):
        data = flask_app.dashboard.get_telemetry_data()
        return jsonify(data)
    return jsonify({"error": "Dashboard nesnesi yok"})

def start_flask_server():
    flask_app.run(host='0.0.0.0', port=8000)

def start_cloudflared_tunnel():
    subprocess.Popen(['cloudflared', 'tunnel', 'run', 'e-car'])

class EVDashboardApp:
    """EV Dashboard uygulaması ana sınıfı"""
    
    def __init__(self):
        try:
            # Komut satırı argümanlarını analiz et
            self.args = self.parse_arguments()
            
            # PyQt uygulamasını başlat
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("EV Dashboard")
            self.app.setOrganizationName("EV Team")
            
            # SIGINT (Ctrl+C) işleyicisi
            signal.signal(signal.SIGINT, self.signal_handler)
            
            # Splash ekranı göster
            self.show_splash_screen()
            
            try:
                # Dashboard'u oluştur (test modu parametresiyle)
                self.dashboard = Dashboard(test_mode=self.args.test)
                
                # Test modunda gerçek bağlantılar yapılmaz
                if not self.args.test:
                    # Eğer otomatik bağlantı isteniyorsa, son bağlantı bilgilerini kontrol et
                    if self.args.auto:
                        self.auto_connect()
                    elif self.args.port:
                        # Belirli bir port ile bağlan
                        self.dashboard.connect_arduino(self.args.port, 115200)
            except Exception as e:
                print(f"Dashboard oluşturulurken hata: {e}")
                # Temel bir dashboard oluştur
                self.dashboard = Dashboard(test_mode=True)
                
            # EVDashboardApp sınıfının __init__ metoduna ekle
            threading.Thread(target=start_flask_server).start()
            threading.Thread(target=start_cloudflared_tunnel).start()
            
            # EVDashboardApp sınıfının __init__ metodunda dashboard oluşturulduktan sonra:
            flask_app.dashboard = self.dashboard
                
        except Exception as e:
            print(f"Uygulama başlatılırken hata: {e}")
            sys.exit(1)
    
    def parse_arguments(self):
        """Komut satırı argümanlarını analiz eder"""
        parser = argparse.ArgumentParser(description="EV Dashboard uygulaması")
        parser.add_argument("-t", "--test", action="store_true", 
                           help="Test modu (Arduino bağlantısı olmadan)")
        parser.add_argument("-a", "--auto", action="store_true", 
                           help="Son başarılı bağlantı ayarları ile otomatik bağlan")
        parser.add_argument("-p", "--port", default=None, 
                           help="Belirli bir Arduino seri portu ile bağlan")
        return parser.parse_args()
    
    def auto_connect(self):
        """Son başarılı bağlantı bilgilerini kullanarak otomatik bağlanır"""
        try:
            # Konfigürasyon dosyasını kontrol et
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                if 'arduino' in config and 'port' in config['arduino']:
                    port = config['arduino']['port']
                    baudrate = config['arduino'].get('baudrate', 115200)
                    
                    print(f"Son başarılı bağlantı bilgileri ile bağlanılıyor: {port}, {baudrate}")
                    return self.dashboard.connect_arduino(port, baudrate)
            
            print("Daha önceki bağlantı bilgisi bulunamadı")
            return False
            
        except Exception as e:
            print(f"Otomatik bağlantı başarısız: {e}")
            return False
    
    def show_splash_screen(self):
        """Başlangıç splash ekranını gösterir"""
        try:
            splash_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      "assets", "splash.png")
            
            # Splash dosyası yoksa oluşturma
            if not os.path.exists(splash_path):
                return
                
            splash_pixmap = QPixmap(splash_path)
            splash = QSplashScreen(splash_pixmap)
            splash.show()
            splash.showMessage("EV Dashboard Başlatılıyor...", 
                             Qt.AlignBottom | Qt.AlignCenter, Qt.white)
            
            # Birkaç saniye göster
            self.app.processEvents()
            time.sleep(2)
            splash.close()
        except Exception as e:
            print(f"Splash ekranı gösterilirken hata: {e}")
    
    def signal_handler(self, sig, frame):
        """SIGINT sinyali alındığında temiz bir çıkış yapar"""
        print("\nUygulamadan çıkılıyor...")
        try:
            # Arduino bağlantısını kapat
            if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
                self.dashboard.arduino.stop()
        except Exception as e:
            print(f"Bağlantı kapatılırken hata: {e}")
        finally:
            QApplication.quit()
    
    def run(self):
        """Uygulamayı çalıştırır"""
        try:
            # Eğer test modu etkinse, sadece sahte veri ile çalış
            if self.args.test:
                QMessageBox.information(self.dashboard, "Test Modu", 
                                    "Arduino bağlantısı olmadan test modunda çalışılıyor.\n"
                                    "Sahte veriler kullanılacak.")
                
            # Ana döngüyü başlat
            return self.app.exec_()
        except Exception as e:
            print(f"Uygulama çalıştırılırken hata: {e}")
            return 1


if __name__ == "__main__":
    try:
        app = EVDashboardApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"Kritik hata: {e}")
        sys.exit(1)
