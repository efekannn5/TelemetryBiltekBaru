#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from typing import Dict, Any, Optional, Callable

class ErrorHandler:
    """Hata yönetimi ve otomatik düzeltme sistemi"""
    
    def __init__(self, logger):
        self.logger = logger
        self.last_values = {}  # Son geçerli değerleri saklar
        self.error_counts = {}  # Hata sayılarını takip eder
        self.recovery_attempts = {}  # Düzeltme girişimlerini takip eder
        
    def handle_data_error(self, data_type: str, value: Any, 
                         valid_range: tuple = None) -> Any:
        """Veri hatalarını yönetir ve düzeltmeye çalışır"""
        try:
            # Değer None ise son geçerli değeri kullan
            if value is None:
                if data_type in self.last_values:
                    self.logger.log_recovery_attempt(
                        f"None değer ({data_type})",
                        "Son geçerli değer kullanıldı",
                        True
                    )
                    return self.last_values[data_type]
                return 0  # Varsayılan değer
                
            # Sayısal değer kontrolü
            if isinstance(value, (int, float)):
                if valid_range:
                    min_val, max_val = valid_range
                    if not min_val <= value <= max_val:
                        # Aralık dışı değeri düzelt
                        corrected = max(min_val, min(value, max_val))
                        self.logger.log_recovery_attempt(
                            f"Aralık dışı değer ({data_type}): {value}",
                            f"Değer düzeltildi: {corrected}",
                            True
                        )
                        return corrected
                        
            # Geçerli değeri sakla
            self.last_values[data_type] = value
            return value
            
        except Exception as e:
            self.logger.log_error(f"Veri işleme hatası ({data_type})", e)
            return self.last_values.get(data_type, 0)
            
    def handle_connection_error(self, port: str, 
                              retry_func: Callable) -> bool:
        """Bağlantı hatalarını yönetir"""
        try:
            error_key = f"connection_{port}"
            current_time = time.time()
            
            # Son deneme zamanını kontrol et
            if error_key in self.recovery_attempts:
                last_attempt, attempt_count = self.recovery_attempts[error_key]
                # 30 saniyeden sık deneme yapma
                if current_time - last_attempt < 30:
                    return False
                    
            # Yeniden bağlanmayı dene
            success = retry_func()
            
            if success:
                self.recovery_attempts.pop(error_key, None)
                self.logger.log_recovery_attempt(
                    f"Bağlantı hatası ({port})",
                    "Yeniden bağlantı başarılı",
                    True
                )
                return True
            else:
                # Başarısız denemeyi kaydet
                attempt_count = self.recovery_attempts.get(error_key, (0, 0))[1] + 1
                self.recovery_attempts[error_key] = (current_time, attempt_count)
                self.logger.log_recovery_attempt(
                    f"Bağlantı hatası ({port})",
                    f"Yeniden bağlantı başarısız (Deneme {attempt_count})",
                    False
                )
                return False
                
        except Exception as e:
            self.logger.log_error("Bağlantı hatası yönetimi başarısız", e)
            return False
            
    def validate_data_packet(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Veri paketini doğrular ve düzeltir"""
        valid_data = {}
        
        # Veri aralıkları ve varsayılan değerler
        validations = {
            'speed': (0, 220, 0),
            'battery_level': (0, 100, 80),
            'battery_temp': (0, 80, 25),
            'motor_temp': (0, 120, 35),
            'power_usage': (0, 150, 0),
            'regen_power': (0, 50, 0),
            'range_estimate': (0, 500, 300),
            'odometer': (0, 1000000, 0),
            'climate_temp': (16, 30, 22),
            'climate_fan': (0, 5, 3),
            'outside_temp': (-50, 60, 25)
        }
        
        try:
            for key, value in data.items():
                if key in validations:
                    min_val, max_val, default = validations[key]
                    valid_data[key] = self.handle_data_error(
                        key, value, (min_val, max_val)
                    ) or default
                else:
                    valid_data[key] = value
                    
            # Zorunlu alanları kontrol et
            for key, (_, _, default) in validations.items():
                if key not in valid_data:
                    valid_data[key] = self.last_values.get(key, default)
                    
            return valid_data
            
        except Exception as e:
            self.logger.log_error("Veri paketi doğrulama hatası", e)
            return self.last_values or {k: v[2] for k, v in validations.items()}
            
    def can_retry_operation(self, operation: str, 
                          max_attempts: int = 3, 
                          timeout: int = 300) -> bool:
        """Bir işlemin yeniden denenip denenemeyeceğini kontrol eder"""
        current_time = time.time()
        error_key = f"operation_{operation}"
        
        if error_key in self.recovery_attempts:
            last_attempt, attempt_count = self.recovery_attempts[error_key]
            
            # Zaman aşımını kontrol et
            if current_time - last_attempt > timeout:
                self.recovery_attempts[error_key] = (current_time, 1)
                return True
                
            # Maksimum deneme sayısını kontrol et
            if attempt_count >= max_attempts:
                return False
                
            self.recovery_attempts[error_key] = (current_time, attempt_count + 1)
            return True
            
        self.recovery_attempts[error_key] = (current_time, 1)
        return True 