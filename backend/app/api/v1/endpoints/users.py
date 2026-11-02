"""
PowerGuard IoT — Users API Router
Manages technician and operator user accounts, roles, and status.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/users", tags=["Users"])

_USERS = [
    {"user_id": "usr-01", "username": "admin", "role": "Administrator", "is_active": True},
    {"user_id": "usr-02", "username": "field_tech_raj", "role": "Technician", "is_active": True},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_users() -> Dict[str, Any]:
    return {"total": len(_USERS), "items": _USERS}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(payload: Dict[str, Any]) -> Dict[str, Any]:
    user = {"user_id": f"usr-{len(_USERS)+1:02d}", "username": payload.get("username", "user"), "role": payload.get("role", "Viewer"), "is_active": True}
    _USERS.append(user)
    return {"message": "User created", "user": user}