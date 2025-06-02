from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QProgressBar, QFrame, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect,
                             QMessageBox, QPushButton, QDialog, QLineEdit, QFormLayout, QDialogButtonBox)
from PyQt5.QtCore import Qt, QTimer, QSize, QRect, QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal, pyqtProperty, pyqtSlot, QRectF, QPointF
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen, QRadialGradient, QLinearGradient, QConicalGradient, QPixmap, QIcon, QPolygon, QImage
import os
import math
import time
import json
import serial.tools.list_ports
from arduino_serial import ArduinoSerial
from logger import EVLogger
from error_handler import ErrorHandler

class CircularGauge(QWidget):
    """Dairesel gösterge (hız, dönüş göstergesi, vb. için)"""
    
    def __init__(self, parent=None, min_value=0, max_value=180, start_angle=210, end_angle=-90):
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value
        self._gauge_value = min_value  # Değişken adı _gauge_value olarak değiştirildi
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.gauge_width = 10
        self.text_size = 62
        self.unit_size = 25
        self.text_value = "0"
        self.unit_text = "km/h"
        self.color_start = QColor(0, 230, 118)  # Yeşil
        self.color_end = QColor(244, 67, 54)    # Kırmızı
        self.bg_color = QColor(26, 31, 46)      # Koyu mavi-gri
        
        # Animasyon için
        self.animation = QPropertyAnimation(self, b"gauge_value")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def set_value(self, value):
        """Değeri ayarlar ve animasyonu başlatır"""
        if value == self._gauge_value:  # _gauge_value kullanıldı
            return
            
        value = max(self.min_value, min(value, self.max_value))
        
        self.animation.stop()
        self.animation.setStartValue(self._gauge_value)  # _gauge_value kullanıldı
        self.animation.setEndValue(value)
        self.animation.start()
        
    def get_value(self):
        return self._gauge_value  # _gauge_value kullanıldı
    
    # Property getter/setter metotları
    def get_gauge_value(self):
        return self._gauge_value
        
    def set_gauge_value(self, value):
        self._gauge_value = value
        self.update()
        
    # PyQt property tanımı
    gauge_value = pyqtProperty(float, get_gauge_value, set_gauge_value)
        
    def set_text(self, text):
        self.text_value = text
        self.update()
        
    def paintEvent(self, event):
        """Dairesel göstergeyi çizer"""
        width = self.width()
        height = self.height()
        size = min(width, height)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Merkez
        center = self.rect().center()
        
        # Dış çerçeve çizimi
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.bg_color))
        
        outer_radius = int(size / 2 - 10)
        gauge_rect = QRect(int(center.x() - outer_radius), int(center.y() - outer_radius),
                          int(outer_radius * 2), int(outer_radius * 2))
        
        # Arka plan gösterge
        painter.drawEllipse(gauge_rect)
        
        # Toplam açı genişliği
        angle_range = abs(self.end_angle - self.start_angle)
        
        # Gösterge çizimi
        if self._gauge_value > self.min_value:  # _gauge_value kullanıldı
            # Değerin açı karşılığı
            value_angle = self.start_angle - (angle_range * (self._gauge_value - self.min_value) / 
                                             (self.max_value - self.min_value))  # _gauge_value kullanıldı
            
            # Gradient oluşturma - çok daha yumuşak geçişli
            gradient = QConicalGradient(center, -self.start_angle)
            # Yeşilden maviye
            gradient.setColorAt(0.0, QColor(0, 230, 118))     # Parlak yeşil
            gradient.setColorAt(0.2, QColor(33, 150, 243))    # Mavi
            # Maviden turuncuya
            gradient.setColorAt(0.4, QColor(33, 150, 243))    # Mavi
            gradient.setColorAt(0.5, QColor(255, 152, 0))     # Turuncu
            gradient.setColorAt(0.6, QColor(255, 152, 0))     # Turuncu
            # Turuncudan kırmızıya
            gradient.setColorAt(1.0, QColor(255, 87, 34))     # Koyu turuncu
            gradient.setColorAt(0.9, QColor(255, 87, 34))     # Koyu turuncu
            gradient.setColorAt(0.8, QColor(244, 67, 54))     # Kırmızı
            gradient.setColorAt(0.7, QColor(244, 67, 54))     # Kırmızı
            
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QBrush(gradient), self.gauge_width, Qt.SolidLine, Qt.RoundCap))
            
            # Değere göre yay çizimi
            painter.drawArc(
                gauge_rect,
                int(self.start_angle * 16),
                int((value_angle - self.start_angle) * 16)
            )
        
        # Metin çizimi
        painter.setPen(QColor(255, 255, 255))
        font = QFont()
        font.setPointSize(self.text_size)
        font.setBold(True)
        painter.setFont(font)
        
        text_rect = QRect(int(center.x() - 100), int(center.y() - 50), 200, 100)
        painter.drawText(text_rect, Qt.AlignCenter, self.text_value)
        
        # Birim çizimi
        font.setPointSize(self.unit_size)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor(138, 147, 178))  # Gri ton
        
        unit_rect = QRect(int(center.x() - 50), int(center.y() + 30), 100, 40)
        painter.drawText(unit_rect, Qt.AlignCenter, self.unit_text)


class BatteryIndicator(QWidget):
    """Modern pil göstergesi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._percentage_value = 0  # Tamamen farklı bir değişken adı kullanıyoruz
        self.charging = False
        self.setMinimumSize(120, 40)
        
        # Animasyon için
        self.animation = QPropertyAnimation(self, b"percentage_animated")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def set_percentage(self, percentage):
        """Pil yüzdesini ayarlar ve animasyonu başlatır"""
        if percentage == self._percentage_value:
            return
            
        percentage = max(0, min(percentage, 100))
        
        self.animation.stop()
        self.animation.setStartValue(self._percentage_value)
        self.animation.setEndValue(percentage)
        self.animation.start()
        
    def get_percentage(self):
        return self._percentage_value
        
    def set_charging(self, charging):
        self.charging = charging
        self.update()
    
    # Property getter/setter metotları
    def get_percentage_animated(self):
        return self._percentage_value
        
    def set_percentage_animated(self, value):
        self._percentage_value = value
        self.update()
        
    # PyQt property tanımı
    percentage_animated = pyqtProperty(float, get_percentage_animated, set_percentage_animated)
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Pil simgesi çizimi
        battery_rect = QRectF(0, height * 0.1, width * 0.7, height * 0.8)
        cap_rect = QRectF(width * 0.7, height * 0.3, width * 0.1, height * 0.4)
        
        # Arka plan
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(26, 31, 46))
        painter.drawRoundedRect(battery_rect, 5, 5)
        painter.drawRoundedRect(cap_rect, 2, 2)
        
        # Doluluk seviyesi
        fill_width = battery_rect.width() * (self._percentage_value / 100)
        fill_rect = QRectF(battery_rect.x(), battery_rect.y(), fill_width, battery_rect.height())
        
        if self._percentage_value > 60:
            fill_color = QColor(0, 230, 118)  # Yeşil
        elif self._percentage_value > 20:
            fill_color = QColor(255, 145, 0)  # Turuncu
        else:
            fill_color = QColor(244, 67, 54)  # Kırmızı
            
        painter.setBrush(fill_color)
        painter.drawRoundedRect(fill_rect, 5, 5)
        
        # Yüzde değeri
        painter.setPen(Qt.white)
        font = painter.font()
        font.setPointSize(12)
        painter.setFont(font)
        
        # Float değeri tek ondalık basamağa yuvarla
        percentage_text = f"{self._percentage_value:.1f}%"
        painter.drawText(battery_rect, Qt.AlignCenter, percentage_text)


class TemperatureGauge(QWidget):
    """Sıcaklık göstergesi"""
    
    def __init__(self, parent=None, min_value=0, max_value=100):
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value
        self._value = min_value  # Değişken adı _value olarak değiştirildi
        self.critical_value = max_value * 0.8
        self.warning_value = max_value * 0.6
        self.title = "Sıcaklık"
        self.unit = "°C"
        
        # Animasyon için
        self.animation = QPropertyAnimation(self, b"temperature_value")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def set_value(self, value):
        """Değeri ayarlar ve animasyonu başlatır"""
        if value == self._value:  # _value kullanıldı
            return
            
        value = max(self.min_value, min(value, self.max_value))
        
        self.animation.stop()
        self.animation.setStartValue(self._value)  # _value kullanıldı
        self.animation.setEndValue(value)
        self.animation.start()
        
    def get_value(self):
        return self._value  # _value kullanıldı

    # Property getter/setter metotları
    def get_temperature_value(self):
        return self._value
        
    def set_temperature_value(self, value):
        self._value = value
        self.update()
        
    # PyQt property tanımı
    temperature_value = pyqtProperty(float, get_temperature_value, set_temperature_value)
        
    def set_title(self, title):
        self.title = title
        self.update()
        
    def set_unit(self, unit):
        self.unit = unit
        self.update()
    
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Başlık çizimi
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor(138, 147, 178))
        
        title_rect = QRect(0, 0, width, 20)
        painter.drawText(title_rect, Qt.AlignLeft | Qt.AlignVCenter, self.title)
        
        # Değer çizimi
        font.setPointSize(16)
        font.setBold(True)
        painter.setFont(font)
        
        # Değere göre renk
        if self._value >= self.critical_value:  # _value kullanıldı
            painter.setPen(QColor(244, 67, 54))  # Kırmızı
        elif self._value >= self.warning_value:  # _value kullanıldı
            painter.setPen(QColor(255, 152, 0))  # Turuncu
        else:
            painter.setPen(QColor(255, 255, 255))
            
        value_rect = QRect(0, 20, int(width - 40), 30)
        painter.drawText(value_rect, Qt.AlignRight | Qt.AlignVCenter, str(int(self._value)))  # _value kullanıldı
        
        # Birim çizimi
        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor(138, 147, 178))
        
        unit_rect = QRect(int(width - 40), 20, 40, 30)
        painter.drawText(unit_rect, Qt.AlignLeft | Qt.AlignVCenter, self.unit)
        
        # Gösterge çizimi
        gauge_height = 6
        gauge_rect = QRect(0, int(height - gauge_height), int(width), gauge_height)
        
        # Arka plan
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(26, 31, 46))
        painter.drawRoundedRect(gauge_rect, 3, 3)
        
        # Değer göstergesi
        if self._value > self.min_value:  # _value kullanıldı
            fill_width = int(gauge_rect.width() * (self._value - self.min_value) / (self.max_value - self.min_value))  # _value kullanıldı
            fill_rect = QRect(int(gauge_rect.x()), int(gauge_rect.y()), fill_width, gauge_rect.height())
            
            # Gradient dolgu
            gradient = QLinearGradient(0, 0, width, 0)
            gradient.setColorAt(0, QColor(33, 150, 243))  # Mavi
            gradient.setColorAt(0.6, QColor(255, 152, 0)) # Turuncu
            gradient.setColorAt(1, QColor(244, 67, 54))   # Kırmızı
            
            painter.setBrush(gradient)
            painter.drawRoundedRect(fill_rect, 3, 3)


class BlindSpotIndicator(QWidget):
    """Kör nokta uyarı göstergesi"""
    
    def __init__(self, parent=None, side="left"):
        super().__init__(parent)
        self.side = side  # "left" veya "right"
        self.active = False
        self.alpha = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.pulse)
        self.pulse_direction = 1
        
        # İkon yükleme
        icon_path = f"assets/icons/blindspot_{side}.png"
        self.icon = QPixmap(icon_path)
        if self.icon.isNull():
            print(f"Uyarı: {icon_path} yüklenemedi!")
        
        # Widget boyutunu sabitle
        self.setFixedSize(60, 60)  # Her iki tarafta da aynı boyut
        
    def set_active(self, active):
        """Kör nokta uyarısını etkinleştirir/devre dışı bırakır"""
        if active == self.active:
            return
            
        self.active = active
        
        if active:
            self.timer.start(50)  # 50ms'de bir puls efekti
            self.alpha = 255  # Başlangıçta tam opaklık
        else:
            self.timer.stop()
            self.alpha = 0
            
        self.update()
        
    def pulse(self):
        """Yanıp sönme efekti için alfa değerini değiştirir"""
        self.alpha = int(self.alpha + (15 * self.pulse_direction))  # Daha hızlı yanıp sönme
        
        if self.alpha >= 255:
            self.alpha = 255
            self.pulse_direction = -1
        elif self.alpha <= 150:  # Minimum değer artırıldı
            self.alpha = 150
            self.pulse_direction = 1
            
        self.update()
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arka plan (yuvarlak panel)
        painter.setPen(Qt.NoPen)
        
        if not self.active:
            painter.setBrush(QColor(26, 31, 46))
        else:
            # Daha parlak ve belirgin kırmızı arka plan
            base_color = QColor(255, 50, 50)  # Daha parlak kırmızı
            painter.setBrush(QColor(base_color.red(), 
                                  base_color.green(), 
                                  base_color.blue(), 
                                  self.alpha))
            
            # Ekstra parlama efekti
            glow = QRadialGradient(width/2, height/2, width/2)
            glow.setColorAt(0, QColor(255, 0, 0, self.alpha))
            glow.setColorAt(1, QColor(255, 0, 0, 0))
            painter.setBrush(glow)
            
        painter.drawEllipse(0, 0, width, height)
        
        # İkon çizimi
        if not self.icon.isNull():
            # İkonu widget boyutuna ölçekle (biraz daha küçük)
            icon_size = min(width, height) * 0.6  # 0.7'den 0.6'ya küçültüldü
            scaled_icon = self.icon.scaled(QSize(int(icon_size), int(icon_size)), 
                                         Qt.KeepAspectRatio, 
                                         Qt.SmoothTransformation)
            
            # İkonu ortala
            x = (width - scaled_icon.width()) // 2
            y = (height - scaled_icon.height()) // 2
            
            if not self.active:
                # İkon rengini grileştir
                painter.setOpacity(0.5)
            else:
                painter.setOpacity(1.0)
                
            painter.drawPixmap(x, y, scaled_icon)


class BlinkIndicator(QWidget):
    """Sinyal göstergesi"""
    
    def __init__(self, parent=None, side="left"):
        super().__init__(parent)
        self.side = side  # "left" veya "right"
        self.active = False
        self.alpha = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.blink)
        self.blink_state = False
        self.blink_counter = 0
        
    def set_active(self, active):
        """Sinyal göstergesini etkinleştirir/devre dışı bırakır"""
        if active == self.active:
            return
            
        self.active = active
        
        if active:
            self.timer.start(500)  # 500ms'de bir yanıp sönme
            self.blink_state = True
            self.alpha = 255
        else:
            self.timer.stop()
            self.blink_state = False
            self.alpha = 0
            
        self.update()
        
    def blink(self):
        """Yanıp sönme efekti"""
        self.blink_state = not self.blink_state
        self.alpha = 255 if self.blink_state else 0
            
        self.update()
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Üçgen çizimi
        points = []
        
        if self.side == "left":
            points.append(QPoint(int(width * 0.3), int(height/2)))
            points.append(QPoint(int(width * 0.8), int(height * 0.2)))
            points.append(QPoint(int(width * 0.8), int(height * 0.8)))
        else:  # right
            points.append(QPoint(int(width * 0.7), int(height/2)))
            points.append(QPoint(int(width * 0.2), int(height * 0.2)))
            points.append(QPoint(int(width * 0.2), int(height * 0.8)))
            
        painter.setPen(Qt.NoPen)
        
        if self.blink_state and self.active:
            # Aktif durumda ve yanıp sönerken
            painter.setBrush(QColor(0, 230, 118, self.alpha))
        else:
            # Devre dışı veya sönük durumda
            painter.setBrush(QColor(70, 75, 95))
            
        painter.drawPolygon(points)


class HeadlightIndicator(QWidget):
    """Far göstergesi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = 0  # 0: Kapalı, 1: Kısa far, 2: Uzun far
        self.setFixedSize(40, 40)
        self.icon = QPixmap("assets/icons/headlight.png")
        
    def set_state(self, state):
        """Far durumunu ayarlar"""
        if state != self.state:
            self.state = state
            self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arka plan
        if self.state > 0:
            painter.setPen(Qt.NoPen)
            if self.state == 1:  # Kısa far
                painter.setBrush(QColor(0, 150, 255, 100))  # Açık mavi
            else:  # Uzun far
                painter.setBrush(QColor(0, 150, 255, 200))  # Koyu mavi
            painter.drawEllipse(0, 0, self.width(), self.height())
        
        # İkon çizimi
        if not self.icon.isNull():
            # İkonu widget boyutuna ölçekle
            scaled_icon = self.icon.scaled(self.size() * 0.8, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # İkonu ortala
            x = (self.width() - scaled_icon.width()) // 2
            y = (self.height() - scaled_icon.height()) // 2
            painter.drawPixmap(x, y, scaled_icon)
            
            # Far kapalıysa ikonu grileştir
            if self.state == 0:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(26, 31, 46, 180))  # Yarı saydam koyu renk
                painter.drawRect(0, 0, self.width(), self.height())


class GearIndicator(QWidget):
    """Vites göstergesi widget'ı"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._gear_opacity = 1.0
        self.current_gear = 'N'  # Başlangıçta nötr
        self.target_gear = 'N'
        self.animation = QPropertyAnimation(self, b"gear_opacity")
        self.animation.setDuration(300)  # 300ms animasyon süresi
        self.setMinimumSize(120, 120)
        self.is_animating = False
        self.last_gear_change_time = 0  # Son vites değişim zamanını takip etmek için
        
    def set_gear(self, gear):
        """Vitesi değiştirir ve animasyonu başlatır"""
        if gear not in ['D', 'N', 'R']:
            return
            
        # Eğer aynı vites ve animasyon devam ediyorsa, hiçbir şey yapma
        if gear == self.current_gear and self.is_animating:
            return
            
        # Eğer aynı vites ve animasyon tamamlanmışsa, hiçbir şey yapma
        if gear == self.current_gear and not self.is_animating:
            return
            
        # Son vites değişiminden bu yana yeterli süre geçmediyse, değişikliği yapma
        current_time = time.time()
        if current_time - self.last_gear_change_time < 0.5:  # 500ms minimum bekleme süresi
            return
            
        # Eğer animasyon devam ediyorsa, mevcut animasyonu durdur
        if self.is_animating:
            self.animation.stop()
            self.is_animating = False
            
        self.target_gear = gear
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self._on_fade_out_complete)
        self.animation.start()
        self.is_animating = True
        self.last_gear_change_time = current_time
        
    def _on_fade_out_complete(self):
        """Solma animasyonu tamamlandığında çağrılır"""
        self.current_gear = self.target_gear
        self.animation.finished.disconnect(self._on_fade_out_complete)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.finished.connect(self._on_fade_in_complete)
        self.animation.start()
        
    def _on_fade_in_complete(self):
        """Belirme animasyonu tamamlandığında çağrılır"""
        self.animation.finished.disconnect(self._on_fade_in_complete)
        self.is_animating = False
        
    def get_gear_opacity(self):
        return self._gear_opacity
        
    def set_gear_opacity(self, value):
        self._gear_opacity = value
        self.update()
        
    gear_opacity = pyqtProperty(float, get_gear_opacity, set_gear_opacity)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        size = min(width, height)
        
        # Arka plan daire
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(26, 31, 46))
        painter.drawEllipse(0, 0, size, size)
        
        # Vites harfi
        font = QFont()
        font.setPointSize(int(size * 0.4))
        font.setBold(True)
        painter.setFont(font)
        
        # Vitese göre renk
        if self.current_gear == 'D':
            color = QColor(0, 230, 118)  # Yeşil
        elif self.current_gear == 'R':
            color = QColor(244, 67, 54)  # Kırmızı
        else:  # N
            color = QColor(255, 152, 0)  # Turuncu
            
        painter.setPen(color)
        painter.setOpacity(self._gear_opacity)
        
        # Metni ortala
        text_rect = QRectF(0, 0, size, size)
        painter.drawText(text_rect, Qt.AlignCenter, self.current_gear)
        
        # Parlaklık efekti (sadece animasyon tamamlandığında)
        if not self.is_animating and self._gear_opacity > 0.5:
            glow = QRadialGradient(size/2, size/2, size/2)
            glow.setColorAt(0, QColor(color.red(), color.green(), color.blue(), int(100 * self._gear_opacity)))
            glow.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(glow)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, size, size)


class ParkSensorStatus(QWidget):
    """Park sensörü durum göstergesi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.park_enabled = False
        self.setMinimumSize(140, 35)
        
    def set_status(self, enabled):
        """Park sensörü durumunu ayarlar"""
        if enabled == self.park_enabled:
            return
            
        self.park_enabled = enabled
        self.update()
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arka plan
        painter.setPen(Qt.NoPen)
        if not self.park_enabled:
            # Park sensörü devre dışıyken kırmızımsı arka plan
            painter.setBrush(QColor(46, 31, 31))
        else:
            # Park sensörü aktifken koyu yeşilimsi arka plan
            painter.setBrush(QColor(31, 46, 31))
            
        painter.drawRoundedRect(0, 0, width, height, height/2, height/2)
        
        # Metin çizimi
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        
        if self.park_enabled:
            painter.setPen(QColor(0, 230, 118))  # Yeşil
            status_text = "ADAS ENABLE"
        else:
            painter.setPen(QColor(255, 100, 100))  # Açık kırmızı
            status_text = "ADAS DISABLE"
            
        painter.drawText(0, 0, width, height, Qt.AlignCenter, status_text)


class AksStatus(QWidget):  # DriveMode sınıfını AksStatus olarak değiştirdik
    """AKS durum göstergesi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.aks_enabled = False
        self.setMinimumSize(140, 35)
        
    def set_status(self, enabled):
        """AKS durumunu ayarlar"""
        if enabled == self.aks_enabled:
            return
            
        self.aks_enabled = enabled
        self.update()
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arka plan
        painter.setPen(Qt.NoPen)
        if not self.aks_enabled:
            # AKS devre dışıyken kırmızımsı arka plan
            painter.setBrush(QColor(46, 31, 31))
        else:
            # AKS aktifken koyu yeşilimsi arka plan
            painter.setBrush(QColor(31, 46, 31))
            
        painter.drawRoundedRect(0, 0, width, height, height/2, height/2)
        
        # Metin çizimi
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        
        if self.aks_enabled:
            painter.setPen(QColor(0, 230, 118))  # Yeşil
            status_text = "AKS ENABLE"
        else:
            painter.setPen(QColor(255, 100, 100))  # Açık kırmızı
            status_text = "AKS DISABLE"
            
        painter.drawText(0, 0, width, height, Qt.AlignCenter, status_text)


class PowerMeter(QWidget):
    """Güç kullanım metresi"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.power_usage = 0     # kW
        self.max_power = 150     # kW
        self.energy_used = 0     # kWh
        
    def set_values(self, power_usage, energy_used=None):
        """Güç ve enerji değerlerini ayarlar"""
        self.power_usage = max(0, min(power_usage, self.max_power))
        if energy_used is not None:
            self.energy_used = energy_used
        self.update()
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Arka plan çizimi (yatay çubuk)
        bar_height = int(height * 0.4)  # Biraz daha küçük bar
        bar_y = int((height - bar_height) / 2)
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(26, 31, 46))
        painter.drawRoundedRect(0, bar_y, width, bar_height, 5, 5)
        
        # Güç kullanımı çizimi
        if self.power_usage > 0:
            power_width = int(width * (self.power_usage / self.max_power))
            
            power_rect = QRect(0, bar_y, power_width, bar_height)
            painter.setPen(Qt.NoPen)
            
            gradient = QLinearGradient(0, 0, power_width, 0)
            gradient.setColorAt(0, QColor(33, 150, 243))  # Mavi
            gradient.setColorAt(1, QColor(244, 67, 54))   # Kırmızı
            
            painter.setBrush(gradient)
            painter.drawRoundedRect(power_rect, 5, 5)
        
        # Güç değeri
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        
        power_text = f"{int(self.power_usage)} kW"
        power_rect = QRect(0, 5, width, bar_y - 5)
        painter.drawText(power_rect, Qt.AlignCenter, power_text)
        
        # Enerji tüketimi
        font.setPointSize(10)
        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor(138, 147, 178))
        
        energy_text = f"{int(self.power_usage):.1f} kWh"
        energy_rect = QRect(0, bar_y + bar_height + 5, width, height - (bar_y + bar_height + 5))
        painter.drawText(energy_rect, Qt.AlignCenter, energy_text)


class ParkSensorVisual(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(180, 120)
        self.distances = {
            'left': 0,
            'rear': 0,
            'right': 0
        }
        self.max_distance = 200
        self.warning_distance = 100
        self.critical_distance = 50
        self.enabled = False
        
        self.car_icon = QPixmap("assets/icons/car_side.png")
        if self.car_icon.isNull():
            print("Uyarı: car_side.png yüklenemedi!")
            
    def set_distances(self, left=None, rear=None, right=None):
        if left is not None and left > 0:
            self.distances['left'] = min(left, self.max_distance)
        if rear is not None and rear > 0:
            self.distances['rear'] = min(rear, self.max_distance)
        if right is not None and right > 0:
            self.distances['right'] = min(right, self.max_distance)
        self.update()
        
    def set_enabled(self, enabled):
        if self.enabled != enabled:
            self.enabled = enabled
            self.update()
        
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Araba ikonunu çiz
        if not self.car_icon.isNull():
            icon_width = int(width * 0.6)
            icon_height = int(height * 0.85)
            scaled_icon = self.car_icon.scaled(icon_width, icon_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            x = int((width - scaled_icon.width()) / 2)
            y = int((height - scaled_icon.height()) / 2) + int(height * 0.05)
            
            painter.drawPixmap(x, y, scaled_icon)
            
        # Park sensörü devre dışıysa çizim yapma
        if not self.enabled:
            return
            
        # Sensör göstergeleri için parametreler
        center_x = width / 2
        center_y = height / 2 + icon_height * 0.35
        
        sensors = {
            'left': {'angle': 135, 'distance': self.distances['left']},
            'rear': {'angle': 180, 'distance': self.distances['rear']},
            'right': {'angle': 225, 'distance': self.distances['right']}
        }
        
        for sensor_type, sensor_data in sensors.items():
            base_angle = sensor_data['angle']
            distance = sensor_data['distance']
            
            # Mesafe 0 ise bu sensör için çizim yapma
            if distance == 0:
                continue
                
            for i in range(3):
                radius = (i + 1) * (min(width, height) * 0.06)
                offset = icon_width * 0.2
                
                if sensor_type == 'left':
                    rect = QRectF(
                        center_x - radius - offset * 1.85,
                        center_y - radius + icon_height * -0.50,
                        radius * 2,
                        radius * 2
                    )
                elif sensor_type == 'right':
                    rect = QRectF(
                        center_x - radius + offset * -1.85,
                        center_y - radius + icon_height * -0.10,
                        radius * 2,
                        radius * 2
                    )
                else:  # rear
                    rect = QRectF(
                        center_x - radius + offset * -2.25,
                        center_y - radius + icon_height * -0.30,
                        radius * 2,
                        radius * 2
                    )
                
                if distance <= self.critical_distance:
                    if i == 0:
                        color = QColor(244, 67, 54)  # Kırmızı
                    else:
                        color = QColor(70, 75, 95)  # Pasif gri
                elif distance <= self.warning_distance:
                    if i <= 1:
                        color = QColor(255, 152, 0)  # Turuncu
                    else:
                        color = QColor(70, 75, 95)  # Pasif gri
                else:
                    color = QColor(0, 230, 118)  # Yeşil
                
                pen = QPen(color, 3)
                painter.setPen(pen)
                
                start_angle = (base_angle - 20) * 16
                span_angle = 40 * 16
                painter.drawArc(rect, start_angle, span_angle)


class Dashboard(QMainWindow):
    """Ana dashboard sınıfı"""
    
    def __init__(self, test_mode=False):
        super().__init__()
        
        # Logger ve hata yöneticisini başlat
        self.logger = EVLogger()
        self.error_handler = ErrorHandler(self.logger)
        
        try:
            # Test modu ayarı
            self.test_mode = test_mode
            
            # Arduino bağlantısı için değişken
            self.arduino = None
            
            # Varsayılan veri yapısını oluştur
            self.current_data = {
                "speed": 0,
                "battery_level": 0,
                "battery_temp": 25,
                "motor_temp": 30,
                "power_usage": 0,
                "regen_power": 0,
                "headlights": 0,
                "left_blind_spot": False,
                "right_blind_spot": False,
                "aks_enabled": False,
                "odometer": 0,
                "pack_voltage": 0,
                "min_cell_voltage": 0,
                "max_cell_voltage": 0,
                "instant_power": 0,
                "average_power": 0
            }
            
            # Widget referanslarını başlat
            self.speed_gauge = None
            self.battery_level = None
            self.aks_status = None
            self.power_meter = None
            self.headlight_indicator = None
            self.left_blind_spot = None
            self.right_blind_spot = None
            self.battery_temp_value = None
            self.motor_temp_value = None
            self.pack_voltage_value = None
            self.min_cell_voltage_value = None
            self.max_cell_voltage_value = None
            self.odometer = None
            
            # Konfigürasyon dosyasını yükle
            self.config = self.load_config()
            
            # Pencere ayarları - direksiyonun arkasındaki ekran için optimize edilmiş
            self.setWindowTitle("EV Dashboard")
            self.setFixedSize(1480, 320)  # Yeni ekran boyutu
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #0f1621;
                }
                QFrame {
                    border-radius: 10px;
                    background-color: rgba(26, 31, 46, 0.8);
                }
                QLabel {
                    color: white;
                    font-family: Arial;
                }
            """)
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            
            # Ana widget ve layout
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            
            # Ana düzen
            main_layout = QHBoxLayout(self.central_widget)
            main_layout.setContentsMargins(5, 5, 5, 5)
            main_layout.setSpacing(5)
            
            # Panelleri oluştur
            left_panel = self.create_left_side_panel()
            center_panel = self.create_center_panel()
            right_panel = self.create_right_side_panel()
            # Panelleri ana düzene ekle (genişlik oranları: 1:2:1)
            main_layout.addWidget(left_panel, 1)
            main_layout.addWidget(center_panel, 2)
            main_layout.addWidget(right_panel, 1)
            
            # Otomatik bağlantı ve güncelleme için timer'lar
            self.setup_timers()
            
            # Test için sahte veri veya gerçek bağlantı
            if self.test_mode:
                self.setup_dummy_data()
            else:
                # Otomatik bağlantıyı dene
                QTimer.singleShot(1000, self.try_auto_connect)  # 1 saniye sonra bağlantıyı dene
            
            # Ekranı tam ekran yap
            self.showFullScreen()
            
            self.connection_check_logged = False
            
        except Exception as e:
            self.logger.log_critical("Dashboard başlatma hatası", e)
            raise

    def create_left_side_panel(self):
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 5, 10, 10)
        left_layout.setSpacing(8)

        # Üst kısım için yatay düzen
        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)
        
        # Park sensörü durum göstergesi
        if not hasattr(self, 'park_sensor_status'):
            self.park_sensor_status = ParkSensorStatus()
        top_layout.addWidget(self.park_sensor_status)
        
        # Kör nokta göstergesi
        self.left_blind_spot = BlindSpotIndicator(side="left")
        top_layout.addWidget(self.left_blind_spot)
        
        # Boş bir widget ekle
        spacer = QWidget()
        spacer.setFixedSize(60, 60)  # Kör nokta göstergesiyle aynı boyut
        top_layout.addWidget(spacer)
        
        left_layout.addLayout(top_layout)

        # Tarih ve saat
        datetime_frame = QFrame()
        datetime_layout = QVBoxLayout(datetime_frame)
        datetime_layout.setContentsMargins(5, 5, 5, 5)
        self.time_label = QLabel(time.strftime("%H:%M"))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        self.date_label = QLabel(time.strftime("%d.%m.%Y"))
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("font-size: 12px; color: #aaaaaa;")
        datetime_layout.addWidget(self.time_label)
        datetime_layout.addWidget(self.date_label)
        
        # Uyarı alanı
        self.warning_frame = QFrame()
        self.warning_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px; padding: 6px 4px; margin-top: 6px;")
        warning_layout = QVBoxLayout(self.warning_frame)
        warning_layout.setContentsMargins(4, 4, 4, 4)
        warning_layout.setSpacing(2)
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet("color: #ffb300; font-size: 14px; font-weight: bold;")
        self.warning_label.setAlignment(Qt.AlignCenter)
        warning_layout.addWidget(self.warning_label)
        self.warning_frame.setVisible(False)
        
        left_layout.addWidget(self.warning_frame)
        left_layout.addWidget(datetime_frame)
        
        # Alt kısımda boşluk bırak
        left_layout.addStretch()
        
        # Vites göstergesi
        if not hasattr(self, 'gear_indicator'):
            self.gear_indicator = GearIndicator()
            self.gear_indicator.setFixedSize(100, 100)
        left_layout.addWidget(self.gear_indicator, 0, Qt.AlignCenter)
        
        return left_panel

    def create_center_panel(self):
        center_panel = QWidget()
        center_layout = QHBoxLayout(center_panel)
        center_layout.setContentsMargins(2, 2, 2, 2)
        center_layout.setSpacing(10)

        # Sol bölüm - Hız göstergesi
        speed_frame = QFrame()
        speed_layout = QVBoxLayout(speed_frame)
        speed_layout.setContentsMargins(5, 5, 5, 5)
        if self.speed_gauge is None:
            self.speed_gauge = CircularGauge(min_value=0, max_value=220)
            self.speed_gauge.setFixedSize(280, 280)
            self.speed_gauge.set_text("0")
        speed_layout.addWidget(self.speed_gauge, 0, Qt.AlignCenter)
        center_layout.addWidget(speed_frame)

        # Orta bölüm - AKS durumu, güç kullanımı ve park sensörü
        middle_frame = QFrame()
        middle_layout = QVBoxLayout(middle_frame)
        middle_layout.setContentsMargins(5, 5, 5, 5)
        middle_layout.setSpacing(10)
        
        # Güç kullanımı
        if self.power_meter is None:
            self.power_meter = PowerMeter()
            self.power_meter.setFixedSize(180, 60)
        middle_layout.addWidget(self.power_meter, 0, Qt.AlignCenter)
        
        # AKS durumu
        if self.aks_status is None:
            self.aks_status = AksStatus()
        middle_layout.addWidget(self.aks_status, 0, Qt.AlignCenter)
        
        # Park sensörü görselleştirmesi
        if not hasattr(self, 'park_sensor_visual'):
            self.park_sensor_visual = ParkSensorVisual()
        middle_layout.addWidget(self.park_sensor_visual, 0, Qt.AlignCenter)
        
        center_layout.addWidget(middle_frame)
        return center_panel

    def create_right_side_panel(self):
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 5, 10, 10)  # Sol panel ile aynı margin
        right_layout.setSpacing(8)  # Sol panel ile aynı spacing
        
        # Üst kısım için yatay düzen
        top_layout = QHBoxLayout()
        top_layout.setSpacing(5)
        
        # Boş bir widget ekle
        spacer = QWidget()
        spacer.setFixedSize(60, 60)  # Kör nokta göstergesiyle aynı boyut
        top_layout.addWidget(spacer)
        
        # Kör nokta göstergesi
        self.right_blind_spot = BlindSpotIndicator(side="right")
        top_layout.addWidget(self.right_blind_spot)
        
        # Far göstergesi
        if self.headlight_indicator is None:
            self.headlight_indicator = HeadlightIndicator()
        top_layout.addWidget(self.headlight_indicator)
        
        right_layout.addLayout(top_layout)
        
        # Batarya göstergesi
        if self.battery_level is None:
            self.battery_level = BatteryIndicator()
            self.battery_level.setFixedSize(160, 40)
        right_layout.addWidget(self.battery_level, 0, Qt.AlignCenter)
        
        # Batarya bilgi paneli
        battery_frame = QFrame()
        battery_frame.setObjectName("infoFrame")
        battery_layout = QVBoxLayout(battery_frame)
        battery_layout.setSpacing(8)  # Sol panel ile aynı spacing
        
        # Sıcaklık ve gerilim bilgileri
        temp_layout = QHBoxLayout()
        temp_label = QLabel("Batarya Sıcaklığı:")
        temp_label.setStyleSheet("font-size: 14px;")
        if self.battery_temp_value is None:
            self.battery_temp_value = QLabel("25°C")
            self.battery_temp_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        temp_layout.addWidget(temp_label)
        temp_layout.addWidget(self.battery_temp_value)
        battery_layout.addLayout(temp_layout)
        
        motor_temp_layout = QHBoxLayout()
        motor_temp_label = QLabel("Motor Sıcaklığı:")
        motor_temp_label.setStyleSheet("font-size: 14px;")
        if self.motor_temp_value is None:
            self.motor_temp_value = QLabel("30°C")
            self.motor_temp_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        motor_temp_layout.addWidget(motor_temp_label)
        motor_temp_layout.addWidget(self.motor_temp_value)
        battery_layout.addLayout(motor_temp_layout)
        
        voltage_layout = QHBoxLayout()
        voltage_label = QLabel("Batarya Paketi Gerilimi:")
        voltage_label.setStyleSheet("font-size: 14px;")
        if self.pack_voltage_value is None:
            self.pack_voltage_value = QLabel("400V")
            self.pack_voltage_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        voltage_layout.addWidget(voltage_label)
        voltage_layout.addWidget(self.pack_voltage_value)
        battery_layout.addLayout(voltage_layout)
        
        min_cell_layout = QHBoxLayout()
        min_cell_label = QLabel("Min. Hücre Gerilimi:")
        min_cell_label.setStyleSheet("font-size: 14px;")
        if self.min_cell_voltage_value is None:
            self.min_cell_voltage_value = QLabel("3.2V")
            self.min_cell_voltage_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        min_cell_layout.addWidget(min_cell_label)
        min_cell_layout.addWidget(self.min_cell_voltage_value)
        battery_layout.addLayout(min_cell_layout)
        
        max_cell_layout = QHBoxLayout()
        max_cell_label = QLabel("Max. Hücre Gerilimi:")
        max_cell_label.setStyleSheet("font-size: 14px;")
        if self.max_cell_voltage_value is None:
            self.max_cell_voltage_value = QLabel("4.2V")
            self.max_cell_voltage_value.setStyleSheet("font-size: 14px; font-weight: bold;")
        max_cell_layout.addWidget(max_cell_label)
        max_cell_layout.addWidget(self.max_cell_voltage_value)
        battery_layout.addLayout(max_cell_layout)
        
        right_layout.addWidget(battery_frame)
        right_layout.addStretch()
        
        return right_panel

    def setup_timers(self):
        """Timer'ları ayarlar"""
        try:
            # Saat güncellemesi
            self.time_timer = QTimer(self)
            self.time_timer.timeout.connect(self.update_time)
            self.time_timer.start(1000)
            
            # Bağlantı kontrolü
            self.connection_timer = QTimer(self)
            self.connection_timer.timeout.connect(self.check_connection_status)
            self.connection_timer.start(5000)
            
            # Veri doğrulama ve düzeltme
            self.validation_timer = QTimer(self)
            self.validation_timer.timeout.connect(self.validate_current_data)
            self.validation_timer.start(1000)
            
            self.logger.log_info("Timer'lar başarıyla ayarlandı")
            
        except Exception as e:
            self.logger.log_error("Timer'lar ayarlanırken hata", e)
            
    def try_auto_connect(self):
        """Otomatik bağlantı dener"""
        try:
            # Mevcut portları kontrol et
            available_ports = list(serial.tools.list_ports.comports())
            
            if not available_ports:
                self.logger.log_warning("Kullanılabilir port bulunamadı")
                QTimer.singleShot(5000, self.try_auto_connect)
                return

            # Arduino'yu bulmak için akıllı port seçimi
            arduino_port = None
            
            # 1. Önce Arduino/CH340/CP210x tanımlayıcılarını ara
            for port in available_ports:
                vid_pid = f"{port.vid:04X}:{port.pid:04X}" if port.vid else ""
                desc = str(port.description).lower()
                hwid = str(port.hwid).lower()
                
                # Arduino veya yaygın USB-Serial çipleri için kontrol
                if any(id in desc or id in hwid for id in ['arduino', 'ch340', 'cp210', 'usb serial']):
                    arduino_port = port.device
                    self.logger.log_info("Arduino bağlantı portu bulundu")
                    break
                    
                # VID:PID kontrolü
                arduino_vids = ['2341', '1A86', '10C4']
                if vid_pid and any(vid in vid_pid for vid in arduino_vids):
                    arduino_port = port.device
                    break

            # 2. Tipik Arduino port isimlerini kontrol et
            if not arduino_port:
                for port in available_ports:
                    if any(id in port.device.lower() for id in ['/dev/ttyacm', '/dev/ttyusb', 'com']):
                        arduino_port = port.device
                        break

            # 3. Son çare: İlk seri portu kullan
            if not arduino_port and available_ports:
                arduino_port = available_ports[0].device

            if arduino_port:
                # Bağlantıyı dene
                baudrate = self.config.get('arduino', {}).get('baudrate', 115200)
                if self.connect_arduino(arduino_port, baudrate):
                    self.logger.log_info("Arduino bağlantısı başarılı")
                else:
                    QTimer.singleShot(5000, self.try_auto_connect)
            else:
                QTimer.singleShot(5000, self.try_auto_connect)
            
        except Exception as e:
            self.logger.log_error("Bağlantı hatası", e)
            QTimer.singleShot(5000, self.try_auto_connect)

    def connect_arduino(self, port, baudrate):
        """Arduino ile bağlantı kurar"""
        try:
            # Eğer önceki bağlantı varsa kapat
            if hasattr(self, 'arduino') and self.arduino is not None:
                try:
                    self.arduino.stop()
                    self.arduino = None
                except:
                    pass

            # Port erişilebilirliğini kontrol et
            try:
                test_serial = serial.Serial(port, baudrate, timeout=1)
                test_serial.close()
            except Exception as e:
                return False

            # Yeni bağlantı oluştur
            self.arduino = ArduinoSerial(port=port, baudrate=baudrate)
            
            # Sinyal bağlantılarını kur
            self.arduino.data_received.connect(self.on_arduino_data)
            self.arduino.connection_status.connect(self.on_connection_status)
            
            # Bağlantıyı başlat
            if self.arduino.start():
                self.config['arduino'] = {
                    'port': port,
                    'baudrate': baudrate
                }
                self.save_config()
                return True
                
            return False
            
        except Exception as e:
            self.logger.log_error("Bağlantı hatası", e)
            return False
            
    def on_connection_status(self, connected):
        """Bağlantı durumu değiştiğinde çağrılır"""
        try:
            if connected:
                self.logger.log_info("Arduino bağlantısı aktif")
                # Bağlantı sağlandığında uyarıyı kaldır
                self.warning_frame.setVisible(False)
            else:
                self.logger.log_warning("Arduino bağlantısı kesildi")
                # Tüm değerleri sıfırla
                self.speed_gauge.set_text("0")
                self.speed_gauge.set_value(0)
                self.battery_level.set_percentage(0)
                self.aks_status.set_status(False)
                self.battery_temp_value.setText("0°C")
                self.motor_temp_value.setText("0°C")
                self.pack_voltage_value.setText("0V")
                self.min_cell_voltage_value.setText("0.00V")
                self.max_cell_voltage_value.setText("0.00V")
                self.left_blind_spot.set_active(False)
                self.right_blind_spot.set_active(False)
                self.headlight_indicator.set_state(0)
                self.power_meter.set_values(0, 0)
                if hasattr(self, 'gear_indicator'):
                    self.gear_indicator.set_gear("N")
                
                # Bağlantı uyarısını göster
                warnings = ["AKS DISABLE (Bağlantı Kesildi!)"]
                self.warning_label.setText("\n".join(warnings))
                self.warning_frame.setVisible(True)
                
                if not self.test_mode:
                    QTimer.singleShot(5000, self.try_auto_connect)  # 5 saniye sonra tekrar bağlanmayı dene
                    
        except Exception as e:
            self.logger.log_error("Bağlantı durum kontrolü hatası", e)
            
    def validate_current_data(self):
        """Mevcut verileri doğrular ve düzeltir"""
        try:
            # current_data'nın var olup olmadığını kontrol et
            if not hasattr(self, 'current_data'):
                self.current_data = {}
                self.logger.log_warning("current_data bulunamadı, yeni oluşturuldu")
                
            if not isinstance(self.current_data, dict):
                self.current_data = {}
                self.logger.log_error("Geçersiz veri formatı, sıfırlandı")
                return False
                
            # Eksik anahtarları varsayılan değerlerle doldur
            default_values = {
                "speed": 0,
                "battery_level": 0,
                "battery_temp": 25,
                "motor_temp": 30,
                "power_usage": 0,
                "regen_power": 0,
                "headlights": 0,
                "left_blind_spot": False,
                "right_blind_spot": False,
                "aks_enabled": False,
                "odometer": 0,
                "pack_voltage": 0,
                "min_cell_voltage": 0,
                "max_cell_voltage": 0,
                "instant_power": 0,
                "average_power": 0
            }
            
            for key, default_value in default_values.items():
                if key not in self.current_data:
                    self.current_data[key] = default_value
                    self.logger.log_info(f"Eksik veri anahtarı eklendi: {key}")
                
            # Hız kontrolü
            speed = self.current_data.get("speed", 0)
            if not isinstance(speed, (int, float)) or speed < 0 or speed > 220:
                self.current_data["speed"] = 0
                self.logger.log_warning(f"Geçersiz hız değeri: {speed}")
                
            # Batarya seviyesi kontrolü
            battery = self.current_data.get("battery_level", 0)
            if not isinstance(battery, (int, float)) or battery < 0 or battery > 100:
                self.current_data["battery_level"] = 0
                self.logger.log_warning(f"Geçersiz batarya seviyesi: {battery}")
                
            # Güç kullanımı kontrolü - Negatif değerler regeneratif frenleme için kabul edilebilir
            power = self.current_data.get("power_usage", 0)
            if not isinstance(power, (int, float)) or power < -50 or power > 150:
                self.current_data["power_usage"] = 0
                self.logger.log_warning(f"Geçersiz güç kullanımı: {power}")
                
            # Sıcaklık kontrolü
            bat_temp = self.current_data.get("battery_temp", 25)
            if not isinstance(bat_temp, (int, float)) or bat_temp < -20 or bat_temp > 100:
                self.current_data["battery_temp"] = 25
                self.logger.log_warning(f"Geçersiz batarya sıcaklığı: {bat_temp}")
                
            mot_temp = self.current_data.get("motor_temp", 30)
            if not isinstance(mot_temp, (int, float)) or mot_temp < -20 or mot_temp > 150:
                self.current_data["motor_temp"] = 30
                self.logger.log_warning(f"Geçersiz motor sıcaklığı: {mot_temp}")
                
            return True
                
        except Exception as e:
            self.logger.log_error("Veri doğrulama hatası", e)
            return False
            
    @pyqtSlot(dict)
    def on_arduino_data(self, data):
        """Arduino'dan veri alındığında çağrılır"""
        try:
            # Veriyi doğrula ve düzelt
            validated_data = self.error_handler.validate_data_packet(data)
            
            # Geçerli veriyi sakla
            self.current_data = validated_data
            
            # Arayüzü güncelle
            self.update_data(validated_data)
            
        except Exception as e:
            self.logger.log_error("Veri işleme hatası", e)
            
    def update_data(self, data):
        """Tüm göstergeleri günceller"""
        try:
            self.log_telemetry_data(data)
            if not isinstance(data, dict):
                self.logger.log_error("Geçersiz veri formatı")
                return
                
            # Park sensörü durumu ve mesafe güncellemesi
            if hasattr(self, 'park_sensor_status'):
                park_data = data.get('park_sensor', {})
                park_enabled = park_data.get('enabled', False)
                self.park_sensor_status.set_status(park_enabled)
                
                # Park sensörü mesafelerini güncelle
                if hasattr(self, 'park_sensor_visual'):
                    self.park_sensor_visual.set_enabled(park_enabled)
                    if park_enabled:
                        self.park_sensor_visual.set_distances(
                            left=park_data.get('distance_left', 0),
                            rear=park_data.get('distance_rear', 0),
                            right=park_data.get('distance_right', 0)
                        )
                    else:
                        # Park sensörü devre dışıyken tüm mesafeleri sıfırla
                        self.park_sensor_visual.set_distances(left=0, rear=0, right=0)
                        
            # Hız göstergesi
            speed = data.get("speed", 0)
            self.speed_gauge.set_text(str(int(speed)))
            self.speed_gauge.set_value(speed)
            # Batarya seviyesi
            battery = data.get("battery_level", 0)
            self.battery_level.set_percentage(battery)
            # AKS durumu
            aks_enabled = data.get("aks_enabled", False)
            self.aks_status.set_status(aks_enabled)
            # Sıcaklıklar
            battery_temp = data.get("battery_temp", 25)
            self.battery_temp_value.setText(f"{battery_temp:.1f}°C")
            motor_temp = data.get("motor_temp", 30)
            self.motor_temp_value.setText(f"{motor_temp:.1f}°C")
            # Batarya gerilim değerleri
            pack_voltage = data.get("pack_voltage", 400)
            self.pack_voltage_value.setText(f"{pack_voltage:.1f}V")
            min_cell = data.get("min_cell_voltage", 3.2)
            self.min_cell_voltage_value.setText(f"{min_cell:.2f}V")
            max_cell = data.get("max_cell_voltage", 4.2)
            self.max_cell_voltage_value.setText(f"{max_cell:.2f}V")
            # Kör nokta göstergeleri
            self.left_blind_spot.set_active(data.get("left_blind_spot", False))
            self.right_blind_spot.set_active(data.get("right_blind_spot", False))
            # Far durumu
            self.headlight_indicator.set_state(data.get("headlights", 0))
            # Güç kullanımı ve enerji
            power_usage = data.get("power_usage", 0)
            energy_used = data.get("energy_used", 0)
            self.power_meter.set_values(power_usage, energy_used)
            # Odometer güncellemesi
            odometer = data.get("odometer", 0)
            if self.odometer:
                self.odometer.set_value(odometer)
            # Vites göstergesi güncellemesi
            if hasattr(self, 'gear_indicator'):
                gear = data.get("gear", "N")
                self.gear_indicator.set_gear(gear)
            # AKS devre dışı ise tüm göstergeleri sıfırla ve uyarı göster
            if not data.get("aks_enabled", True):
                self.speed_gauge.set_text("0")
                self.speed_gauge.set_value(0)
                self.battery_level.set_percentage(0)
                self.aks_status.set_status(False)
                self.battery_temp_value.setText("0°C")
                self.motor_temp_value.setText("0°C")
                self.pack_voltage_value.setText("0V")
                self.min_cell_voltage_value.setText("0.00V")
                self.max_cell_voltage_value.setText("0.00V")
                self.left_blind_spot.set_active(False)
                self.right_blind_spot.set_active(False)
                self.headlight_indicator.set_state(0)
                self.power_meter.set_values(0, 0)
                if hasattr(self, 'gear_indicator'):
                    self.gear_indicator.set_gear("N")
                warnings = ["AKS devre dışı!"]
                self.warning_label.setText("\n".join(warnings))
                self.warning_frame.setVisible(True)
                return
            # Uyarı kontrolü (eşikler config dosyasından)
            thresholds = self.config.get("warning_thresholds", {})
            warnings = []
            battery_temp_max = thresholds.get("battery_temp", {}).get("max", 60)
            if data.get("battery_temp", 25) > battery_temp_max:
                warnings.append(f"Aşırı Batarya Sıcaklığı! ({data.get('battery_temp', 25):.1f}°C > {battery_temp_max}°C)")
            motor_temp_max = thresholds.get("motor_temp", {}).get("max", 100)
            if data.get("motor_temp", 30) > motor_temp_max:
                warnings.append(f"Aşırı Motor Sıcaklığı! ({data.get('motor_temp', 30):.1f}°C > {motor_temp_max}°C)")
            min_cell_min = thresholds.get("min_cell_voltage", {}).get("min", 2.8)
            if data.get("min_cell_voltage", 3.2) < min_cell_min:
                warnings.append(f"Düşük Min. Hücre Gerilimi! ({data.get('min_cell_voltage', 3.2):.2f}V < {min_cell_min}V)")
            max_cell_max = thresholds.get("max_cell_voltage", {}).get("max", 4.3)
            if data.get("max_cell_voltage", 4.2) > max_cell_max:
                warnings.append(f"Yüksek Max. Hücre Gerilimi! ({data.get('max_cell_voltage', 4.2):.2f}V > {max_cell_max}V)")
            battery_level_min = thresholds.get("battery_level", {}).get("min", 10)
            if data.get("battery_level", 0) < battery_level_min:
                warnings.append(f"Düşük Batarya Seviyesi! ({data.get('battery_level', 0):.1f}% < {battery_level_min}%)")
            if warnings:
                self.warning_label.setText("\n".join(warnings))
                self.warning_frame.setVisible(True)
            else:
                self.warning_label.setText("Her şey düzgün!")
                self.warning_frame.setVisible(False)

            # ADAS verilerini güncelle
            if 'adas' in data:
                adas_data = data['adas']
                if hasattr(self, 'adas_visual'):
                    self.adas_visual.set_distances(
                        rear=adas_data.get('distance_rear', 0),
                        left=adas_data.get('distance_left', 0),
                        right=adas_data.get('distance_right', 0)
                    )
                    self.adas_visual.set_speed(adas_data.get('speed', 0))
        except Exception as e:
            self.logger.log_error("Veri güncelleme hatası", e)

    def log_telemetry_data(self, data):
        """Her gelen telemetri verisini logs/telemetry_data/ klasöründe günlük dosyaya JSON satırı olarak kaydeder. JSON'daki virgüller noktalı virgül olarak değiştirilir."""
        import datetime
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'telemetry_data')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, datetime.datetime.now().strftime('%Y-%m-%d') + '.log')
        try:
            json_str = json.dumps(data, ensure_ascii=False).replace(',', ';')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json_str + '\n')
        except Exception as e:
            self.logger.log_error('Telemetri verisi kaydedilemedi', e)

    def load_config(self):
        """Yapılandırma dosyasını yükler"""
        default_config = {
            "max_range": 400,
            "battery_level": 80,
            "vehicle_settings": {
                "default_climate_temp": 22,
                "default_fan_speed": 3
            },
            "vehicle_data": {
                "odometer": 12500,
                "climate_temp": 22,
                "outside_temp": 24,
                "show_regen": False
            },
            "arduino": {
                "port": None,
                "baudrate": 115200
            }
        }
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    merged_config = default_config.copy()
                    merged_config.update(loaded_config)
                    return merged_config
            else:
                try:
                    with open(config_path, "w", encoding='utf-8') as f:
                        json.dump(default_config, f, indent=4, ensure_ascii=False)
                except Exception as e:
                    print(f"Varsayılan config dosyası oluşturulamadı: {e}")
                return default_config
        except Exception as e:
            print(f"Konfigürasyon yüklenirken hata oluştu: {e}")
            return default_config

    def save_config(self):
        """Yapılandırma dosyasını güvenli şekilde kaydeder"""
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        try:
            with open(config_path, "w", encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.log_error("Config dosyası kaydedilemedi", e)

    def update_time(self):
        """Saat ve tarihi günceller"""
        if hasattr(self, 'time_label') and self.time_label:
            self.time_label.setText(time.strftime("%H:%M"))
        if hasattr(self, 'date_label') and self.date_label:
            self.date_label.setText(time.strftime("%d.%m.%Y"))

    def check_connection_status(self):
        """Bağlantı durumunu kontrol eder (dummy). Gerektiğinde geliştirilebilir."""
        if not getattr(self, 'connection_check_logged', False):
            self.logger.log_info("Bağlantı kontrolü yapıldı.")
            self.connection_check_logged = True

    def get_telemetry_data(self):
        """En güncel telemetri verisini döndürür"""
        return self.current_data
