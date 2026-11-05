"""PowerGuard IoT — User Preferences Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_get_preferences():
    res = client.get("/v1/preferences/")
    assert res.status_code == 200
    assert "theme" in res.json()

def test_update_preferences():
    res = client.put("/v1/preferences/", json={"theme": "dark", "sound_alerts_enabled": True})
    assert res.status_code == 200
    assert res.json()["preferences"]["sound_alerts_enabled"] is True