"""
PowerGuard IoT — Audit API Router
Compliance and audit trail query endpoint for administrative configuration changes.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/audit", tags=["Audit"])

_AUDIT_TRAIL = [
    {"event_id": "AUD-001", "action": "tariff.update", "actor": "admin", "timestamp": "2026-11-02T10:00:00Z"},
    {"event_id": "AUD-002", "action": "device.reboot", "actor": "technician_1", "timestamp": "2026-11-02T12:30:00Z"},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_audit_events() -> Dict[str, Any]:
    return {"total": len(_AUDIT_TRAIL), "items": _AUDIT_TRAIL}