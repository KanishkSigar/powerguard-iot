"""PowerGuard IoT — API Keys Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_keys_list():
    res = client.get("/v1/keys/")
    assert res.status_code == 200
    assert res.json()["total"] >= 1

def test_keys_generate():
    res = client.post("/v1/keys/", json={"name": "HomeAssistant Connector"})
    assert res.status_code == 201
    assert "raw_token" in res.json()["key"]

def test_keys_revoke():
    res = client.delete("/v1/keys/KEY-01")
    assert res.status_code == 200
    assert res.json()["message"] == "API key revoked"