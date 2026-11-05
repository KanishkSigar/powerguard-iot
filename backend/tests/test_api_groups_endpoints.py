"""PowerGuard IoT — Device Groups Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_groups_list():
    res = client.get("/v1/groups/")
    assert res.status_code == 200
    assert res.json()["total"] >= 1

def test_groups_create():
    res = client.post("/v1/groups/", json={"name": "Substation 3", "zone": "West Wing"})
    assert res.status_code == 201
    assert res.json()["group"]["name"] == "Substation 3"

def test_groups_devices():
    res = client.get("/v1/groups/GRP-01/devices")
    assert res.status_code == 200
    assert "devices" in res.json()