# Deployment & Setup

This document describes how to deploy the PowerGuard IoT application stack locally for development and testing using Docker Compose.

---

## 1. Stack Components

The complete development stack is defined in `docker-compose.yml` and consists of the following services:

1. **Mosquitto** (`mqtt`): MQTT broker serving as the ingestion gateway. Exposed on port `1883`.
2. **InfluxDB** (`influxdb`): Time-series database for telemetry storage. Exposed on port `8086`.
3. **FastAPI Backend** (`backend`): Python API server and MQTT subscriber. Exposed on port `8000`.
4. **Dashboard Frontend** (`frontend`): Static web resources.

---

## 2. Quick Start Steps

### Step 1: Clone the Repository & Configure Env
Copy the example environment template to `.env` in the backend directory:
```bash
cd backend
cp .env.example .env
```
Ensure the configurations for InfluxDB tokens, database bucket names, and alert credentials match your expectations.

### Step 2: Spin up Mosquitto and InfluxDB
Launch the supporting infrastructure services in detached mode:
```bash
docker-compose up -d mqtt influxdb
```

### Step 3: Run the Backend & Simulator Locally
To run and modify Python code during development:

1. Create a virtual environment and install requirements:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
3. Run the telemetry simulator in a separate terminal:
   ```bash
   python simulator.py
   ```

### Step 4: Access the Frontend Dashboard
Simply open the static page [frontend/index.html](file:///z:/Codes/github/powerguard-iot/frontend/index.html) in your browser. It will automatically connect to `http://localhost:8000/api/ws/realtime` for live charts.
