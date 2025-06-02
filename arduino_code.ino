// Powered by Efekan Nefesoglu

#include <ArduinoJson.h>
#include <Wire.h>
#include <mcp_can.h>
#include <SPI.h>
#include <SD.h>

// CAN-BUS Pin tanımları
const int CAN_CS_PIN = 10;
const int CAN_INT_PIN = 2;
const int SD_CS_PIN = 4;  // SD kart CS pini

// CAN-BUS ID'leri
const unsigned long AKS_STATUS_ID = 0x180;  // AKS durum mesajı ID
const unsigned long SPEED_DATA_ID = 0x181;  // Hız verisi ID
const unsigned long BATTERY_DATA_ID = 0x182;  // Batarya verisi ID
const unsigned long TEMP_DATA_ID = 0x183;  // Sıcaklık verisi ID
const unsigned long CELL_VOLTAGE_ID = 0x184; // Hücre voltaj ID
const unsigned long POWER_DATA_ID = 0x185;   // Güç verisi ID

// Sensör pinleri
const int BATTERY_TEMP_PIN = A2;
const int MOTOR_TEMP_PIN = A3;
const int LEFT_BLIND_SPOT_PIN = 5;
const int RIGHT_BLIND_SPOT_PIN = 6;
const int HEADLIGHT_PIN = 4;

// CAN-BUS nesnesi
MCP_CAN CAN(CAN_CS_PIN);

// Sistem değişkenleri
unsigned long lastUpdateTime = 0;
const int UPDATE_INTERVAL = 100; // 100ms (10Hz)
unsigned long lastCanMessageTime = 0;
const unsigned long CAN_TIMEOUT = 1000; // 1 saniye timeout

// Log dosyası ayarları
const char* LOG_FILENAME = "vehicle.csv";
unsigned long lastLogTime = 0;
const int LOG_INTERVAL = 1000; // 1 saniye

// Araç verileri
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
} vehicle;

// JSON belge ve tampon
StaticJsonDocument<1024> doc;
char jsonBuffer[1024];

// --- Uyarı simülasyonu için değişkenler ---
int warningPhase = 0;
int warningCounter = 0;
// ... existing code ...

void setup() {
    // Seri haberleşmeyi başlat
    Serial.begin(115200);
    
    // Pin modlarını ayarla
    pinMode(LEFT_BLIND_SPOT_PIN, INPUT);
    pinMode(RIGHT_BLIND_SPOT_PIN, INPUT);
    pinMode(HEADLIGHT_PIN, INPUT);
    pinMode(CAN_INT_PIN, INPUT);
    
    // SD kartı başlat
    if (!SD.begin(SD_CS_PIN)) {
        Serial.println("SD kart başlatılamadı!");
    } else {
        Serial.println("SD kart başlatıldı!");
        // CSV başlığını yaz (dosya yoksa)
        if (!SD.exists(LOG_FILENAME)) {
            File logFile = SD.open(LOG_FILENAME, FILE_WRITE);
            if (logFile) {
                logFile.println("Timestamp,AKS,Hiz,Batarya%,BataryaSicaklik,MotorSicaklik,Guc,RejenGuc,Farlar,SolKorNokta,SagKorNokta,Kilometre,PaketVoltaj,MinHucreV,MaxHucreV,AnlikGuc,OrtalamaGuc");
                logFile.close();
            }
        }
    }
    
    // CAN-BUS başlatma
    while (CAN.begin(CAN_500KBPS) != CAN_OK) {
        Serial.println("CAN-BUS başlatılamadı, tekrar deneniyor...");
        delay(1000);
    }
    Serial.println("CAN-BUS başlatıldı!");
    
    // Başlangıç değerlerini sıfırla
    memset(&vehicle, 0, sizeof(vehicle));
}

void loop() {
    unsigned long currentTime = millis();
    
    // CAN mesajlarını oku
    readCanMessages();
    
    // CAN timeout kontrolü
    if (currentTime - lastCanMessageTime > CAN_TIMEOUT) {
        resetAllValues();  // Timeout durumunda tüm değerleri sıfırla
        vehicle.aksEnabled = false;
    }
    
    // Sadece AKS aktifse sensör verilerini oku
    if (vehicle.aksEnabled) {
        readSensorData();
    }

    // --- Uyarı simülasyonu ---
    warningCounter++;
    if (warningCounter >= 20) { // Her 20 döngüde bir
        warningCounter = 0;
        warningPhase = random(0, 5); // 0: normal, 1: aşırı batarya sıcaklığı, 2: aşırı motor sıcaklığı, 3: düşük hücre gerilimi, 4: yüksek hücre gerilimi, 5: düşük batarya
        if (warningPhase == 1) vehicle.batteryTemp = 65.0;
        else if (warningPhase == 2) vehicle.motorTemp = 110.0;
        else if (warningPhase == 3) vehicle.minCellVoltage = 2.7;
        else if (warningPhase == 4) vehicle.maxCellVoltage = 4.35;
        else if (warningPhase == 5) vehicle.batteryLevel = 8;
    }
    // --- Uyarı simülasyonu sonu ---

    // Telemetri gönderimi
    if (currentTime - lastUpdateTime >= UPDATE_INTERVAL) {
        sendTelemetryData();
        lastUpdateTime = currentTime;
    }
    
    // Log kaydı
    if (currentTime - lastLogTime >= LOG_INTERVAL) {
        logToSD();
        lastLogTime = currentTime;
    }
}

void readSensorData() {
    // Kör nokta sensörleri
    vehicle.leftBlindSpot = digitalRead(LEFT_BLIND_SPOT_PIN);
    vehicle.rightBlindSpot = digitalRead(RIGHT_BLIND_SPOT_PIN);
    
    // Far durumu
    vehicle.headlights = digitalRead(HEADLIGHT_PIN);
    
    // Sıcaklık sensörleri (analog okuma)
    float rawBatteryTemp = analogRead(BATTERY_TEMP_PIN);
    float rawMotorTemp = analogRead(MOTOR_TEMP_PIN);
    
    // Analog değerleri sıcaklığa çevir
    vehicle.batteryTemp = convertToTemperature(rawBatteryTemp);
    vehicle.motorTemp = convertToTemperature(rawMotorTemp);
}

float convertToTemperature(float rawValue) {
    // 10-bit ADC (0-1023) to temperature conversion
    float voltage = (rawValue / 1023.0) * 5.0;
    return (voltage - 0.5) * 100.0; // LM35 sensör için örnek dönüşüm
}

void readCanMessages() {
    unsigned char len = 0;
    unsigned char buf[8];
    unsigned long canId;
    
    if (CAN_MSGAVAIL == CAN.checkReceive()) {
        CAN.readMsgBuf(&len, buf);
        canId = CAN.getCanId();
        lastCanMessageTime = millis();
        
        switch (canId) {
            case AKS_STATUS_ID:
                processAksStatus(buf, len);
                break;
            case SPEED_DATA_ID:
                processSpeedData(buf, len);
                break;
            case BATTERY_DATA_ID:
                processBatteryData(buf, len);
                break;
            case TEMP_DATA_ID:
                processTempData(buf, len);
                break;
            case CELL_VOLTAGE_ID:
                processCellVoltage(buf, len);
                break;
            case POWER_DATA_ID:
                processPowerData(buf, len);
                break;
        }
    }
}

void processAksStatus(unsigned char *buf, unsigned char len) {
    if (len >= 1) {
        bool newAksState = (buf[0] == 1);
        if (vehicle.aksEnabled && !newAksState) {
            // AKS devre dışı kaldığında tüm değerleri sıfırla
            resetAllValues();
        }
        vehicle.aksEnabled = newAksState;
    }
}

void processSpeedData(unsigned char *buf, unsigned char len) {
    if (len >= 4) {
        // 2 byte hız, 2 byte kilometre sayacı
        vehicle.speed = ((buf[0] << 8) | buf[1]) * 0.1; // km/h
        vehicle.odometer = ((buf[2] << 8) | buf[3]) * 0.1; // km
    }
}

void processBatteryData(unsigned char *buf, unsigned char len) {
    if (len >= 4) {
        vehicle.batteryLevel = buf[0];
        vehicle.packVoltage = ((buf[1] << 8) | buf[2]) * 0.1;
        vehicle.powerUsage = buf[3] * 0.5;
    }
}

void processTempData(unsigned char *buf, unsigned char len) {
    if (len >= 2) {
        // CAN'den gelen sıcaklık verilerini sensör verileriyle karşılaştır
        float canBatteryTemp = buf[0] - 40; // -40 ile +215 arası
        float canMotorTemp = buf[1] - 40;
        
        // Sensör ve CAN verilerinin ortalamasını al
        vehicle.batteryTemp = (vehicle.batteryTemp + canBatteryTemp) / 2;
        vehicle.motorTemp = (vehicle.motorTemp + canMotorTemp) / 2;
    }
}

void processCellVoltage(unsigned char *buf, unsigned char len) {
    if (len >= 4) {
        vehicle.minCellVoltage = ((buf[0] << 8) | buf[1]) * 0.001; // V
        vehicle.maxCellVoltage = ((buf[2] << 8) | buf[3]) * 0.001; // V
    }
}

void processPowerData(unsigned char *buf, unsigned char len) {
    if (len >= 4) {
        vehicle.instantPower = ((buf[0] << 8) | buf[1]) * 0.1; // kW
        vehicle.averagePower = ((buf[2] << 8) | buf[3]) * 0.1; // kW
        
        // Rejeneratif frenleme gücü (negatif güç)
        vehicle.regenPower = vehicle.instantPower < 0 ? -vehicle.instantPower : 0;
    }
}

void sendTelemetryData() {
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
    
    // JSON verisini gönder
    serializeJson(doc, Serial);
    Serial.println();
    Serial.println("#END#");
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
    // odometer değeri sıfırlanmıyor çünkü bu toplam değer
}

void logToSD() {
    File logFile = SD.open(LOG_FILENAME, FILE_WRITE);
    if (logFile) {
        // Zaman damgası
        logFile.print(millis());
        logFile.print(",");
        
        // Araç verileri
        logFile.print(vehicle.aksEnabled);
        logFile.print(",");
        logFile.print(vehicle.speed);
        logFile.print(",");
        logFile.print(vehicle.batteryLevel);
        logFile.print(",");
        logFile.print(vehicle.batteryTemp);
        logFile.print(",");
        logFile.print(vehicle.motorTemp);
        logFile.print(",");
        logFile.print(vehicle.powerUsage);
        logFile.print(",");
        logFile.print(vehicle.regenPower);
        logFile.print(",");
        logFile.print(vehicle.headlights);
        logFile.print(",");
        logFile.print(vehicle.leftBlindSpot);
        logFile.print(",");
        logFile.print(vehicle.rightBlindSpot);
        logFile.print(",");
        logFile.print(vehicle.odometer);
        logFile.print(",");
        logFile.print(vehicle.packVoltage);
        logFile.print(",");
        logFile.print(vehicle.minCellVoltage);
        logFile.print(",");
        logFile.print(vehicle.maxCellVoltage);
        logFile.print(",");
        logFile.print(vehicle.instantPower);
        logFile.print(",");
        logFile.println(vehicle.averagePower);
        
        logFile.close();
    }
}
