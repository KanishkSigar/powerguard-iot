// ============================================================
// PowerGuard IoT — Configuration
// ============================================================
// Copy this file to config.h and fill in your values.
// config.h is gitignored to protect your credentials.
// ============================================================

#ifndef CONFIG_H
#define CONFIG_H

// ----------------------
// WiFi Configuration
// ----------------------
#define WIFI_SSID       "YOUR_WIFI_SSID"
#define WIFI_PASSWORD   "YOUR_WIFI_PASSWORD"

// ----------------------
// MQTT Configuration
// ----------------------
#define MQTT_BROKER     "192.168.1.100"   // IP of your MQTT broker
#define MQTT_PORT       1883
#define MQTT_USER       ""                 // Leave empty if no auth
#define MQTT_PASSWORD   ""                 // Leave empty if no auth

// ----------------------
// Device Configuration
// ----------------------
#define DEVICE_ID       "meter_01"

// ----------------------
// MQTT Topics
// ----------------------
#define TOPIC_MAIN      "home/energy/" DEVICE_ID "/main"
#define TOPIC_CHANNEL1  "home/energy/" DEVICE_ID "/channel1"
#define TOPIC_CHANNEL2  "home/energy/" DEVICE_ID "/channel2"
#define TOPIC_STATUS    "home/energy/" DEVICE_ID "/status"

// ----------------------
// Sensor Calibration
// ----------------------
// CT Clamp calibration constant
// For SCT-013-030 with 33Ω burden resistor: ~30.0
// Adjust based on multimeter comparison
#define CT_CALIBRATION_MAIN     30.0
#define CT_CALIBRATION_CH1      30.0
#define CT_CALIBRATION_CH2      30.0

// Voltage sensor calibration constant
// For ZMPT101B: typically ~234.0 (adjust with multimeter)
#define VOLTAGE_CALIBRATION     234.0

// ----------------------
// Reading Intervals
// ----------------------
#define READING_INTERVAL_MS     2000   // Send readings every 2 seconds
#define SAMPLES_PER_READING     1480   // Number of ADC samples per reading

// ----------------------
// Pin Assignments
// ----------------------
#define PIN_CT_MAIN     34    // ADC1_CH6 — Main line CT clamp
#define PIN_CT_CH1      35    // ADC1_CH7 — Channel 1 CT clamp
#define PIN_CT_CH2      32    // ADC1_CH4 — Channel 2 CT clamp
#define PIN_VOLTAGE     33    // ADC1_CH5 — ZMPT101B voltage sensor

#define PIN_OLED_SDA    21    // I2C SDA for OLED
#define PIN_OLED_SCL    22    // I2C SCL for OLED

// ----------------------
// OLED Display
// ----------------------
#define SCREEN_WIDTH    128
#define SCREEN_HEIGHT   64
#define OLED_ADDR       0x3C

// ----------------------
// Simulation Mode
// ----------------------
// Set to true to generate fake sensor data (for testing without hardware)
#define SIMULATION_MODE false

#endif // CONFIG_H
