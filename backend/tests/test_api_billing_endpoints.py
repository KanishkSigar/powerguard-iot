"""PowerGuard IoT — Billing & Tariff API Endpoints Tests"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.v1 import v1_router

app = FastAPI()
app.include_router(v1_router)
client = TestClient(app)

def test_tariffs_endpoints():
    res = client.get("/v1/tariffs/")
    assert res.status_code == 200
    assert res.json()["total"] >= 1

def test_billing_estimate_endpoints():
    res = client.get("/v1/billing/estimate?projected_days=30")
    assert res.status_code == 200
    assert res.json()["currency"] == "INR"

def test_reports_endpoints():
    res = client.get("/v1/reports/daily?date=2026-11-02")
    assert res.status_code == 200
    assert res.json()["total_consumption_kwh"] > 0

def test_export_jobs_endpoints():
    res = client.post("/v1/export/jobs", json={"format": "csv"})
    assert res.status_code == 202
    assert "job_id" in res.json()

def test_schedules_endpoints():
    res = client.get("/v1/schedules/")
    assert res.status_code == 200
    assert res.json()["total"] >= 1