"""
PowerGuard IoT — Firmware API Router
Controls Over-The-Air (OTA) binary distributions, checksum validation, and rollback operations.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/firmware", tags=["Firmware"])

_RELEASES = [
    {"version": "2.4.1", "channel": "stable", "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "size_bytes": 1048576},
]

@router.get("/releases", status_code=status.HTTP_200_OK)
def list_firmware_releases() -> Dict[str, Any]:
    return {"total": len(_RELEASES), "items": _RELEASES}

@router.post("/rollback", status_code=status.HTTP_200_OK)
def trigger_rollback(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "initiated",
        "device_id": payload.get("device_id", "DEV-ESP32-001"),
        "target_partition": "ota_0",
        "action": "reboot_and_switch",
    }