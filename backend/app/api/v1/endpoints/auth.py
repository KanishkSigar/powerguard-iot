"""
PowerGuard IoT — Authentication API Router
Issues JWT access tokens and authenticates operators and IoT edge nodes.
"""
from typing import Dict, Any
from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: Dict[str, str]) -> Dict[str, Any]:
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    if username == "admin" and password == "powerguard":
        return {
            "access_token": "mock_jwt_token_powerguard_admin_2026",
            "token_type": "bearer",
            "expires_in_seconds": 3600,
        }
    raise HTTPException(status_code=401, detail="Invalid username or credentials")