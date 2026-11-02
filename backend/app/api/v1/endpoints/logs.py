"""
PowerGuard IoT — Logs API Router
Collects edge diagnostic logs and delivers filtered server log streams.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, Query, status

router = APIRouter(prefix="/logs", tags=["Logs"])

_LOGS = [
    {"timestamp": "2026-11-02T15:00:00Z", "level": "INFO", "source": "MQTT", "message": "Telemetry batch ingested for DEV-ESP32-001"},
    {"timestamp": "2026-11-02T15:01:00Z", "level": "WARN", "source": "ALERTS", "message": "High apparent power on Phase B"},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_logs(level: str = Query("ALL")) -> Dict[str, Any]:
    if level != "ALL":
        return {"items": [log for log in _LOGS if log["level"] == level.upper()]}
    return {"items": _LOGS}