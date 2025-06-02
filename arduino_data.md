# Arduino'dan Gelen Veriler

Arduino'dan JSON formatında aşağıdaki veriler gönderilecektir:

```json
{
  "speed": 60,                // Araç hızı (km/h)
  "battery_level": 75,        // Pil seviyesi (%)
  "battery_temp": 28,         // Pil sıcaklığı (°C)
  "motor_temp": 42,           // Motor sıcaklığı (°C)
  "power_usage": 15,          // Anlık güç kullanımı (kW)
  "regen_power": 0,           // Rejeneratif frenleme gücü (kW)
  "headlights": 1,            // Far durumu (0: kapalı, 1: kısa, 2: uzun)
  "left_blind_spot": false,   // Sol kör nokta uyarısı
  "right_blind_spot": false,  // Sağ kör nokta uyarısı
  "aks_enabled": true,        // AKS aktif mi?
  "odometer": 12500,          // Kilometre sayacı
  "pack_voltage": 400,        // Batarya paketi voltajı (V)
  "min_cell_voltage": 3.15,   // Minimum hücre voltajı (V)
  "max_cell_voltage": 4.21,   // Maksimum hücre voltajı (V)
  "instant_power": 20,        // Anlık güç (kW)
  "average_power": 15         // Ortalama güç (kW)
}
```

## Uyarı Durumları
Aşağıdaki alanlar kritik eşikleri geçtiğinde arayüzde uyarı olarak gösterilir:
- battery_temp > 60°C : Aşırı Batarya Sıcaklığı
- motor_temp > 100°C : Aşırı Motor Sıcaklığı
- min_cell_voltage < 2.8V : Düşük Hücre Gerilimi
- max_cell_voltage > 4.3V : Yüksek Hücre Gerilimi
- battery_level < 10% : Düşük Batarya Seviyesi

## Veri İletişim Protokolü
Arduino'dan gelen JSON verisi seri port üzerinden iletilecektir. Her veri paketi arasında "#END#" işareti bulunacaktır.
