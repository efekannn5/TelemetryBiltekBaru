# TelemetryBiltekBaru

Bu proje, TÜBİTAK Efficiency Challenge 2025 kapsamında Efekan Nefesoğlu tarafından geliştirilen elektrikli araç telemetri ve veri izleme sistemidir. Proje, aracın performans verilerini gerçek zamanlı olarak izlemek, kaydetmek ve görselleştirmek için tasarlanmıştır.

## 👨‍💻 Geliştirici

**Efekan Nefesoğlu**
- Bartın Üniversitesi Bilgisayar Programcılığı Öğrencisi
- BiltekBaru Elektrikli Araç Kulübü Üyesi
- E-posta: [efekan@nefesoglu.com](mailto:efekan@nefesoglu.com)
- GitHub: [efekannn5](https://github.com/efekannn5)
- LinkedIn: [Efekan Nefesoğlu](https://www.linkedin.com/in/efekan-nefesoğlu-b4552128b)

### Geliştirici Notları
Bu proje, elektrikli araç telemetri sisteminin geliştirilmesi sürecinde edinilen deneyimler ve çözümler doğrultusunda oluşturulmuştur. Sistem, Raspberry Pi 4B üzerinde çalışacak şekilde optimize edilmiş ve gerçek zamanlı veri akışı için özel olarak tasarlanmıştır.

## 💻 Donanım Özellikleri

### Ana Sistem
- **İşlemci:** Raspberry Pi 4B (2GB RAM)
- **İşletim Sistemi:** Raspberry Pi OS (64-bit)
- **Depolama:** 16GB MicroSD Kart 
- **Ekran:** Waveshare 11.9inch Capacitive 320×1480 Touch Screen LCD Display
- **Güç:** 5V/3A USB-C Güç Kaynağı
- **Mikrodenetleyici:** Arduino Mega 2560

## 🚀 Özellikler

### Veri Toplama ve İzleme
- Arduino tabanlı sensör veri toplama
- Gerçek zamanlı veri izleme ve görselleştirme
- Veri kaydetme ve loglama
- Web tabanlı dashboard arayüzü
- Hata yönetimi ve loglama sistemi
- Cloudflare tüneli ile uzaktan erişim

### İzlenen Parametreler
- Araç hızı (km/h)
- Pil seviyesi ve sıcaklığı
- Motor sıcaklığı
- Güç kullanımı 
- Batarya paketi voltajı ve hücre voltajları
- Kilometre sayacı
- Far durumu ve kör nokta uyarıları
- AKS durumu
- ADAS bilgisi

### Güvenlik Özellikleri
- Kritik sıcaklık uyarıları
- Düşük batarya uyarıları
- Voltaj limit kontrolü
- Hata loglama ve raporlama

## 🛠️ Kurulum ve Kullanım

### 1. Projeyi İndirme
```bash
# Projeyi klonlayın
git clone https://github.com/efekannn5/TelemetryBiltekBaru.git

# Proje dizinine gidin
cd TelemetryBiltekBaru
```

### 2. Gerekli Yazılımların Kurulumu

#### Python Kurulumu
```bash
# Python 3.x'i indirin ve kurun
# Windows için: https://www.python.org/downloads/
# Linux için:
sudo apt-get update
sudo apt-get install python3 python3-pip
```

#### Gerekli Python Paketlerinin Kurulumu
```bash
# Sanal ortam oluşturma (önerilen)
python -m venv venv

# Sanal ortamı aktifleştirme
# Windows için:
venv\Scripts\activate
# Linux/MacOS için:
source venv/bin/activate

# Gerekli paketleri yükleme
pip install -r requirements.txt
```

#### Arduino IDE Kurulumu
1. [Arduino IDE'yi indirin](https://www.arduino.cc/en/software)
2. Kurulumu tamamlayın
3. Gerekli kütüphaneleri yükleyin:
   - ArduinoJson
   - Wire
   - Adafruit_Sensor

### 3. Donanım Kurulumu

#### Raspberry Pi Kurulumu
1. [Raspberry Pi OS'u indirin](https://www.raspberrypi.org/software/)
2. SD karta yazın
3. Raspberry Pi'yi başlatın
4. Sistem güncellemelerini yapın:
```bash
sudo apt-get update
sudo apt-get upgrade
```

#### Ekran Kurulumu
1. Waveshare ekranı Raspberry Pi'ye bağlayın
2. Gerekli sürücüleri yükleyin:
```bash
sudo apt-get install -y python3-pip
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

### 4. Yapılandırma

#### Arduino Yapılandırması
1. `arduino_code.ino` dosyasını Arduino IDE'de açın
2. Kart tipini seçin (Arduino Mega 2560)
3. Port ayarlarını yapın
4. Kodu yükleyin

#### Telemetri Sistemi Yapılandırması
1. `config.json` dosyasını düzenleyin:
```json
{
    "arduino": {
        "port": "/dev/ttyACM0",  // Windows için "COM3" gibi
        "baudrate": 115200
    },
    "display": {
        "width": 1480,
        "height": 320
    }
}
```

### 5. Çalıştırma

#### Normal Mod
```bash
python main.py
```

#### Test Modu
```bash
python main.py -t
```

#### Otomatik Bağlantı
```bash
python main.py -a
```

#### Belirli Port ile Bağlantı
```bash
python main.py -p COM3  # Windows için
python main.py -p /dev/ttyACM0  # Linux için
```

### 6. Uzaktan Erişim

#### Cloudflare Tüneli Kurulumu
1. Cloudflared'ı indirin:
```bash
# Windows için
winget install Cloudflare.cloudflared

# Linux için
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
```

2. Tüneli yapılandırın:
```bash
cloudflared tunnel login
cloudflared tunnel create e-car
```

3. `config.yml` dosyasını düzenleyin:
```yaml
tunnel: e-car
credentials-file: /path/to/credentials.json

ingress:
  - hostname: ecar.efekannefesoglu.com
    service: http://localhost:8000
```

### 7. Sorun Giderme

#### Yaygın Sorunlar ve Çözümleri

1. **Arduino Bağlantı Hatası**
   - Port numarasını kontrol edin
   - Arduino IDE'de doğru kart seçili mi?
   - USB kablosunu değiştirin

2. **Ekran Sorunları**
   - GPIO bağlantılarını kontrol edin
   - Sürücülerin yüklü olduğundan emin olun
   - Raspberry Pi'yi yeniden başlatın

3. **Cloudflare Tüneli Sorunları**
   - İnternet bağlantısını kontrol edin
   - Kimlik bilgilerinin doğru olduğundan emin olun
   - Tünel durumunu kontrol edin: `cloudflared tunnel list`

4. **Python Paket Hataları**
   - Sanal ortamın aktif olduğundan emin olun
   - requirements.txt'yi güncelleyin
   - pip'i güncelleyin: `pip install --upgrade pip`

## 📁 Proje Yapısı

### Ana Dosyalar
- `main.py`: Ana uygulama dosyası
- `dashboard_ui.py`: Dashboard arayüzü
- `serial_reader.py`: Seri port veri okuma
- `logger.py`: Loglama sistemi
- `error_handler.py`: Hata yönetimi

### Arduino Dosyaları
- `arduino_code.ino`: Ana Arduino kodu
- `arduino_test.ino`: Test ve kalibrasyon kodu
- `arduino_serial.py`: Arduino iletişim kütüphanesi

### Dizinler
- `assets/`: Görsel ve medya dosyaları
- `logs/`: Log dosyaları
- `styles/`: UI stil dosyaları

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📊 Veri Akışı

### 1. Veri Toplama
- Arduino sensörlerden veri okur
- JSON formatında veri paketleri oluşturur
- Her veri paketi "#END#" ile sonlandırılır

### 2. Veri İşleme
- `serial_reader.py` verileri alır ve işler
- Veriler doğrulanır ve formatlanır
- Hata kontrolü yapılır

### 3. Veri Görselleştirme
- Dashboard'da gerçek zamanlı gösterim
- Grafikler ve göstergeler güncellenir
- Uyarılar kontrol edilir

### 4. Veri Kaydetme
- Tüm veriler loglanır
- Hata durumları kaydedilir
- Performans metrikleri tutulur

## 🔧 Hata Ayıklama

### Log Dosyaları
- Hata logları: `logs/error.log`
- Veri logları: `logs/data.log`
- Sistem logları: `logs/system.log`

### Hata Yönetimi
- `error_handler.py` hataları yönetir
- Kritik hatalar bildirilir
- Otomatik kurtarma mekanizmaları

### Test Araçları
- `arduino_test.ino`: Seri port testi
- Kalibrasyon araçları
- Performans test araçları

## 🌐 Uzaktan Erişim (Cloudflare Tüneli)

### Cloudflare Tüneli Nedir?
Cloudflare Tüneli (Cloudflared), yerel ağınızdaki servisleri güvenli bir şekilde internete açmanızı sağlayan bir araçtır. Bu projede, telemetri verilerini güvenli bir şekilde dışarıya açmak için kullanılmaktadır.

### Kurulum ve Yapılandırma

1. Cloudflared Kurulumu:
```bash
# Windows için
winget install Cloudflare.cloudflared

# Linux için
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
```

2. Cloudflare Hesabı Oluşturma:
   - Cloudflare hesabı oluşturun
   - DNS ayarlarınızı Cloudflare'a yönlendirin
   - Domain adınızı Cloudflare'a ekleyin

3. Tünel Oluşturma:
```bash
cloudflared tunnel login
cloudflared tunnel create e-car
```

4. Yapılandırma Dosyası (`config.yml`):
```yaml
tunnel: e-car
credentials-file: /path/to/credentials.json

ingress:
  - hostname: ecar.efekannefesoglu.com
    service: http://localhost:8000
  - service: http_status:404
```

5. Tüneli Başlatma:
```bash
cloudflared tunnel run e-car
```

### Güvenlik Özellikleri
- SSL/TLS şifreleme
- DDoS koruması
- IP gizleme
- Otomatik yük dengeleme
- Rate limiting

### Avantajları
- Güvenli bağlantı
- Kolay kurulum
- Ücretsiz kullanım
- Otomatik SSL sertifikası
- Yüksek performans

### Kullanım Senaryoları
1. Yarış Sırasında:
   - Takım üyeleri telemetri verilerini uzaktan izleyebilir
   - Teknik ekip anlık verilere erişebilir
   - Performans analizi yapılabilir

2. Test Sürüşlerinde:
   - Veri toplama ve analiz
   - Gerçek zamanlı izleme
   - Hata ayıklama

3. Eğitim Amaçlı:
   - Öğrenciler telemetri sistemini uzaktan inceleyebilir
   - Demo ve sunumlar için kullanılabilir

### Sorun Giderme
- Bağlantı sorunları için log kontrolü
- DNS ayarlarının doğruluğu
- Tünel durumunun kontrolü
- Port yönlendirme kontrolü

## 📊 Dashboard Bileşenleri

### Ana Bileşenler

1. **CircularGauge (Dairesel Gösterge)**
   - Hız, dönüş göstergesi gibi dairesel değerleri gösterir
   - Animasyonlu geçişler
   - Renk gradyanı ile değer aralıklarını belirtir
   - Özelleştirilebilir açı ve değer aralıkları

2. **BatteryIndicator (Pil Göstergesi)**
   - Pil seviyesini yüzde olarak gösterir
   - Şarj durumunu belirtir
   - Animasyonlu değer değişimleri
   - Kritik seviye uyarıları

3. **TemperatureGauge (Sıcaklık Göstergesi)**
   - Motor ve batarya sıcaklıklarını gösterir
   - Uyarı ve kritik seviye göstergeleri
   - Renk kodlaması ile sıcaklık durumu
   - Özelleştirilebilir sıcaklık aralıkları

4. **BlindSpotIndicator (Kör Nokta Göstergesi)**
   - Sol ve sağ kör nokta uyarıları
   - Animasyonlu uyarı efektleri
   - Görsel ve renk kodlaması
   - Gerçek zamanlı sensör verisi

5. **HeadlightIndicator (Far Göstergesi)**
   - Far durumunu gösterir (Kapalı/Kısa/Uzun)
   - Görsel simgeler
   - Durum değişim animasyonları

6. **GearIndicator (Vites Göstergesi)**
   - Mevcut vites durumunu gösterir (D/N/R)
   - Animasyonlu vites değişimleri
   - Büyük ve okunaklı gösterim
   - Geçiş efektleri

7. **PowerMeter (Güç Göstergesi)**
   - Anlık güç kullanımını gösterir
   - Enerji tüketimi bilgisi
   - Grafiksel gösterim
   - Tarihsel veri takibi

8. **ParkSensorVisual (Park Sensörü Görseli)**
   - Mesafe sensörlerinden gelen verileri gösterir
   - Görsel mesafe göstergeleri
   - Renk kodlaması ile mesafe uyarıları
   - Çoklu sensör desteği

### Panel Düzeni

1. **Sol Panel**
   - Batarya durumu
   - Sıcaklık göstergeleri
   - Sistem durumu

2. **Orta Panel**
   - Hız göstergesi
   - Vites göstergesi
   - Ana bilgi ekranı

3. **Sağ Panel**
   - Güç göstergesi
   - Park sensörü
   - Uyarı göstergeleri

### Özellikler

1. **Veri Görselleştirme**
   - Gerçek zamanlı veri akışı
   - Animasyonlu geçişler
   - Renk kodlaması
   - Grafiksel gösterimler

2. **Uyarı Sistemi**
   - Kritik seviye uyarıları
   - Görsel ve renkli uyarılar
   - Sesli uyarılar
   - Log kayıtları

3. **Veri Kaydı**
   - Telemetri verilerinin kaydı
   - Hata logları
   - Performans metrikleri
   - Tarihsel veri analizi

4. **Özelleştirme**
   - Tema seçenekleri
   - Gösterge düzeni
   - Uyarı eşikleri
   - Görsel ayarlar

### Teknik Özellikler

1. **Performans**
   - Düşük CPU kullanımı
   - Optimize edilmiş animasyonlar
   - Hızlı veri işleme
   - Düşük bellek kullanımı

2. **Güvenilirlik**
   - Hata yakalama
   - Otomatik kurtarma
   - Veri doğrulama
   - Bağlantı kontrolü

3. **Genişletilebilirlik**
   - Yeni gösterge ekleme
   - Özel widget'lar
   - Plugin sistemi
   - API entegrasyonu

## 🎮 Ana Uygulama (main.py)

### Genel Bakış
`main.py`, telemetri sisteminin ana uygulamasıdır. Arduino'dan gelen verileri işler, dashboard'u yönetir ve web arayüzünü sunar.

### Temel Bileşenler

1. **EVDashboardApp Sınıfı**
   - Ana uygulama sınıfı
   - Tüm bileşenleri yönetir
   - Başlatma ve kapatma işlemlerini kontrol eder
   - Hata yönetimini sağlar

2. **Flask Web Sunucusu**
   - Web arayüzünü sunar
   - Telemetri verilerini JSON formatında sağlar
   - Statik dosyaları yönetir
   - API endpoint'leri sunar

3. **Cloudflare Tüneli**
   - Uzaktan erişimi sağlar
   - Güvenli bağlantı yönetimi
   - Otomatik SSL sertifikası
   - Yük dengeleme

### Başlatma Süreci

1. **Argüman Analizi**
   ```python
   -t, --test    # Test modu
   -a, --auto    # Otomatik bağlantı
   -p, --port    # Belirli port ile bağlantı
   ```
    
2. **Başlangıç Kontrolleri**
   - Gerekli dosyaların varlığı
   - Port erişilebilirliği
   - Bağlantı durumu
   - Konfigürasyon kontrolü

3. **Bileşen Başlatma**
   - Dashboard arayüzü
   - Arduino bağlantısı
   - Web sunucusu
   - Cloudflare tüneli

### Veri Akışı

1. **Arduino'dan Veri Alma**
   - Seri port üzerinden veri okuma
   - JSON formatında veri işleme
   - Veri doğrulama
   - Hata kontrolü

2. **Veri İşleme**
   - Veri formatı dönüştürme
   - Değer normalizasyonu
   - Uyarı kontrolü
   - Log kaydı

3. **Veri Dağıtımı**
   - Dashboard güncelleme
   - Web arayüzü güncelleme
   - Log dosyasına kayıt
   - Hata bildirimi

### Güvenlik Özellikleri

1. **Bağlantı Güvenliği**
   - SSL/TLS şifreleme
   - Port kontrolü
   - Bağlantı doğrulama
   - Oturum yönetimi

2. **Veri Güvenliği**
   - Veri doğrulama
   - Hata kontrolü
   - Güvenli veri depolama
   - Erişim kontrolü

3. **Sistem Güvenliği**
   - Hata yakalama
   - Otomatik kurtarma
   - Güvenli kapatma
   - Log yönetimi

### Hata Yönetimi

1. **Bağlantı Hataları**
   - Port bulunamama
   - Bağlantı kopması
   - Veri okuma hatası
   - Timeout durumları

2. **Veri Hataları**
   - Format hataları
   - Eksik veri
   - Geçersiz değerler
   - Senkronizasyon sorunları

3. **Sistem Hataları**
   - Bellek taşması
   - CPU yükü
   - Disk alanı
   - Ağ sorunları

### Performans Optimizasyonu

1. **Bellek Yönetimi**
   - Verimli veri yapıları
   - Önbellek kullanımı
   - Bellek temizleme
   - Kaynak yönetimi

2. **CPU Kullanımı**
   - Asenkron işlemler
   - Thread yönetimi
   - İşlem önceliklendirme
   - Yük dengeleme

3. **Ağ Optimizasyonu**
   - Veri sıkıştırma
   - Batch işlemler
   - Bağlantı havuzu
   - Timeout yönetimi

### Geliştirici Araçları

1. **Test Modu**
   - Sahte veri üretimi
   - Bağlantı simülasyonu
   - Performans testi
   - Hata simülasyonu

2. **Debug Modu**
   - Detaylı loglama
   - Hata izleme
   - Performans metrikleri
   - Bellek analizi

3. **Geliştirme Araçları**
   - Kod analizi
   - Performans profili
   - Bellek profili
   - Test araçları

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📊 Veri Akışı

### 1. Veri Toplama
- Arduino sensörlerden veri okur
- JSON formatında veri paketleri oluşturur
- Her veri paketi "#END#" ile sonlandırılır

### 2. Veri İşleme
- `serial_reader.py` verileri alır ve işler
- Veriler doğrulanır ve formatlanır
- Hata kontrolü yapılır

### 3. Veri Görselleştirme
- Dashboard'da gerçek zamanlı gösterim
- Grafikler ve göstergeler güncellenir
- Uyarılar kontrol edilir

### 4. Veri Kaydetme
- Tüm veriler loglanır
- Hata durumları kaydedilir
- Performans metrikleri tutulur

## 🔧 Hata Ayıklama

### Log Dosyaları
- Hata logları: `logs/error.log`
- Veri logları: `logs/data.log`
- Sistem logları: `logs/system.log`

### Hata Yönetimi
- `error_handler.py` hataları yönetir
- Kritik hatalar bildirilir
- Otomatik kurtarma mekanizmaları

### Test Araçları
- `arduino_test.ino`: Seri port testi
- Kalibrasyon araçları
- Performans test araçları

## 🌐 Uzaktan Erişim (Cloudflare Tüneli)

### Cloudflare Tüneli Nedir?
Cloudflare Tüneli (Cloudflared), yerel ağınızdaki servisleri güvenli bir şekilde internete açmanızı sağlayan bir araçtır. Bu projede, telemetri verilerini güvenli bir şekilde dışarıya açmak için kullanılmaktadır.

### Kurulum ve Yapılandırma

1. Cloudflared Kurulumu:
```bash
# Windows için
winget install Cloudflare.cloudflared

# Linux için
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
```

2. Cloudflare Hesabı Oluşturma:
   - Cloudflare hesabı oluşturun
   - DNS ayarlarınızı Cloudflare'a yönlendirin
   - Domain adınızı Cloudflare'a ekleyin

3. Tünel Oluşturma:
```bash
cloudflared tunnel login
cloudflared tunnel create e-car
```

4. Yapılandırma Dosyası (`config.yml`):
```yaml
tunnel: e-car
credentials-file: /path/to/credentials.json

ingress:
  - hostname: ecar.efekannefesoglu.com
    service: http://localhost:8000
```

5. Tüneli Başlatma:
```bash
cloudflared tunnel run e-car
```

### Güvenlik Özellikleri
- SSL/TLS şifreleme
- DDoS koruması
- IP gizleme
- Otomatik yük dengeleme
- Rate limiting

### Avantajları
- Güvenli bağlantı
- Kolay kurulum
- Ücretsiz kullanım
- Otomatik SSL sertifikası
- Yüksek performans

### Kullanım Senaryoları
1. Yarış Sırasında:
   - Takım üyeleri telemetri verilerini uzaktan izleyebilir
   - Teknik ekip anlık verilere erişebilir
   - Performans analizi yapılabilir

2. Test Sürüşlerinde:
   - Veri toplama ve analiz
   - Gerçek zamanlı izleme
   - Hata ayıklama

3. Eğitim Amaçlı:
   - Öğrenciler telemetri sistemini uzaktan inceleyebilir
   - Demo ve sunumlar için kullanılabilir

### Sorun Giderme
- Bağlantı sorunları için log kontrolü
- DNS ayarlarının doğruluğu
- Tünel durumunun kontrolü
- Port yönlendirme kontrolü

## 📊 Dashboard Bileşenleri

### Ana Bileşenler

1. **CircularGauge (Dairesel Gösterge)**
   - Hız, dönüş göstergesi gibi dairesel değerleri gösterir
   - Animasyonlu geçişler
   - Renk gradyanı ile değer aralıklarını belirtir
   - Özelleştirilebilir açı ve değer aralıkları

2. **BatteryIndicator (Pil Göstergesi)**
   - Pil seviyesini yüzde olarak gösterir
   - Şarj durumunu belirtir
   - Animasyonlu değer değişimleri
   - Kritik seviye uyarıları

3. **TemperatureGauge (Sıcaklık Göstergesi)**
   - Motor ve batarya sıcaklıklarını gösterir
   - Uyarı ve kritik seviye göstergeleri
   - Renk kodlaması ile sıcaklık durumu
   - Özelleştirilebilir sıcaklık aralıkları

4. **BlindSpotIndicator (Kör Nokta Göstergesi)**
   - Sol ve sağ kör nokta uyarıları
   - Animasyonlu uyarı efektleri
   - Görsel ve renk kodlaması
   - Gerçek zamanlı sensör verisi

5. **HeadlightIndicator (Far Göstergesi)**
   - Far durumunu gösterir (Kapalı/Kısa/Uzun)
   - Görsel simgeler
   - Durum değişim animasyonları

6. **GearIndicator (Vites Göstergesi)**
   - Mevcut vites durumunu gösterir (D/N/R)
   - Animasyonlu vites değişimleri
   - Büyük ve okunaklı gösterim
   - Geçiş efektleri

7. **PowerMeter (Güç Göstergesi)**
   - Anlık güç kullanımını gösterir
   - Enerji tüketimi bilgisi
   - Grafiksel gösterim
   - Tarihsel veri takibi

8. **ParkSensorVisual (Park Sensörü Görseli)**
   - Mesafe sensörlerinden gelen verileri gösterir
   - Görsel mesafe göstergeleri
   - Renk kodlaması ile mesafe uyarıları
   - Çoklu sensör desteği

### Panel Düzeni

1. **Sol Panel**
   - Batarya durumu
   - Sıcaklık göstergeleri
   - Sistem durumu

2. **Orta Panel**
   - Hız göstergesi
   - Vites göstergesi
   - Ana bilgi ekranı

3. **Sağ Panel**
   - Güç göstergesi
   - Park sensörü
   - Uyarı göstergeleri

### Özellikler

1. **Veri Görselleştirme**
   - Gerçek zamanlı veri akışı
   - Animasyonlu geçişler
   - Renk kodlaması
   - Grafiksel gösterimler

2. **Uyarı Sistemi**
   - Kritik seviye uyarıları
   - Görsel ve renkli uyarılar
   - Sesli uyarılar
   - Log kayıtları

3. **Veri Kaydı**
   - Telemetri verilerinin kaydı
   - Hata logları
   - Performans metrikleri
   - Tarihsel veri analizi

4. **Özelleştirme**
   - Tema seçenekleri
   - Gösterge düzeni
   - Uyarı eşikleri
   - Görsel ayarlar

### Teknik Özellikler

1. **Performans**
   - Düşük CPU kullanımı
   - Optimize edilmiş animasyonlar
   - Hızlı veri işleme
   - Düşük bellek kullanımı

2. **Güvenilirlik**
   - Hata yakalama
   - Otomatik kurtarma
   - Veri doğrulama
   - Bağlantı kontrolü

3. **Genişletilebilirlik**
   - Yeni gösterge ekleme
   - Özel widget'lar
   - Plugin sistemi
   - API entegrasyonu

## 🎮 Ana Uygulama (main.py)

### Genel Bakış
`main.py`, telemetri sisteminin ana uygulamasıdır. Arduino'dan gelen verileri işler, dashboard'u yönetir ve web arayüzünü sunar.

### Temel Bileşenler

1. **EVDashboardApp Sınıfı**
   - Ana uygulama sınıfı
   - Tüm bileşenleri yönetir
   - Başlatma ve kapatma işlemlerini kontrol eder
   - Hata yönetimini sağlar

2. **Flask Web Sunucusu**
   - Web arayüzünü sunar
   - Telemetri verilerini JSON formatında sağlar
   - Statik dosyaları yönetir
   - API endpoint'leri sunar

3. **Cloudflare Tüneli**
   - Uzaktan erişimi sağlar
   - Güvenli bağlantı yönetimi
   - Otomatik SSL sertifikası
   - Yük dengeleme

### Başlatma Süreci

1. **Argüman Analizi**
   ```python
   -t, --test    # Test modu
   -a, --auto    # Otomatik bağlantı
   -p, --port    # Belirli port ile bağlantı
   ```
    
2. **Başlangıç Kontrolleri**
   - Gerekli dosyaların varlığı
   - Port erişilebilirliği
   - Bağlantı durumu
   - Konfigürasyon kontrolü

3. **Bileşen Başlatma**
   - Dashboard arayüzü
   - Arduino bağlantısı
   - Web sunucusu
   - Cloudflare tüneli

### Veri Akışı

1. **Arduino'dan Veri Alma**
   - Seri port üzerinden veri okuma
   - JSON formatında veri işleme
   - Veri doğrulama
   - Hata kontrolü

2. **Veri İşleme**
   - Veri formatı dönüştürme
   - Değer normalizasyonu
   - Uyarı kontrolü
   - Log kaydı

3. **Veri Dağıtımı**
   - Dashboard güncelleme
   - Web arayüzü güncelleme
   - Log dosyasına kayıt
   - Hata bildirimi

### Güvenlik Özellikleri

1. **Bağlantı Güvenliği**
   - SSL/TLS şifreleme
   - Port kontrolü
   - Bağlantı doğrulama
   - Oturum yönetimi

2. **Veri Güvenliği**
   - Veri doğrulama
   - Hata kontrolü
   - Güvenli veri depolama
   - Erişim kontrolü

3. **Sistem Güvenliği**
   - Hata yakalama
   - Otomatik kurtarma
   - Güvenli kapatma
   - Log yönetimi

### Hata Yönetimi

1. **Bağlantı Hataları**
   - Port bulunamama
   - Bağlantı kopması
   - Veri okuma hatası
   - Timeout durumları

2. **Veri Hataları**
   - Format hataları
   - Eksik veri
   - Geçersiz değerler
   - Senkronizasyon sorunları

3. **Sistem Hataları**
   - Bellek taşması
   - CPU yükü
   - Disk alanı
   - Ağ sorunları

### Performans Optimizasyonu

1. **Bellek Yönetimi**
   - Verimli veri yapıları
   - Önbellek kullanımı
   - Bellek temizleme
   - Kaynak yönetimi

2. **CPU Kullanımı**
   - Asenkron işlemler
   - Thread yönetimi
   - İşlem önceliklendirme
   - Yük dengeleme

3. **Ağ Optimizasyonu**
   - Veri sıkıştırma
   - Batch işlemler
   - Bağlantı havuzu
   - Timeout yönetimi

### Geliştirici Araçları

1. **Test Modu**
   - Sahte veri üretimi
   - Bağlantı simülasyonu
   - Performans testi
   - Hata simülasyonu

2. **Debug Modu**
   - Detaylı loglama
   - Hata izleme
   - Performans metrikleri
   - Bellek analizi

3. **Geliştirme Araçları**
   - Kod analizi
   - Performans profili
   - Bellek profili
   - Test araçları

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```
**Açıklama:** Bu metod, uygulamanın güvenli bir şekilde kapatılmasını sağlar. Arduino bağlantısını kapatır, log dosyalarını kapatır ve timer'ları durdurur.

## 📝 Önemli Metodlar ve Açıklamaları

### 1. Arduino Veri İşleme
```python
def on_arduino_data(self, data):
    """Arduino'dan gelen verileri işler ve dashboard'u günceller"""
    try:
        # Veri doğrulama
        if not self.validate_current_data(data):
            return
            
        # Göstergeleri güncelle
        self.speed_gauge.set_value(data['speed'])
        self.battery_indicator.set_percentage(data['battery_level'])
        self.temp_gauge.set_value(data['battery_temp'])
        
        # Uyarıları kontrol et
        self.check_warnings(data)
        
        # Veriyi logla
        self.log_telemetry_data(data)
        
    except Exception as e:
        self.error_handler.log_error("Veri işleme hatası", str(e))
```
**Açıklama:** Bu metod Arduino'dan gelen ham verileri alır, doğrular ve dashboard'daki göstergeleri günceller. Ayrıca uyarıları kontrol eder ve verileri loglar.

### 2. Otomatik Bağlantı
```python
def auto_connect(self):
    """Son başarılı bağlantı ayarlarını kullanarak Arduino'ya bağlanır"""
    try:
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
```
**Açıklama:** Bu metod, daha önce başarılı olan bağlantı ayarlarını config.json dosyasından okuyarak Arduino'ya otomatik bağlanmayı dener.

### 3. Veri Doğrulama
```python
def validate_current_data(self, data):
    """Gelen verilerin geçerliliğini kontrol eder"""
    required_fields = ['speed', 'battery_level', 'battery_temp', 'motor_temp']
    
    # Gerekli alanların varlığını kontrol et
    if not all(field in data for field in required_fields):
        self.error_handler.log_error("Eksik veri alanları", str(data))
        return False
        
    # Değer aralıklarını kontrol et
    if not (0 <= data['speed'] <= 200):
        self.error_handler.log_error("Geçersiz hız değeri", str(data['speed']))
        return False
        
    if not (0 <= data['battery_level'] <= 100):
        self.error_handler.log_error("Geçersiz batarya seviyesi", str(data['battery_level']))
        return False
        
    return True
```
**Açıklama:** Bu metod, Arduino'dan gelen verilerin geçerliliğini kontrol eder. Gerekli alanların varlığını ve değerlerin mantıklı aralıkta olup olmadığını doğrular.

### 4. Uyarı Kontrolü
```python
def check_warnings(self, data):
    """Kritik durumları kontrol eder ve uyarıları gösterir"""
    warnings = []
    
    # Batarya sıcaklığı kontrolü
    if data['battery_temp'] > 60:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Batarya Sıcaklığı',
            'value': data['battery_temp']
        })
    
    # Motor sıcaklığı kontrolü
    if data['motor_temp'] > 100:
        warnings.append({
            'type': 'critical',
            'message': 'Aşırı Motor Sıcaklığı',
            'value': data['motor_temp']
        })
    
    # Düşük batarya kontrolü
    if data['battery_level'] < 10:
        warnings.append({
            'type': 'warning',
            'message': 'Düşük Batarya',
            'value': data['battery_level']
        })
    
    # Uyarıları göster
    if warnings:
        self.show_warnings(warnings)
```
**Açıklama:** Bu metod, gelen verilerdeki kritik durumları kontrol eder ve gerekirse uyarıları gösterir. Batarya sıcaklığı, motor sıcaklığı ve batarya seviyesi gibi önemli parametreleri izler.

### 5. Veri Loglama
```python
def log_telemetry_data(self, data):
    """Telemetri verilerini log dosyasına kaydeder"""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'data': data
        }
        
        # JSON formatında logla
        with open('logs/telemetry.log', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
            
        # Kritik verileri ayrıca kaydet
        if self.is_critical_data(data):
            self.log_critical_data(log_entry)
            
    except Exception as e:
        self.error_handler.log_error("Log yazma hatası", str(e))
```
**Açıklama:** Bu metod, telemetri verilerini zaman damgası ile birlikte log dosyasına kaydeder. Kritik veriler ayrı bir dosyaya da kaydedilir.

### 6. Güvenli Kapatma
```python
def signal_handler(self, sig, frame):
    """Uygulamayı güvenli bir şekilde kapatır"""
    print("\nUygulamadan çıkılıyor...")
    try:
        # Arduino bağlantısını kapat
        if hasattr(self.dashboard, 'arduino') and self.dashboard.arduino:
            self.dashboard.arduino.stop()
            
        # Log dosyalarını kapat
        self.logger.close()
        
        # Timer'ları durdur
        self.update_timer.stop()
        self.connection_timer.stop()
        
    except Exception as e:
        print(f"Kapatma sırasında hata: {e}")
    finally:
        QApplication.quit()
```