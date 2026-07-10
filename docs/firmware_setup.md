# Firmware Setup & Compilation Guide

This document describes how to configure, compile, and upload the Arduino-based C++ firmware to the ESP32 microcontroller.

---

## 1. Development Environment

You can compile and upload the firmware using either **PlatformIO** (recommended) or the **Arduino IDE**.

### Required Libraries
Ensure you install the following dependencies via your library manager:
1. **EmonLib**: Energy monitoring library by Trystan Lea.
2. **PubSubClient**: MQTT client by Nick O'Leary.
3. **ArduinoJson**: JSON parser by Benoit Blanchon (version 6.x or 7.x).
4. **Adafruit SSD1306** & **Adafruit GFX**: Graphics drivers for the I2C OLED display.

---

## 2. Configuration Setup (`config.h`)

Before compiling, you must copy the configuration template to a local configuration file:

```bash
cd firmware
cp config.example.h config.h
```

Open `config.h` and update the parameters for your environment:

### WiFi & MQTT Broker settings
```cpp
#define WIFI_SSID       "YOUR_WIFI_SSID"
#define WIFI_PASSWORD   "YOUR_WIFI_PASSWORD"

#define MQTT_BROKER     "192.168.1.100"   // IP Address of Mosquitto host
#define MQTT_PORT       1883
```

### Calibration Settings
You must calibrate the values against a physical digital multimeter (DMM) to get accurate readings:
```cpp
// Calibration constants for current monitoring (CT clamps)
#define CT_CALIBRATION_MAIN     30.0

// Calibration constant for ZMPT101B voltage module (typically ~234.0)
#define VOLTAGE_CALIBRATION     234.0
```

### Test/Simulation Mode
If you do not have physical ESP32 hardware or sensors on hand, you can enable simulation mode in the firmware. This will generate fake sine readings for development testing:
```cpp
#define SIMULATION_MODE true
```

---

## 3. Compiling & Flashing

### Option A: Arduino IDE
1. Open the Arduino IDE.
2. Open `firmware/powerguard.ino`.
3. In **Tools > Board**, select **ESP32 Dev Module**.
4. Install all library dependencies via **Tools > Manage Libraries**.
5. Connect your ESP32 to your PC using a micro-USB cable.
6. Select the correct COM port in **Tools > Port**.
7. Click the **Upload** button.

### Option B: PlatformIO (VS Code)
If using PlatformIO, you can create a standard `platformio.ini` in the `firmware/` directory:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
lib_deps =
    openenergymonitor/EmonLib @ ^3.0
    knolleary/PubSubClient @ ^2.8
    bblanchon/ArduinoJson @ ^6.21
    adafruit/Adafruit SSD1306 @ ^2.5
    adafruit/Adafruit GFX Library @ ^1.11
```

Run the compile and upload command:
```bash
# Upload and start the serial monitor
pio run --target upload --target monitor
```
