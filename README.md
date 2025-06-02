# TelemetryBiltekBaru

Bu proje, TÜBİTAK Efficiency Challenge 2025 kapsamında geliştirilen elektrikli araç telemetri ve veri izleme sistemidir. Proje, aracın performans verilerini gerçek zamanlı olarak izlemek, kaydetmek ve görselleştirmek için tasarlanmıştır.

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

## 📋 Gereksinimler

### Yazılım Gereksinimleri
- Python 3.x
- PyQt5 5.15.6
- PySerial 3.5
- Arduino IDE (Arduino kodları için)

### Donanım Gereksinimleri
- Arduino Mega veya benzeri mikrodenetleyici
- Sensörler:
  - Sıcaklık sensörleri
  - Voltaj sensörleri
  - Hız sensörü
  - Akım sensörü
- USB bağlantı kablosu
- Bilgisayar (Windows/Linux/MacOS)

## 🛠️ Kurulum

### 1. Python Ortamının Hazırlanması
```bash
# Sanal ortam oluşturma (önerilen)
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows

# Gerekli paketlerin yüklenmesi
pip install -r requirements.txt
```

### 2. Arduino Kurulumu
1. Arduino IDE'yi yükleyin
2. Gerekli kütüphaneleri yükleyin:
   - ArduinoJson
   - Wire
   - Adafruit_Sensor
3. `arduino_code.ino` dosyasını açın
4. Kart tipini ve port ayarlarını yapın
5. Kodu yükleyin

### 3. Yapılandırma
1. `config.yml` dosyasını düzenleyin:
   ```yaml
   tunnel: e-car
   credentials-file: /path/to/credentials.json
   
   ingress:
     - hostname: ecar.efekannefesoglu.com
       service: http://localhost:8000
   ```

2. `config.json` dosyasını kontrol edin:
   ```json
   {
       "max_range": 400,
       "battery_level": 80,
       "arduino": {
           "port": "/dev/ttyACM0",
           "baudrate": 115200
       }
   }
   ```

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

## 🚀 Kullanım

### Başlatma Modları

1. Normal Başlatma:
```bash
python main.py
```
- Web arayüzü ve dashboard birlikte başlar
- Arduino otomatik olarak aranır
- Cloudflare tüneli aktif olur

2. Test Modu:
```bash
python main.py -t
# veya
python main.py --test
```
- Arduino bağlantısı olmadan çalışır
- Sahte veriler kullanılır
- Web arayüzü ve dashboard çalışır
- Geliştirme ve test için idealdir

3. Otomatik Bağlantı:
```bash
python main.py -a
# veya
python main.py --auto
```
- Son başarılı bağlantı ayarlarını kullanır
- `config.json` dosyasındaki port bilgisini kullanır
- Manuel port seçimine gerek kalmaz

4. Belirli Port ile Başlatma:
```bash
python main.py -p COM3
# veya
python main.py --port /dev/ttyACM0
```
- Belirtilen port üzerinden Arduino'ya bağlanır
- Windows için COM portları (COM1, COM2, vb.)
- Linux için /dev/tty portları (/dev/ttyACM0, /dev/ttyUSB0, vb.)

### Başlatma Parametreleri

| Parametre | Açıklama | Örnek |
|-----------|-----------|--------|
| `-t, --test` | Test modu | `python main.py -t` |
| `-a, --auto` | Otomatik bağlantı | `python main.py -a` |
| `-p, --port` | Belirli port | `python main.py -p COM3` |

### Başlatma Senaryoları

1. Geliştirme Ortamı:
```bash
python main.py -t
```
- Arduino olmadan test
- Hızlı geliştirme
- Web arayüzü testi

2. Yarış Ortamı:
```bash
python main.py -a
```
- Otomatik bağlantı
- Hızlı başlatma
- Güvenilir çalışma

3. Farklı Port Testi:
```bash
python main.py -p /dev/ttyUSB0
```
- Port değişikliği testi
- Farklı Arduino kartları
- Bağlantı sorunları giderme

### Web Arayüzü
- Yerel erişim: `http://localhost:8000`
- Uzak erişim: `https://ecar.efekannefesoglu.com`

### Dashboard Özellikleri
- Gerçek zamanlı veri görselleştirme
- Grafik ve göstergeler
- Uyarı sistemi
- Veri kaydetme ve dışa aktarma

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

## 📝 Lisans

Bu proje CC0 (Creative Commons Zero) lisansı altında lisanslanmıştır. Bu lisans, projeyi herhangi bir amaç için kullanma, değiştirme ve dağıtma özgürlüğü sağlar. Detaylar için `LICENSE` dosyasına bakın.

## 👥 Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

### Katkıda Bulunma Kuralları
- Kod standartlarına uyun
- Test yazın
- Dokümantasyonu güncelleyin
- Pull request açıklaması yazın

## 📞 İletişim ve Destek
- **Geliştirici:** Efekan Nefesoğlu – <efekan8190nefesoglu@gmail.com>  
- **Takım:** BiltekBaru Elektrikli Araç Kulübü – Bartın Üniversitesi  

### GitHub
- Sorularınız veya önerileriniz için GitHub üzerinden issue açabilirsiniz
- Pull request'lerinizi bekliyoruz
- Dokümantasyon geliştirmelerine katkıda bulunabilirsiniz

### Teknik Destek
- Hata raporları için issue açın
- Özellik istekleri için issue açın
- Dokümantasyon hataları için issue açın

## 🔄 Güncellemeler

### v1.0.0
- İlk sürüm
- Temel telemetri özellikleri
- Dashboard arayüzü
- Arduino entegrasyonu

### Gelecek Özellikler
- Web site gorsel iyileştirme

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
