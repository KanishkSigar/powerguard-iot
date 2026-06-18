# Backend

Python FastAPI backend server for PowerGuard IoT.

## Responsibilities

- Subscribe to MQTT topics and ingest sensor data
- Store readings in InfluxDB
- Serve REST API endpoints for the dashboard
- Run anomaly detection scoring
- Dispatch alerts (Telegram, Email)
