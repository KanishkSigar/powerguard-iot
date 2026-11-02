"""
PowerGuard IoT — Settings API Router
Manages global platform configuration parameters, grid voltage nominals, and units.
"""
from typing import Dict, Any
from fastapi import APIRouter, status

router = APIRouter(prefix="/settings", tags=["Settings"])

_SETTINGS = {
    "grid_nominal_voltage_v": 230.0,
    "grid_nominal_frequency_hz": 50.0,
    "default_currency": "INR",
    "telemetry_retention_days": 365,
}

@router.get("/", status_code=status.HTTP_200_OK)
def get_settings() -> Dict[str, Any]:
    return _SETTINGS

@router.put("/", status_code=status.HTTP_200_OK)
def update_settings(updates: Dict[str, Any]) -> Dict[str, Any]:
    _SETTINGS.update(updates)
    return {"message": "Settings updated", "settings": _SETTINGS}