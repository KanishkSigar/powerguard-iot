"""PowerGuard IoT — Telemetry API Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_devices_endpoints():
    res = client.get("/v1/devices/")
    assert res.status_code == 200
    assert "items" in res.json()
    assert res.json()["total"] >= 1

    single = client.get("/v1/devices/DEV-ESP32-001")
    assert single.status_code == 200
    assert single.json()["device_id"] == "DEV-ESP32-001"

def test_readings_endpoints():
    res = client.get("/v1/readings/latest")
    assert res.status_code == 200
    assert "channels" in res.json()
    assert res.json()["total_power_w"] > 0

def test_dashboard_endpoints():
    res = client.get("/v1/dashboard/summary")
    assert res.status_code == 200
    assert res.json()["active_devices_count"] > 0

def test_health_endpoints():
    res = client.get("/v1/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_metrics_endpoints():
    res = client.get("/v1/metrics/power-quality")
    assert res.status_code == 200
    assert "thd_voltage_percent" in res.json()