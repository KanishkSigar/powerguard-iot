"""
PowerGuard IoT — Webhooks API Router
Registers external HTTP webhook callbacks triggered on critical threshold violations.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

_WEBHOOKS = [
    {"webhook_id": "WHK-01", "target_url": "https://api.ops.company.com/power-alert", "events": ["overcurrent", "power_loss"], "is_active": True},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_webhooks() -> Dict[str, Any]:
    return {"total": len(_WEBHOOKS), "items": _WEBHOOKS}

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    whk = {
        "webhook_id": f"WHK-{len(_WEBHOOKS)+1:02d}",
        "target_url": payload.get("target_url", ""),
        "events": payload.get("events", ["all"]),
        "is_active": True,
    }
    _WEBHOOKS.append(whk)
    return {"message": "Webhook registered", "webhook": whk}