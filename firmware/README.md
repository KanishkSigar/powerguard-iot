# Firmware

ESP32 Arduino firmware for the PowerGuard IoT energy meter.

## Hardware Required

- ESP32 DevKit v1
- SCT-013-030 CT Clamp (current sensor)
- ZMPT101B (voltage sensor)
- 0.96" OLED Display (SSD1306)
- Burden resistor circuit (33Ω resistor, 2× 10kΩ resistors, 10µF capacitor)

## Libraries

- `EmonLib` — Energy monitoring calculations
- `PubSubClient` — MQTT client
- `Adafruit_SSD1306` — OLED display driver
- `ArduinoJson` — JSON serialization
