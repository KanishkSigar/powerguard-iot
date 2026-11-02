"""
PowerGuard IoT — Alerts API Router
Manages threshold violation alerts, incident escalation, and acknowledgment.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query, status, HTTPException

router = APIRouter(prefix="/alerts", tags=["Alerts"])

_ALERTS = [
    {"alert_id": "ALT-101", "device_id": "DEV-ESP32-001", "severity": "warning", "metric": "current", "message": "High current on Phase A", "acknowledged": False},
    {"alert_id": "ALT-102", "device_id": "DEV-ESP32-002", "severity": "critical", "metric": "voltage", "message": "Voltage sag below 200V", "acknowledged": True},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_alerts(severity: Optional[str] = Query(None), acknowledged: Optional[bool] = Query(None)) -> Dict[str, Any]:
    res = _ALERTS
    if severity:
        res = [a for a in res if a["severity"].lower() == severity.lower()]
    if acknowledged is not None:
        res = [a for a in res if a["acknowledged"] == acknowledged]
    return {"total": len(res), "items": res}

@router.post("/{alert_id}/acknowledge", status_code=status.HTTP_200_OK)
def acknowledge_alert(alert_id: str) -> Dict[str, Any]:
    for a in _ALERTS:
        if a["alert_id"] == alert_id:
            a["acknowledged"] = True
            return {"message": "Alert acknowledged", "alert_id": alert_id}
    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")