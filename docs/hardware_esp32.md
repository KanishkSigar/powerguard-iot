# Hardware Integration & ESP32 Configuration

This document specifies the hardware component list, wiring connection guide, and ESP32 pin assignments for the physical PowerGuard IoT energy meter.

---

## 1. Bill of Materials (BOM)

To construct a physical monitoring unit, you will need:

| Component | Quantity | Description | Recommended Spec |
|---|---|---|---|
| **ESP32 Development Board** | 1 | Microcontroller with WiFi/Bluetooth | ESP32 DevKitC v4 (30-pin or 38-pin layout) |
| **SCT-013-000 CT Clamp** | Up to 3 | Non-invasive current sensor | 30A/1V or 100A/50mA (requires burden resistor) |
| **ZMPT101B Module** | 1 | Active single-phase AC voltage sensor | 0-250V AC input, Analog output |
| **SSD1306 OLED Display** | 1 | Status monitor display screen | 0.96-inch 128x64 pixels, I2C interface |
| **Burden Resistor** | 1 per clamp | Required if using current-output CT clamps | 33 $\Omega$ for SCT-013-000 with 5V ADC input |
| **Resistors & Capacitors** | 1 set | For ADC level shifting circuit bias | $2 \times 10\,\text{k}\Omega$ resistors, $1 \times 10\,\mu\text{F}$ capacitor per clamp |

---

## 2. Pin Assignments (ESP32 DevKitC)

The firmware assumes the following pins are wired to the components. Analog signals must use ADC1 pins because ADC2 cannot be used when WiFi is active.

```
                  +-----------------------+
                  |         ESP32         |
                  |                       |
   [CT Main Input] 34 [ADC1_6]  [I2C SDA] 21 [SDA] ---> [OLED SDA]
    [CT Ch1 Input] 35 [ADC1_7]  [I2C SCL] 22 [SCL] ---> [OLED SCL]
    [CT Ch2 Input] 32 [ADC1_4]            |
   [Voltage Input] 33 [ADC1_5]            |
                  +-----------------------+
```

---

## 3. Circuit Schematics & Analog Front End (AFE)

Because the ESP32 ADC reads only positive voltages between `0V` and `3.3V`, AC signals from the sensors must be shifted so their mid-point sits at `1.65V`.

### CT Clamp Level-Shifting Circuit

```
                     +3.3V (ESP32)
                       │
                     [10kΩ Resistor]
                       │
  [CT Clamp Pin 1] ────┼─────── [10µF Cap] ─── GND
                       │
                     [10kΩ Resistor]
                       │
  [CT Clamp Pin 2] ────┼───────> To ESP32 ADC Pin (34, 35, or 32)
                       │
                      GND
```

### ZMPT101B Wiring Guide

The ZMPT101B module includes an onboard operational amplifier that shifts the output voltage automatically.
- **VCC**: Connect to ESP32 `3.3V` or `5V` (depending on module variant).
- **GND**: Connect to ESP32 `GND`.
- **OUT**: Connect to ESP32 `GPIO33` (ADC1 Channel 5).
- **AC Input**: Connect to the mains AC phase (L) and neutral (N) securely.

> [!CAUTION]
> **HIGH VOLTAGE WARNING**: The AC side of the ZMPT101B module connects directly to live mains voltage (110V/230V AC). Always disconnect mains power before handling the circuit, and ensure adequate insulation.
