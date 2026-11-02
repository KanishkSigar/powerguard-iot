"""PowerGuard IoT — Security, Auth & RBAC API Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_auth_login_success():
    res = client.post("/v1/auth/login", json={"username": "admin", "password": "powerguard"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_auth_login_invalid():
    res = client.post("/v1/auth/login", json={"username": "admin", "password": "wrongpassword"})
    assert res.status_code == 401

def test_users_endpoints():
    res = client.get("/v1/users/")
    assert res.status_code == 200
    assert res.json()["total"] >= 1

def test_roles_and_permissions():
    r_res = client.get("/v1/roles/")
    assert r_res.status_code == 200
    p_res = client.get("/v1/permissions/")
    assert p_res.status_code == 200

def test_audit_endpoints():
    res = client.get("/v1/audit/")
    assert res.status_code == 200
    assert "items" in res.json()