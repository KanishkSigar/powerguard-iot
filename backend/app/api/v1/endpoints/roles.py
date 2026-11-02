"""
PowerGuard IoT — Roles API Router
Defines system access roles for Role-Based Access Control (RBAC).
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/roles", tags=["Roles"])

_ROLES = [
    {"role_name": "Administrator", "description": "Full access to telemetry, hardware config, and tariffs"},
    {"role_name": "Operator", "description": "Can acknowledge alerts and view dashboard charts"},
    {"role_name": "Viewer", "description": "Read-only access to power consumption stats"},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_roles() -> Dict[str, Any]:
    return {"total": len(_ROLES), "items": _ROLES}