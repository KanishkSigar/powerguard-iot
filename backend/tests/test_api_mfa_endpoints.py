"""PowerGuard IoT — MFA API Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_mfa_setup():
    res = client.post("/v1/mfa/setup")
    assert res.status_code == 200
    assert "secret" in res.json()
    assert "provisioning_uri" in res.json()

def test_mfa_verify_valid():
    res = client.post("/v1/mfa/verify", json={"code": "123456"})
    assert res.status_code == 200
    assert res.json()["status"] == "verified"

def test_mfa_verify_invalid():
    res = client.post("/v1/mfa/verify", json={"code": "invalid"})
    assert res.status_code == 400

def test_mfa_disable():
    res = client.post("/v1/mfa/disable", json={"code": "123456"})
    assert res.status_code == 200
    assert res.json()["status"] == "disabled"