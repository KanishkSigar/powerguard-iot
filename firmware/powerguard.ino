// ============================================================
// PowerGuard IoT — ESP32 Energy Monitor Firmware
// ============================================================
// Reads current and voltage sensors, calculates power metrics,
// and publishes data to MQTT broker.
// ============================================================

#include <WiFi.h>
#include "config.h"

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
// Setup
// ----------------------

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println();
  Serial.println("========================================");
  Serial.println("  PowerGuard IoT — Energy Monitor");
  Serial.println("  Device: " DEVICE_ID);
  Serial.println("========================================");
  Serial.println();

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

  delay(READING_INTERVAL_MS);
}
