"""PowerGuard IoT — Cluster Status & Token Introspection Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_system_status():
    res = client.get("/v1/status/")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_status_ping():
    res = client.get("/v1/status/ping")
    assert res.status_code == 200
    assert res.json()["ping"] == "pong"

def test_token_introspection():
    res = client.post("/v1/tokens/introspect", json={"token": "valid_mock_jwt"})
    assert res.status_code == 200
    assert res.json()["active"] is True

def test_token_refresh():
    res = client.post("/v1/tokens/refresh", json={"refresh_token": "valid_refresh_token"})
    assert res.status_code == 200
    assert "access_token" in res.json()