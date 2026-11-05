"""
PowerGuard IoT — User Preferences API Router
Stores operator UI configurations, telemetry units, and notification preferences.
"""
from typing import Dict, Any
from fastapi import APIRouter, status

router = APIRouter(prefix="/preferences", tags=["Preferences"])

_PREFERENCES = {
    "theme": "dark",
    "currency": "INR",
    "telemetry_refresh_interval_ms": 2000,
    "email_alerts_enabled": True,
    "sound_alerts_enabled": False,
    "default_channel_view": "all",
}

@router.get("/", status_code=status.HTTP_200_OK)
def get_preferences() -> Dict[str, Any]:
    return _PREFERENCES

@router.put("/", status_code=status.HTTP_200_OK)
def update_preferences(updates: Dict[str, Any]) -> Dict[str, Any]:
    _PREFERENCES.update(updates)
    return {"message": "Preferences updated", "preferences": _PREFERENCES}