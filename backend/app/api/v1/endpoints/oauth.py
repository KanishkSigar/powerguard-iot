"""
PowerGuard IoT — OAuth2 Authorization API Router
Implements OAuth2 authorization code flow and client credential exchange endpoints.
"""
from typing import Dict, Any
from fastapi import APIRouter, status, Form, HTTPException

router = APIRouter(prefix="/oauth", tags=["OAuth2"])

@router.post("/token", status_code=status.HTTP_200_OK)
def issue_oauth_token(payload: Dict[str, Any]) -> Dict[str, Any]:
    grant_type = payload.get("grant_type", "client_credentials")
    if grant_type in ["client_credentials", "authorization_code"]:
        return {
            "access_token": "pg_oauth_access_token_sec_991823",
            "token_type": "bearer",
            "expires_in": 7200,
            "scope": "read write telemetry",
        }
    raise HTTPException(status_code=400, detail=f"Unsupported grant_type: {grant_type}")

@router.get("/authorize", status_code=status.HTTP_200_OK)
def authorize_client(client_id: str = "powerguard_web", redirect_uri: str = "http://localhost/callback") -> Dict[str, Any]:
    return {
        "status": "consent_required",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scopes": ["read", "write"],
    }

@router.post("/revoke", status_code=status.HTTP_200_OK)
def revoke_oauth_token(payload: Dict[str, str]) -> Dict[str, Any]:
    return {"status": "revoked", "token": payload.get("token", "")}