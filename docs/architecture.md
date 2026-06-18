# System Architecture — PowerGuard IoT

## High-Level Overview

PowerGuard IoT follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                          │
│                                                                     │
│   ┌─────────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│   │  Web Dashboard   │    │ Telegram Bot │    │  Email Alerts    │  │
│   │  (HTML/JS)       │    │              │    │  (SMTP)          │  │
│   └────────┬─────────┘    └──────┬───────┘    └────────┬─────────┘  │
│            │                     │                      │            │
├────────────┼─────────────────────┼──────────────────────┼────────────┤
│            │          APPLICATION LAYER                  │            │
│            │                     │                      │            │
│   ┌────────▼─────────────────────▼──────────────────────▼─────────┐ │
│   │                    FastAPI Backend Server                      │ │
│   │                                                               │ │
│   │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌─────────────┐ │ │
│   │  │ REST API │  │  MQTT    │  │  Anomaly  │  │   Alert     │ │ │
│   │  │ Endpoints│  │Subscriber│  │  Detector │  │  Dispatcher │ │ │
│   │  └──────────┘  └──────────┘  └───────────┘  └─────────────┘ │ │
│   └───────────────────────┬───────────────────────────────────────┘ │
│                           │                                         │
├───────────────────────────┼─────────────────────────────────────────┤
│                    DATA LAYER                                       │
│                           │                                         │
│   ┌───────────────────────▼───────────────────────────────────────┐ │
│   │                      InfluxDB                                 │ │
│   │              (Time-Series Database)                           │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                   COMMUNICATION LAYER                               │
│                                                                     │
│   ┌───────────────────────────────────────────────────────────────┐ │
│   │              Mosquitto MQTT Broker                            │ │
│   │         (Pub/Sub Message Broker over WiFi)                    │ │
│   └───────────────────────┬───────────────────────────────────────┘ │
│                           │                                         │
├───────────────────────────┼─────────────────────────────────────────┤
│                   HARDWARE LAYER                                    │
│                           │                                         │
│   ┌───────────────────────▼───────────────────────────────────────┐ │
│   │                  ESP32 Microcontroller                        │ │
│   │                                                               │ │
│   │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌────────────┐ │ │
│   │  │ CT Clamp │  │ Voltage  │  │   OLED    │  │   WiFi     │ │ │
│   │  │ SCT-013  │  │ ZMPT101B │  │  Display  │  │   Module   │ │ │
│   │  └──────────┘  └──────────┘  └───────────┘  └────────────┘ │ │
│   └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Sensor Reading Flow
```
CT Clamp → ADC → EmonLib (RMS calculation) → JSON payload → MQTT publish
Voltage Sensor → ADC → EmonLib → ─────────────────────────┘
```

### 2. Data Ingestion Flow
```
MQTT Broker → FastAPI MQTT Subscriber → Validate payload → Write to InfluxDB
```

### 3. Dashboard Query Flow
```
User opens dashboard → Frontend calls REST API → FastAPI queries InfluxDB → JSON response → Charts render
```

### 4. Anomaly Detection Flow
```
New reading arrives → Feature extraction → Isolation Forest scoring → If anomaly → Log to DB + Trigger alert
                                         → Rule-based checks ──────┘
```

### 5. Alert Flow
```
Anomaly detected → Alert Dispatcher → Check throttle (no spam) → Send via Telegram Bot API
                                                                → Send via SMTP Email
```

## MQTT Topic Design

| Topic | Publisher | Subscriber | Payload |
|-------|----------|------------|---------|
| `home/energy/{device_id}/{channel}` | ESP32 | Backend | Sensor readings JSON |
| `home/energy/{device_id}/status` | ESP32 | Backend | `online` / `offline` (LWT) |
| `home/energy/alerts` | Backend | Dashboard | Anomaly alert JSON |

## API Endpoint Design

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/realtime` | Latest readings from all channels |
| `GET` | `/api/history` | Historical data (query params: channel, start, end) |
| `GET` | `/api/usage/daily` | Daily kWh consumption summary |
| `GET` | `/api/usage/monthly` | Monthly consumption with cost estimate |
| `GET` | `/api/analytics/peak-hours` | Peak usage time analysis |
| `GET` | `/api/anomalies` | List of detected anomalies |
| `POST` | `/api/settings/thresholds` | Update alert thresholds |
| `GET` | `/api/devices` | List registered devices and channels |

## Database Schema (InfluxDB)

**Measurement:** `energy_readings`

| Type | Field | Data Type | Example |
|------|-------|-----------|---------|
| Tag | `device_id` | string | `meter_01` |
| Tag | `channel` | string | `kitchen` |
| Field | `voltage` | float | `228.5` |
| Field | `current` | float | `2.34` |
| Field | `power` | float | `534.99` |
| Field | `apparent_power` | float | `535.0` |
| Field | `power_factor` | float | `0.99` |
| Field | `energy_kwh` | float | `0.0015` |
| Timestamp | — | nanoseconds | auto |

**Measurement:** `anomalies`

| Type | Field | Data Type | Example |
|------|-------|-----------|---------|
| Tag | `device_id` | string | `meter_01` |
| Tag | `channel` | string | `kitchen` |
| Tag | `severity` | string | `high` |
| Field | `type` | string | `threshold_breach` |
| Field | `description` | string | `Power exceeded 2000W` |
| Field | `power_at_detection` | float | `2150.0` |
| Field | `anomaly_score` | float | `-0.82` |
| Timestamp | — | nanoseconds | auto |
