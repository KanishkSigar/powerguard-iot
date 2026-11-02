"""
PowerGuard IoT — Notifications API Router
Inbox for operator alerts, scheduled notifications, and device disconnect notices.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status

router = APIRouter(prefix="/notifications", tags=["Notifications"])

_NOTIFICATIONS = [
    {"id": "NOTIF-1", "title": "Grid Voltage High", "unread": True, "created_at": "2026-11-02T14:30:00Z"},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_notifications() -> Dict[str, Any]:
    return {"total": len(_NOTIFICATIONS), "items": _NOTIFICATIONS}

@router.post("/mark-all-read", status_code=status.HTTP_200_OK)
def mark_all_read() -> Dict[str, Any]:
    for n in _NOTIFICATIONS:
        n["unread"] = False
    return {"message": "All notifications marked as read"}