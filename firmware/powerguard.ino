// ============================================================
// PowerGuard IoT — ESP32 Energy Monitor Firmware
// ============================================================
// Reads current and voltage sensors, calculates power metrics,
// and publishes data to MQTT broker.
// ============================================================

#include <WiFi.h>
#include "EmonLib.h"
#include "config.h"

// ----------------------
// Energy Monitor Instances
// ----------------------

EnergyMonitor emonMain;    // Main line monitor
EnergyMonitor emonCh1;     // Channel 1 monitor
EnergyMonitor emonCh2;     // Channel 2 monitor

// ----------------------
// Sensor Reading Storage
// ----------------------

struct EnergyReading {
  float voltage;
  float current;
  float realPower;
  float apparentPower;
  float powerFactor;
  float energyKwh;
};

EnergyReading readingMain;
EnergyReading readingCh1;
EnergyReading readingCh2;

// Cumulative energy tracking (in watt-seconds)
float cumulativeEnergyMain = 0;
float cumulativeEnergyCh1  = 0;
float cumulativeEnergyCh2  = 0;

unsigned long lastReadingTime = 0;

// ----------------------
// WiFi Connection
// ----------------------

void setupWiFi() {
  Serial.print("[WiFi] Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    attempts++;
    if (attempts > 40) {  // 20 second timeout
      Serial.println("\n[WiFi] Connection failed! Restarting...");
      ESP.restart();
    }
  }

  Serial.println();
  Serial.print("[WiFi] Connected! IP: ");
  Serial.println(WiFi.localIP());
}

// ----------------------
// Sensor Setup
// ----------------------

void setupSensors() {
  Serial.println("[Sensors] Initializing energy monitors...");

  // Configure current sensors (CT clamps)
  // current(pin, calibration)
  emonMain.current(PIN_CT_MAIN, CT_CALIBRATION_MAIN);
  emonCh1.current(PIN_CT_CH1, CT_CALIBRATION_CH1);
  emonCh2.current(PIN_CT_CH2, CT_CALIBRATION_CH2);

  // Configure voltage sensor
  // voltage(pin, calibration, phase_shift)
  emonMain.voltage(PIN_VOLTAGE, VOLTAGE_CALIBRATION, 1.7);
  emonCh1.voltage(PIN_VOLTAGE, VOLTAGE_CALIBRATION, 1.7);
  emonCh2.voltage(PIN_VOLTAGE, VOLTAGE_CALIBRATION, 1.7);

  // Set ADC resolution for ESP32 (12-bit = 4096)
  analogReadResolution(12);

  Serial.println("[Sensors] Energy monitors initialized.");
}

// ----------------------
// Simulated Readings
// ----------------------

#if SIMULATION_MODE
float simulateValue(float base, float variance) {
  return base + ((float)random(-100, 100) / 100.0) * variance;
}

void readSimulatedSensors() {
  // Simulate realistic Indian household readings
  readingMain.voltage      = simulateValue(230.0, 5.0);
  readingMain.current      = simulateValue(3.5, 1.0);
  readingMain.realPower    = readingMain.voltage * readingMain.current * simulateValue(0.95, 0.03);
  readingMain.apparentPower = readingMain.voltage * readingMain.current;
  readingMain.powerFactor  = readingMain.realPower / readingMain.apparentPower;

  readingCh1.voltage       = readingMain.voltage;
  readingCh1.current       = simulateValue(1.2, 0.5);
  readingCh1.realPower     = readingCh1.voltage * readingCh1.current * simulateValue(0.92, 0.05);
  readingCh1.apparentPower = readingCh1.voltage * readingCh1.current;
  readingCh1.powerFactor   = readingCh1.realPower / readingCh1.apparentPower;

  readingCh2.voltage       = readingMain.voltage;
  readingCh2.current       = simulateValue(0.8, 0.3);
  readingCh2.realPower     = readingCh2.voltage * readingCh2.current * simulateValue(0.90, 0.04);
  readingCh2.apparentPower = readingCh2.voltage * readingCh2.current;
  readingCh2.powerFactor   = readingCh2.realPower / readingCh2.apparentPower;
}
#endif

// ----------------------
// Read Sensors (Real Hardware)
// ----------------------

void readSensors() {
  #if SIMULATION_MODE
    readSimulatedSensors();
  #else
    // Calculate real power, apparent power, Vrms, Irms, power factor
    emonMain.calcVI(SAMPLES_PER_READING, 2000);
    readingMain.voltage       = emonMain.Vrms;
    readingMain.current       = emonMain.Irms;
    readingMain.realPower     = emonMain.realPower;
    readingMain.apparentPower = emonMain.apparentPower;
    readingMain.powerFactor   = emonMain.powerFactor;

    emonCh1.calcVI(SAMPLES_PER_READING, 2000);
    readingCh1.voltage        = emonCh1.Vrms;
    readingCh1.current        = emonCh1.Irms;
    readingCh1.realPower      = emonCh1.realPower;
    readingCh1.apparentPower  = emonCh1.apparentPower;
    readingCh1.powerFactor    = emonCh1.powerFactor;

    emonCh2.calcVI(SAMPLES_PER_READING, 2000);
    readingCh2.voltage        = emonCh2.Vrms;
    readingCh2.current        = emonCh2.Irms;
    readingCh2.realPower      = emonCh2.realPower;
    readingCh2.apparentPower  = emonCh2.apparentPower;
    readingCh2.powerFactor    = emonCh2.powerFactor;
  #endif

  // Calculate cumulative energy (kWh)
  unsigned long now = millis();
  if (lastReadingTime > 0) {
    float elapsedHours = (now - lastReadingTime) / 3600000.0;
    cumulativeEnergyMain += readingMain.realPower * elapsedHours;
    cumulativeEnergyCh1  += readingCh1.realPower * elapsedHours;
    cumulativeEnergyCh2  += readingCh2.realPower * elapsedHours;
  }
  lastReadingTime = now;

  readingMain.energyKwh = cumulativeEnergyMain / 1000.0;
  readingCh1.energyKwh  = cumulativeEnergyCh1 / 1000.0;
  readingCh2.energyKwh  = cumulativeEnergyCh2 / 1000.0;
}

// ----------------------
// Print Readings to Serial
// ----------------------

void printReadings() {
  Serial.println("--- Energy Readings ---");
  Serial.printf("[Main]  V: %.1fV  I: %.2fA  P: %.1fW  S: %.1fVA  PF: %.2f  E: %.4fkWh\n",
    readingMain.voltage, readingMain.current, readingMain.realPower,
    readingMain.apparentPower, readingMain.powerFactor, readingMain.energyKwh);
  Serial.printf("[Ch1]   V: %.1fV  I: %.2fA  P: %.1fW  S: %.1fVA  PF: %.2f  E: %.4fkWh\n",
    readingCh1.voltage, readingCh1.current, readingCh1.realPower,
    readingCh1.apparentPower, readingCh1.powerFactor, readingCh1.energyKwh);
  Serial.printf("[Ch2]   V: %.1fV  I: %.2fA  P: %.1fW  S: %.1fVA  PF: %.2f  E: %.4fkWh\n",
    readingCh2.voltage, readingCh2.current, readingCh2.realPower,
    readingCh2.apparentPower, readingCh2.powerFactor, readingCh2.energyKwh);
  Serial.println();
}

// ----------------------
// Setup
// ----------------------

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("========================================");
  Serial.println("  PowerGuard IoT — Energy Monitor");
  Serial.println("  Device: " DEVICE_ID);
  #if SIMULATION_MODE
  Serial.println("  Mode: SIMULATION");
  #else
  Serial.println("  Mode: HARDWARE");
  #endif
  Serial.println("========================================");
  Serial.println();

  // Initialize sensors
  setupSensors();

  // Connect to WiFi
  setupWiFi();
}

// ----------------------
// Main Loop
// ----------------------

void loop() {
  // Reconnect WiFi if disconnected
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WiFi] Disconnected. Reconnecting...");
    setupWiFi();
  }

  // Read sensors
  readSensors();

  // Print to serial
  printReadings();

  delay(READING_INTERVAL_MS);
}
