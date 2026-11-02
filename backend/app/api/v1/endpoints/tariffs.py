"""
PowerGuard IoT — Tariffs API Router
Configures utility electricity tariff plans and Time-of-Use (ToU) billing rate structures.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/tariffs", tags=["Tariffs"])

_TARIFFS = [
    {
        "tariff_id": "COMM-TOU-2026",
        "provider": "State Electricity Board",
        "currency": "INR",
        "base_rate": 7.50,
        "peak_rate": 11.20,
        "off_peak_rate": 5.40,
        "is_active": True,
    }
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_tariffs() -> Dict[str, Any]:
    return {"total": len(_TARIFFS), "items": _TARIFFS}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tariff(tariff: Dict[str, Any]) -> Dict[str, Any]:
    _TARIFFS.append(tariff)
    return {"message": "Tariff plan created", "tariff": tariff}