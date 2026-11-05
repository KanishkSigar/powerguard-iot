"""
PowerGuard IoT — Active User Sessions API Router
Tracks active web and mobile operator sessions with remote termination capabilities.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/sessions", tags=["Sessions"])

_SESSIONS = [
    {"session_id": "SES-101", "user_id": "usr-01", "ip": "192.168.1.50", "client": "Dashboard WebApp (Chrome/Win11)", "is_current": True},
    {"session_id": "SES-102", "user_id": "usr-01", "ip": "10.0.0.12", "client": "PowerGuard Mobile (Android)", "is_current": False},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_sessions() -> Dict[str, Any]:
    return {"total": len(_SESSIONS), "items": _SESSIONS}

@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
def terminate_session(session_id: str) -> Dict[str, Any]:
    for s in _SESSIONS:
        if s["session_id"] == session_id:
            _SESSIONS.remove(s)
            return {"message": "Session terminated", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")