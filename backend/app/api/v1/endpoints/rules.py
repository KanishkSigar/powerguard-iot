"""
PowerGuard IoT — Rules API Router
Automated automation and threshold evaluation rules triggering smart relays and alerts.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/rules", tags=["Rules"])

_RULES = [
    {"rule_id": "RUL-01", "name": "Overcurrent Protection", "condition": "current_rms > 100", "action": "trigger_alert", "is_enabled": True},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_rules() -> Dict[str, Any]:
    return {"total": len(_RULES), "items": _RULES}