"""PowerGuard IoT — OAuth2 Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_oauth_token_issue():
    res = client.post("/v1/oauth/token", json={"grant_type": "client_credentials"})
    assert res.status_code == 200
    assert "access_token" in res.json()
    assert res.json()["token_type"] == "bearer"

def test_oauth_token_unsupported_grant():
    res = client.post("/v1/oauth/token", json={"grant_type": "unsupported_grant"})
    assert res.status_code == 400

def test_oauth_authorize():
    res = client.get("/v1/oauth/authorize?client_id=web_app")
    assert res.status_code == 200
    assert res.json()["status"] == "consent_required"

def test_oauth_revoke():
    res = client.post("/v1/oauth/revoke", json={"token": "pg_token_xyz"})
    assert res.status_code == 200
    assert res.json()["status"] == "revoked"