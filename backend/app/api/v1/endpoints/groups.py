"""
PowerGuard IoT — Device Groups API Router
Manages logical groupings of energy monitoring devices and physical facility zones.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/groups", tags=["Groups"])

_GROUPS = [
    {"group_id": "GRP-01", "name": "Main Manufacturing Plant", "zone": "Industrial Zone A", "device_count": 4},
    {"group_id": "GRP-02", "name": "Administrative Offices", "zone": "Commercial Block B", "device_count": 2},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_groups() -> Dict[str, Any]:
    return {"total": len(_GROUPS), "items": _GROUPS}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_group(payload: Dict[str, Any]) -> Dict[str, Any]:
    new_group = {
        "group_id": f"GRP-{len(_GROUPS)+1:02d}",
        "name": payload.get("name", "New Group"),
        "zone": payload.get("zone", "General Zone"),
        "device_count": 0,
    }
    _GROUPS.append(new_group)
    return {"message": "Device group created", "group": new_group}

@router.get("/{group_id}/devices", status_code=status.HTTP_200_OK)
def list_group_devices(group_id: str) -> Dict[str, Any]:
    return {"group_id": group_id, "devices": ["DEV-ESP32-001", "DEV-ESP32-002"]}