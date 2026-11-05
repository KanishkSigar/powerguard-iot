"""PowerGuard IoT — Active User Sessions Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_list_sessions():
    res = client.get("/v1/sessions/")
    assert res.status_code == 200
    assert res.json()["total"] >= 1

def test_terminate_session():
    res = client.delete("/v1/sessions/SES-102")
    assert res.status_code == 200
    assert res.json()["message"] == "Session terminated"