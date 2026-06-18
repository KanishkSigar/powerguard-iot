# ⚡ PowerGuard IoT

> Smart Energy Meter with Anomaly Detection — An IoT-based energy monitoring system

## 🎯 Overview

PowerGuard IoT is a low-cost, intelligent energy monitoring system that tracks real-time power consumption, logs historical usage data, detects anomalies using machine learning, and alerts users through Telegram and email.

## ✨ Features

- **Real-time Monitoring** — Live voltage, current, power readings via web dashboard
- **Historical Analytics** — Daily/monthly consumption tracking with cost estimation
- **Anomaly Detection** — ML-powered detection of unusual power patterns
- **Smart Alerts** — Telegram and email notifications for anomalies
- **Multi-Channel** — Monitor multiple appliances/circuits independently
- **Beautiful Dashboard** — Modern, responsive web UI with dark mode

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

> Coming soon — project under active development.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
