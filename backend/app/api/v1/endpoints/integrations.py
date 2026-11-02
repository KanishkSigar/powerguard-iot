"""
PowerGuard IoT — Integrations API Router
Configures connections to third-party home automation (Home Assistant, MQTT, Grafana).
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/integrations", tags=["Integrations"])

_INTEGRATIONS = [
    {"name": "Home Assistant", "type": "mqtt_discovery", "status": "connected"},
    {"name": "Grafana Enterprise", "type": "influx_datasource", "status": "connected"},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_integrations() -> Dict[str, Any]:
    return {"total": len(_INTEGRATIONS), "items": _INTEGRATIONS}