"""
PowerGuard IoT — Devices API Router
Provides hardware node registration, lifecycle management, and discovery endpoints.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/devices", tags=["Devices"])

_MOCK_DEVICES = [
    {"device_id": "DEV-ESP32-001", "name": "Main Distribution Panel", "status": "online", "channels": 3, "ip": "192.168.1.101"},
    {"device_id": "DEV-ESP32-002", "name": "HVAC Chiller Plant", "status": "online", "channels": 3, "ip": "192.168.1.102"},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_devices(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by operational status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> Dict[str, Any]:
    devices = _MOCK_DEVICES
    if status_filter:
        devices = [d for d in devices if d["status"].lower() == status_filter.lower()]
    return {"total": len(devices), "items": devices[skip : skip + limit]}

@router.get("/{device_id}", status_code=status.HTTP_200_OK)
def get_device(device_id: str) -> Dict[str, Any]:
    for dev in _MOCK_DEVICES:
        if dev["device_id"] == device_id:
            return dev
    raise HTTPException(status_code=404, detail=f"Device {device_id} not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_device(payload: Dict[str, Any]) -> Dict[str, Any]:
    device_id = payload.get("device_id", f"DEV-ESP32-{len(_MOCK_DEVICES)+1:03d}")
    new_dev = {"device_id": device_id, "name": payload.get("name", "New Node"), "status": "online", "channels": payload.get("channels", 3)}
    return {"message": "Device registered successfully", "device": new_dev}