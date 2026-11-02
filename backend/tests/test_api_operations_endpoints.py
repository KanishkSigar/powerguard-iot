"""PowerGuard IoT — Operations, Alerts & Integrations API Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_alerts_endpoints():
    res = client.get("/v1/alerts/")
    assert res.status_code == 200
    ack = client.post("/v1/alerts/ALT-101/acknowledge")
    assert ack.status_code == 200

def test_anomalies_endpoints():
    res = client.get("/v1/anomalies/")
    assert res.status_code == 200

def test_firmware_endpoints():
    res = client.get("/v1/firmware/releases")
    assert res.status_code == 200

def test_notifications_endpoints():
    res = client.get("/v1/notifications/")
    assert res.status_code == 200

def test_webhooks_endpoints():
    res = client.get("/v1/webhooks/")
    assert res.status_code == 200

def test_integrations_and_settings():
    i_res = client.get("/v1/integrations/")
    assert i_res.status_code == 200
    s_res = client.get("/v1/settings/")
    assert s_res.status_code == 200
    assert "grid_nominal_voltage_v" in s_res.json()