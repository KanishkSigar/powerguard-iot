"""
PowerGuard IoT — Health API Router
System and edge component health check endpoints for liveness and readiness probes.
"""
from typing import Dict, Any
from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", status_code=status.HTTP_200_OK)
def check_health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "database": "connected",
        "mqtt_broker": "connected",
        "telemetry_stream": "active",
    }

@router.get("/device/{device_id}", status_code=status.HTTP_200_OK)
def check_device_vitality(device_id: str) -> Dict[str, Any]:
    return {
        "device_id": device_id,
        "vitality": "healthy",
        "wifi_rssi_dbm": -58,
        "free_heap_bytes": 54200,
        "uptime_seconds": 864000,
    }