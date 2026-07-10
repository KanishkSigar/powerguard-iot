# API Reference Guide

This document describes the REST and WebSocket API endpoints exposed by the FastAPI backend server of PowerGuard IoT.

All REST endpoints are prefixed with `/api` and return responses in standard JSON format (unless otherwise specified).

---

## 1. System Health & Info

### GET `/health`
Check the operational status of the server.
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-07-10T12:00:00Z"
  }
  ```

### GET `/api/system/info`
Retrieve detailed environment and system execution info.
- **Response**:
  ```json
  {
    "status": "online",
    "python_version": "3.10.12 (main, Jun 11 2026, 10:00:00)",
    "platform": "Linux-5.15.0-generic-x86_64-with-glibc2.35",
    "timestamp": "2026-07-10T12:00:00.000000"
  }
  ```

---

## 2. Telemetry Real-time Feeds

### GET `/api/realtime`
Get the latest cached in-memory readings for all telemetry channels.
- **Parameters**:
  - `device_id` (Query, Optional): Filter readings by a specific hardware identifier.
- **Response**:
  ```json
  {
    "status": "ok",
    "channels": {
      "pg_device_01/main": {
        "device_id": "pg_device_01",
        "channel": "main",
        "voltage_rms": 230.1,
        "current_rms": 4.5,
        "power_watts": 1035.45,
        "apparent_power_va": 1035.45,
        "power_factor": 1.0,
        "energy_kwh": 12.45
      }
    },
    "last_updated": "2026-07-10T12:00:00.000000"
  }
  ```

### WebSocket `/api/ws/realtime`
Open a persistent, bidirectional WebSocket channel to receive real-time updates as soon as MQTT messages are received.
- **Message format sent to clients**:
  ```json
  {
    "device_id": "pg_device_01",
    "channel": "main",
    "voltage_rms": 230.1,
    "current_rms": 4.5,
    "power_watts": 1035.45,
    "apparent_power_va": 1035.45,
    "power_factor": 1.0,
    "energy_kwh": 12.45,
    "timestamp": "2026-07-10T12:00:00Z"
  }
  ```

---

## 3. History & Exports

### GET `/api/history`
Fetch historical telemetry raw readings.
- **Parameters**:
  - `channel` (Query, Default: `main`): The channel name.
  - `range` (Query, Default: `-24h`): The relative lookback interval. Supported values: `-1h`, `-6h`, `-12h`, `-24h`, `-7d`, `-30d`.
  - `device_id` (Query, Optional): Filter by device identifier.
- **Response**:
  ```json
  {
    "channel": "main",
    "range": "-24h",
    "count": 2,
    "readings": [
      {
        "timestamp": "2026-07-10T11:00:00Z",
        "voltage": 229.8,
        "current": 4.2,
        "power": 965.16,
        "energy_kwh": 12.01,
        "power_factor": 1.0
      }
    ]
  }
  ```

### GET `/api/history/export`
Stream historical energy readings directly as a CSV file attachment.
- **Parameters**: Same as `GET /api/history`
- **Response**: Streamed CSV file (`powerguard_export_<channel>_<range>.csv`).

---

## 4. Usage Analytics & Reporting

### GET `/api/usage/daily`
Provides daily aggregated consumption statistics and cost calculation.
- **Parameters**:
  - `channel` (Query, Default: `main`): The channel name.
  - `days` (Query, Default: `30`): Lookback duration (1 to 365 days).
  - `device_id` (Query, Optional): Filter by device identifier.
- **Response**:
  ```json
  {
    "channel": "main",
    "days": 30,
    "tariff_rate_inr": 6.50,
    "total_kwh": 150.35,
    "total_cost_inr": 977.28,
    "daily_breakdown": [
      {
        "day": "2026-07-09",
        "total_kwh": 5.01,
        "cost_inr": 32.57
      }
    ]
  }
  ```

### GET `/api/usage/monthly`
Aggregate consumption over the past 30 days and locate peak days.
- **Parameters**: Same as daily usage
- **Response**: Summarized metrics (average kWh, total cost, peak usage day metadata).

### GET `/api/reports/monthly`
Generate and download a formal, printable PDF report containing energy metrics, trends, and charts for the current month.
- **Response**: Streamed PDF binary file (`PowerGuard_Report_<channel>_<YYYY-MM>.pdf`).

---

## 5. Machine Learning & Anomaly Analytics

### GET `/api/analytics/peak-hours`
Run analytical group-by queries on InfluxDB over the past 7 days to calculate average consumption per hour of the day.
- **Response**:
  ```json
  {
    "channel": "main",
    "hourly_breakdown": [
      { "hour": 0, "avg_power_watts": 350.2 }
    ],
    "peak_hours": [
      { "hour": 19, "avg_power_watts": 1820.4 }
    ],
    "off_peak_hours": [
      { "hour": 3, "avg_power_watts": 120.1 }
    ]
  }
  ```

### GET `/api/analytics/forecast`
Generate energy usage predictions for the upcoming 7 days using statistical modeling on historical aggregated data.
- **Response**:
  ```json
  {
    "channel": "main",
    "days_predicted": 7,
    "forecast": [
      { "day": "2026-07-11", "predicted_kwh": 5.25 }
    ]
  }
  ```

### GET `/api/anomalies`
Query the list of detected anomaly events saved in the system.
- **Parameters**:
  - `hours` (Query, Default: `24`): Hourly search span.
- **Response**:
  ```json
  {
    "count": 1,
    "hours": 24,
    "anomalies": [
      {
        "timestamp": "2026-07-10T10:15:30Z",
        "device_id": "pg_device_01",
        "channel": "main",
        "severity": "high",
        "type": "Critical Power Threshold Exceeded",
        "description": "Active power of 2450W exceeded safety limit of 2000W",
        "power_at_detection": 2450.0,
        "anomaly_score": -0.15
      }
    ]
  }
  ```

---

## 6. Device Registry & Threshold Rules

### GET `/api/devices`
Identify all active device client IDs and their online statuses based on recent message ping times.
- **Response**:
  ```json
  {
    "count": 1,
    "devices": [
      {
        "device_id": "pg_device_01",
        "channels": ["main"],
        "status": "online"
      }
    ]
  }
  ```

### GET `/api/settings/thresholds`
Retrieve current values configured for runtime anomaly checking parameters.
- **Response**:
  ```json
  {
    "power_threshold_watts": 2000.0,
    "left_on_seconds": 7200,
    "tariff_rate_inr": 6.50
  }
  ```

### POST `/api/settings/thresholds`
Update runtime alert threshold values dynamically.
- **Parameters**:
  - `power_threshold_watts` (Body/Query, Optional)
  - `left_on_seconds` (Body/Query, Optional)
  - `tariff_rate_inr` (Body/Query, Optional)
- **Response**: Standard status update message with updated keys.
