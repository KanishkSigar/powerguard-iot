# ⚡ PowerGuard IoT

> Smart Energy Meter with Anomaly Detection — An IoT-based energy monitoring system

## 🎯 Overview

PowerGuard IoT is a low-cost, intelligent energy monitoring system that tracks real-time power consumption, logs historical usage data, detects anomalies using machine learning, and alerts users through Telegram and email.

## ✨ Features

- **Real-time Monitoring** — Live voltage, current, power readings via web dashboard
- **Historical Analytics** — Daily/monthly consumption tracking with cost estimation
- **Advanced Forecasting** — Predictive ML forecasting of future energy usage
- **Automated Reporting** — Downloadable monthly PDF reports and CSV data exports
- **Real-time Streaming** — WebSocket-based instantaneous live data updates
- **Anomaly Detection** — ML-powered detection of unusual power patterns

## 🏗️ Architecture

```
ESP32 + Sensors → MQTT → FastAPI Backend → InfluxDB
                                         → React Dashboard
                                         → Anomaly Detection (ML)
                                         → Telegram / Email Alerts
```

## 🧩 Tech Stack

| Layer | Technology |
|-------|-----------|
| Firmware | ESP32 (Arduino C++) |
| Communication | MQTT (Mosquitto) |
| Backend | Python (FastAPI) |
| Database | InfluxDB |
| Frontend | HTML/CSS/JS with Chart.js |
| ML | scikit-learn (Isolation Forest) |
| Alerts | Telegram Bot API, SMTP |
| Deployment | Docker Compose |

## 📁 Project Structure

```
powerguard-iot/
├── firmware/          # ESP32 Arduino firmware
├── backend/           # FastAPI backend server
├── frontend/          # Web dashboard
├── ml/                # Anomaly detection models & scripts
├── mqtt/              # Mosquitto broker configuration
├── docs/              # Documentation & diagrams
├── docker-compose.yml # Full stack deployment
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites
- Docker and Docker Compose
- Python 3.10+
- PlatformIO or Arduino IDE (for firmware)

### 2. Infrastructure Setup (MQTT + InfluxDB)
```bash
# Start Mosquitto and InfluxDB
docker-compose up -d
```

### 3. Backend & Simulator Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

# Run the backend API and MQTT subscriber
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In a new terminal, run the data simulator (if you don't have ESP32 hardware)
venv\Scripts\activate
python simulator.py
```

### 4. Frontend Dashboard
Simply open `frontend/index.html` in your web browser. It will connect to the local API automatically.

### 5. ML Model Training
After running the simulator for a few minutes (or importing historical data):
```bash
cd ml
python train_model.py
```

## 📡 MQTT Topic Structure

The system uses a hierarchical topic structure for communication:

- `home/energy/<device_id>/<channel>` — Energy readings (JSON payload)
  - Channels: `main`, `channel1`, `channel2`
- `home/energy/<device_id>/status` — Device status (`online`/`offline`)

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
