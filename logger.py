#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Powered by Efekan Nefesoglu

import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

class EVLogger:
    """EV Dashboard için gelişmiş loglama sistemi"""
    
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.ensure_log_directory()
        self.setup_logger()
        
    def ensure_log_directory(self):
        """Log klasörünün varlığını kontrol eder ve yoksa oluşturur"""
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
            except Exception as e:
                print(f"Log klasörü oluşturulamadı: {e}")
                self.log_dir = "."  # Varsayılan dizini kullan
                
    def setup_logger(self):
        """Logger'ı yapılandırır"""
        try:
            # Ana logger'ı oluştur
            self.logger = logging.getLogger('EVDashboard')
            self.logger.setLevel(logging.DEBUG)
            
            # Log dosyası formatı
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)s] - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Günlük log dosyası (her gün için ayrı dosya)
            daily_log_file = os.path.join(
                self.log_dir,
                f"ev_dashboard_{datetime.now().strftime('%Y%m%d')}.log"
            )
            
            # Dosya handler'ı (maksimum 10MB, 30 dosya rotasyonu)
            file_handler = RotatingFileHandler(
                daily_log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=30
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            
            # Konsol handler'ı
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)
            
            # Handler'ları logger'a ekle
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Logger yapılandırılamadı: {e}")
            self.logger = logging.getLogger('Fallback')
            self.logger.addHandler(logging.StreamHandler())
            
    def log_error(self, message, exception=None):
        """Hata mesajını loglar"""
        if exception:
            self.logger.error(f"{message}: {str(exception)}")
        else:
            self.logger.error(message)
            
    def log_warning(self, message):
        """Uyarı mesajını loglar"""
        self.logger.warning(message)
        
    def log_info(self, message):
        """Bilgi mesajını loglar"""
        self.logger.info(message)
        
    def log_debug(self, message):
        """Debug mesajını loglar"""
        self.logger.debug(message)
        
    def log_critical(self, message, exception=None):
        """Kritik hata mesajını loglar"""
        if exception:
            self.logger.critical(f"{message}: {str(exception)}")
        else:
            self.logger.critical(message)
            
    def log_data_error(self, data_type, error, raw_data=None):
        """Veri hatalarını loglar"""
        message = f"Veri hatası ({data_type}): {error}"
        if raw_data:
            message += f"\nHam veri: {raw_data}"
        self.logger.error(message)
        
    def log_connection_status(self, connected, port=None, message=None):
        """Bağlantı durumunu loglar"""
        if connected:
            self.logger.info(f"Bağlantı başarılı{f' ({port})' if port else ''}")
        else:
            self.logger.warning(f"Bağlantı kesildi{f': {message}' if message else ''}")
            
    def log_recovery_attempt(self, issue, action, success=None):
        """Hata düzeltme girişimlerini loglar"""
        if success is None:
            self.logger.info(f"Düzeltme girişimi - Sorun: {issue}, Eylem: {action}")
        elif success:
            self.logger.info(f"Düzeltme başarılı - Sorun: {issue}, Eylem: {action}")
        else:
            self.logger.warning(f"Düzeltme başarısız - Sorun: {issue}, Eylem: {action}")
            
    def get_recent_errors(self, count=10):
        """Son hataları getirir"""
        try:
            errors = []
            with open(os.path.join(self.log_dir, 
                     f"ev_dashboard_{datetime.now().strftime('%Y%m%d')}.log")) as f:
                for line in f:
                    if "[ERROR]" in line or "[CRITICAL]" in line:
                        errors.append(line.strip())
            return errors[-count:]
        except Exception:
            return [] 