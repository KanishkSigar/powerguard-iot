"""
PowerGuard IoT — Telemetry Readings API Router
Exposes endpoints for querying high-resolution real-time and historical electrical telemetry.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query, status

router = APIRouter(prefix="/readings", tags=["Readings"])

@router.get("/latest", status_code=status.HTTP_200_OK)
def get_latest_readings(device_id: Optional[str] = Query(None)) -> Dict[str, Any]:
    return {
        "device_id": device_id or "DEV-ESP32-001",
        "channels": {
            "phase_a": {"voltage_rms": 230.4, "current_rms": 12.1, "power_w": 2787.8, "power_factor": 0.98},
            "phase_b": {"voltage_rms": 229.8, "current_rms": 10.5, "power_w": 2412.9, "power_factor": 0.97},
            "phase_c": {"voltage_rms": 231.2, "current_rms": 11.2, "power_w": 2589.4, "power_factor": 0.99},
        },
        "total_power_w": 7790.1,
    }

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
def ingest_telemetry_batch(readings: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"status": "accepted", "records_processed": len(readings)}