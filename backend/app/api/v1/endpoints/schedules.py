"""
PowerGuard IoT — Schedules API Router
Provides scheduling endpoints for smart load shedding, battery charging, and relay automation.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/schedules", tags=["Schedules"])

_SCHEDULES = [
    {"schedule_id": "SCH-01", "appliance": "Water Heater", "start_time": "23:00", "duration_min": 120, "is_active": True},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_schedules() -> Dict[str, Any]:
    return {"total": len(_SCHEDULES), "items": _SCHEDULES}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_schedule(payload: Dict[str, Any]) -> Dict[str, Any]:
    new_sch = {
        "schedule_id": f"SCH-{len(_SCHEDULES)+1:02d}",
        "appliance": payload.get("appliance", "Generic Relay"),
        "start_time": payload.get("start_time", "00:00"),
        "duration_min": payload.get("duration_min", 60),
        "is_active": True,
    }
    _SCHEDULES.append(new_sch)
    return {"message": "Schedule created", "schedule": new_sch}