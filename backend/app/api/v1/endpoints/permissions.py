"""
PowerGuard IoT — Permissions API Router
Lists fine-grained security permissions and checks operator authorizations.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/permissions", tags=["Permissions"])

_PERMISSIONS = [
    "devices.read", "devices.write", "telemetry.read",
    "alerts.acknowledge", "tariffs.modify", "firmware.deploy",
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_permissions() -> Dict[str, Any]:
    return {"total": len(_PERMISSIONS), "permissions": _PERMISSIONS}