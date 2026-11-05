"""
PowerGuard IoT — API Keys Management Router
Issues, lists, and revokes machine-to-machine API keys for external integration.
"""
from typing import Dict, Any, List
from fastapi import APIRouter, status, HTTPException

router = APIRouter(prefix="/keys", tags=["API Keys"])

_KEYS = [
    {"key_id": "KEY-01", "name": "Grafana Reader", "prefix": "pg_live_9a8f", "scopes": ["readings.read"], "is_active": True},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_keys() -> Dict[str, Any]:
    return {"total": len(_KEYS), "items": _KEYS}

@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_key(payload: Dict[str, Any]) -> Dict[str, Any]:
    key_entry = {
        "key_id": f"KEY-{len(_KEYS)+1:02d}",
        "name": payload.get("name", "Integration Key"),
        "prefix": "pg_live_b4c1",
        "raw_token": "pg_live_b4c198fe710293847aa1928374",
        "scopes": payload.get("scopes", ["readings.read"]),
        "is_active": True,
    }
    _KEYS.append(key_entry)
    return {"message": "API key generated", "key": key_entry}

@router.delete("/{key_id}", status_code=status.HTTP_200_OK)
def revoke_key(key_id: str) -> Dict[str, Any]:
    for k in _KEYS:
        if k["key_id"] == key_id:
            k["is_active"] = False
            return {"message": "API key revoked", "key_id": key_id}
    raise HTTPException(status_code=404, detail="API key not found")