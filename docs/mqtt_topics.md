# MQTT Topic Structure & Payloads

This document defines the MQTT messaging protocol, topic hierarchy, and JSON payload formats used for real-time telemetry distribution and state tracking in PowerGuard IoT.

---

## 1. Topic Hierarchy Overview

By default, all MQTT topics use the prefix configured under the backend settings (default: `home/energy`). The system uses a hierarchical structure to separate concerns:

| Topic | Description | Payload Type |
|---|---|---|
| `home/energy/<device_id>/status` | Lifecycle and connection tracking (LWT) | Plain Text (`online` / `offline`) |
| `home/energy/<device_id>/<channel>` | Real-time electrical measurements | JSON |

- `<device_id>`: Unique hardware alphanumeric identifier (e.g., `pg_device_01`).
- `<channel>`: Measurement branch or circuit zone (e.g., `main`, `channel1`, `aircon`).

---

## 2. Telemetry Message Format

Published by edge devices to the topic:
`home/energy/<device_id>/<channel>` (e.g., `home/energy/pg_device_01/main`)

### Telemetry Payload Schema (JSON)
```json
{
  "voltage_rms": 230.12,
  "current_rms": 4.52,
  "power_watts": 1035.45,
  "apparent_power_va": 1040.15,
  "power_factor": 0.99,
  "energy_kwh": 12.458
}
```

### Telemetry Field Breakdown

- `voltage_rms` (Float): Root-Mean-Square voltage measured across the AC line (Volts, e.g. `230.12`).
- `current_rms` (Float): Root-Mean-Square current flow measured by the current clamp (Amperes, e.g. `4.52`).
- `power_watts` (Float): Active (real) power draw calculated from voltage and current phase values (Watts, e.g. `1035.45`).
- `apparent_power_va` (Float): Apparent power ($V_{RMS} \times I_{RMS}$) indicating overall electrical demand (Volt-Amperes, e.g. `1040.15`).
- `power_factor` (Float): Efficiency ratio calculated as $\text{Active Power} / \text{Apparent Power}$ (range `0.0` to `1.0`).
- `energy_kwh` (Float): Cumulative lifetime energy consumed calculated locally on the microcontroller (Kilowatt-hours, e.g. `12.458`).

---

## 3. Device Lifecycle (Last Will & Testament)

To track hardware availability, edge devices establish a connection status message using MQTT's **Last Will and Testament (LWT)** feature.

Published to the topic:
`home/energy/<device_id>/status` (e.g., `home/energy/pg_device_01/status`)

- **Online Announcement**: Immediately upon connecting to the broker, the device publishes a retained payload of `online`.
- **Offline Failure Statement**: If the device drops off the network unexpectedly without sending a clean disconnect packet, the MQTT broker automatically publishes the registered Will payload of `offline` to the same topic.
