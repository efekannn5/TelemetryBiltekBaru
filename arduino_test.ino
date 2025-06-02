#include <ArduinoJson.h>

// Simülasyon için değişkenler
struct VehicleData {
    float speed;
    int batteryLevel;
    float batteryTemp;
    float motorTemp;
    float powerUsage;
    float regenPower;
    int headlights;
    bool leftBlindSpot;
    bool rightBlindSpot;
    bool aksEnabled;
    long odometer;
    float packVoltage;
    float minCellVoltage;
    float maxCellVoltage;
    float instantPower;
    float averagePower;
    char gear;  // Vites durumu: 'D', 'N', 'R'
    // Park sensörü verileri
    bool parkEnabled;
    float parkDistanceRear;  // Arka sensör mesafesi (cm)
    float parkDistanceLeft;  // Sol sensör mesafesi (cm)
    float parkDistanceRight; // Sağ sensör mesafesi (cm)
} vehicle;

// Simülasyon parametreleri
unsigned long lastUpdateTime = 0;
const int UPDATE_INTERVAL = 100; // 100ms
unsigned long simulationStartTime;
float accelerationPhase = 0;
unsigned long lastGearChangeTime = 0;  // Son vites değişim zamanı
const unsigned long GEAR_CHANGE_INTERVAL = 5000;  // Her 5 saniyede bir vites değişimi

// AKS simülasyonu için değişkenler
unsigned long lastAksChangeTime = 0;
const unsigned long AKS_DISABLE_INTERVAL = 30000; // Her 30 saniyede bir AKS'yi devre dışı bırak
const unsigned long AKS_DISABLE_DURATION = 5000;  // 5 saniye boyunca devre dışı tut

// JSON belge ve tampon
StaticJsonDocument<1024> doc;
char jsonBuffer[1024];

void setup() {
    Serial.begin(115200);
    simulationStartTime = millis();
    initializeTestData();
}

void loop() {
    unsigned long currentTime = millis();
    
    // AKS simülasyonu
    simulateAksStatus(currentTime);
    
    if (currentTime - lastUpdateTime >= UPDATE_INTERVAL) {
        if (vehicle.aksEnabled) {
            updateTestData();
        }
        sendTelemetryData();
        lastUpdateTime = currentTime;
    }
}

void simulateAksStatus(unsigned long currentTime) {
    // İlk AKS değişimi için başlangıç zamanını ayarla
    if (lastAksChangeTime == 0) {
        lastAksChangeTime = currentTime;
    }
    
    // AKS'nin devre dışı kalma zamanını kontrol et
    if (vehicle.aksEnabled && 
        (currentTime - lastAksChangeTime >= AKS_DISABLE_INTERVAL)) {
        vehicle.aksEnabled = false;
        lastAksChangeTime = currentTime;
        resetAllValues();
    }
    // AKS'nin tekrar devreye girme zamanını kontrol et
    else if (!vehicle.aksEnabled && 
             (currentTime - lastAksChangeTime >= AKS_DISABLE_DURATION)) {
        vehicle.aksEnabled = true;
        lastAksChangeTime = currentTime;
        initializeTestData();  // AKS tekrar aktif olduğunda değerleri başlat
    }
}

void resetAllValues() {
    vehicle.speed = 0;
    vehicle.batteryLevel = 0;
    vehicle.batteryTemp = 0;
    vehicle.motorTemp = 0;
    vehicle.powerUsage = 0;
    vehicle.regenPower = 0;
    vehicle.headlights = 0;
    vehicle.leftBlindSpot = false;
    vehicle.rightBlindSpot = false;
    vehicle.packVoltage = 0;
    vehicle.minCellVoltage = 0;
    vehicle.maxCellVoltage = 0;
    vehicle.instantPower = 0;
    vehicle.averagePower = 0;
    vehicle.gear = 'N';  // Vitesi nötr konuma al
    // Park sensörü değerlerini sıfırla
    vehicle.parkEnabled = false;
    vehicle.parkDistanceRear = 0;
    vehicle.parkDistanceLeft = 0;
    vehicle.parkDistanceRight = 0;
}

void initializeTestData() {
    vehicle.speed = 0;
    vehicle.batteryLevel = 95;
    vehicle.batteryTemp = 25;
    vehicle.motorTemp = 30;
    vehicle.powerUsage = 0;
    vehicle.regenPower = 0;
    vehicle.headlights = 0;
    vehicle.leftBlindSpot = false;
    vehicle.rightBlindSpot = false;
    vehicle.aksEnabled = true;
    vehicle.gear = 'N';  // Başlangıçta nötr
    // odometer değeri korunuyor
    vehicle.packVoltage = 400;
    vehicle.minCellVoltage = 3.8;
    vehicle.maxCellVoltage = 4.0;
    vehicle.instantPower = 0;
    vehicle.averagePower = 0;
    // Park sensörü başlangıç değerleri
    vehicle.parkEnabled = true;
    vehicle.parkDistanceRear = 200;
    vehicle.parkDistanceLeft = 150;
    vehicle.parkDistanceRight = 150;
}

void updateTestData() {
    // Zaman bazlı simülasyon
    float timeSinceStart = (millis() - simulationStartTime) / 1000.0; // saniye
    accelerationPhase += 0.1;
    
    // Vites değişimi simülasyonu
    unsigned long currentTime = millis();  // currentTime değişkenini tanımla
    if (currentTime - lastGearChangeTime >= GEAR_CHANGE_INTERVAL) {
        // Vitesleri sırayla değiştir: N -> D -> N -> R -> N
        switch (vehicle.gear) {
            case 'N':
                vehicle.gear = 'D';
                break;
            case 'D':
                vehicle.gear = 'N';
                break;
            case 'R':
                vehicle.gear = 'N';
                break;
            default:
                vehicle.gear = 'N';
        }
        lastGearChangeTime = currentTime;
    }
    
    // Hız simülasyonu (vitese göre değişir)
    if (vehicle.gear == 'D') {
        vehicle.speed = 60 + 60 * sin(accelerationPhase * 0.1);
    } else if (vehicle.gear == 'R') {
        vehicle.speed = -20 - 20 * sin(accelerationPhase * 0.1);  // Geri vites için negatif hız
    } else {  // N
        vehicle.speed = 0;  // Nötr vites için hız 0
    }
    
    if (vehicle.speed < 0) vehicle.speed = 0;  // Negatif hızları 0'a çevir
    
    // Güç kullanımı (hıza bağlı)
    vehicle.instantPower = vehicle.speed * 0.5; // Basit bir güç modeli
    vehicle.powerUsage = vehicle.instantPower;
    
    // Batarya seviyesi (zamanla yavaşça azalan)
    vehicle.batteryLevel = 95 - (timeSinceStart / 3600.0) * 5; // Saatte %5 azalma
    if (vehicle.batteryLevel < 0) vehicle.batteryLevel = 0;
    
    // Sıcaklık simülasyonu
    vehicle.batteryTemp = 25 + 15 * sin(timeSinceStart * 0.001);
    vehicle.motorTemp = 30 + 20 * sin(timeSinceStart * 0.002);
    
    // Batarya voltajları
    vehicle.packVoltage = 380 + (vehicle.batteryLevel * 0.2);
    vehicle.minCellVoltage = 3.2 + (vehicle.batteryLevel * 0.01);
    vehicle.maxCellVoltage = vehicle.minCellVoltage + 0.2;
    
    // Kör nokta simülasyonu
    if (random(100) < 5) { // %5 ihtimalle değişim
        vehicle.leftBlindSpot = !vehicle.leftBlindSpot;
    }
    if (random(100) < 5) {
        vehicle.rightBlindSpot = !vehicle.rightBlindSpot;
    }
    
    // Far durumu (gece/gündüz simülasyonu)
    int hour = (int)(timeSinceStart / 3600) % 24;
    vehicle.headlights = (hour < 6 || hour > 18) ? 2 : 0; // Gece tam far, gündüz kapalı
    
    // Ortalama güç hesaplama
    vehicle.averagePower = (vehicle.averagePower * 0.9) + (vehicle.instantPower * 0.1);
    
    // Kilometre sayacı güncelleme
    vehicle.odometer += vehicle.speed / 36000.0; // Her saniye için km artışı

    // Park sensörü mesafelerini her zaman simüle et
    vehicle.parkDistanceRear = 100 + 100 * sin(timeSinceStart * 0.5);
    vehicle.parkDistanceLeft = 50 + 100 * sin(timeSinceStart * 0.3);
    vehicle.parkDistanceRight = 50 + 100 * sin(timeSinceStart * 0.4);
    // Rastgele engel simülasyonu (%10 ihtimalle)
    if (random(100) < 10) {
        int sensor = random(3);  // 0: arka, 1: sol, 2: sağ
        switch(sensor) {
            case 0:
                vehicle.parkDistanceRear = random(30, 80);  // 30-80cm arası
                break;
            case 1:
                vehicle.parkDistanceLeft = random(20, 60);  // 20-60cm arası
                break;
            case 2:
                vehicle.parkDistanceRight = random(20, 60); // 20-60cm arası
                break;
        }
    }
    // Park sensörü ENABLE mantığı: herhangi bir sensör 200cm'den küçükse aktif
    if (vehicle.parkDistanceRear < 200 || vehicle.parkDistanceLeft < 200 || vehicle.parkDistanceRight < 200) {
        vehicle.parkEnabled = true;
    } else {
        vehicle.parkEnabled = false;
    }
}

void sendTelemetryData() {
    // JSON belgesini temizle
    doc.clear();
    
    // Temel araç verileri
    doc["speed"] = vehicle.speed;
    doc["battery_level"] = vehicle.batteryLevel;
    doc["battery_temp"] = vehicle.batteryTemp;
    doc["motor_temp"] = vehicle.motorTemp;
    doc["power_usage"] = vehicle.powerUsage;
    doc["regen_power"] = vehicle.regenPower;
    doc["headlights"] = vehicle.headlights;
    doc["left_blind_spot"] = vehicle.leftBlindSpot;
    doc["right_blind_spot"] = vehicle.rightBlindSpot;
    doc["aks_enabled"] = vehicle.aksEnabled;
    doc["odometer"] = vehicle.odometer;
    doc["pack_voltage"] = vehicle.packVoltage;
    doc["min_cell_voltage"] = vehicle.minCellVoltage;
    doc["max_cell_voltage"] = vehicle.maxCellVoltage;
    doc["instant_power"] = vehicle.instantPower;
    doc["average_power"] = vehicle.averagePower;
    doc["gear"] = String(vehicle.gear);
    
    // Park sensörü verileri
    JsonObject park_sensor = doc.createNestedObject("park_sensor");
    park_sensor["enabled"] = vehicle.parkEnabled;
    park_sensor["distance_rear"] = vehicle.parkDistanceRear;
    park_sensor["distance_left"] = vehicle.parkDistanceLeft;
    park_sensor["distance_right"] = vehicle.parkDistanceRight;
    
    // Veriyi gönder
    Serial.print("DATA:");
    serializeJson(doc, Serial);
    Serial.println("#END#");  // Veri sonu işareti
    Serial.flush();
    
    delay(100); // Gecikme
}