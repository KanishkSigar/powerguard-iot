"""
PowerGuard IoT — Anomalies API Router
Provides endpoints to review ML-inferred electrical consumption anomalies and mark feedback.
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Query, status, HTTPException

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])

_ANOMALIES = [
    {"record_id": "ANOM-001", "device_id": "DEV-ESP32-001", "score": 0.94, "category": "abnormal_spike", "is_false_positive": False},
    {"record_id": "ANOM-002", "device_id": "DEV-ESP32-002", "score": 0.81, "category": "phantom_load", "is_false_positive": False},
]

@router.get("/", status_code=status.HTTP_200_OK)
def list_anomalies(min_score: float = Query(0.7, ge=0.0, le=1.0)) -> Dict[str, Any]:
    matched = [a for a in _ANOMALIES if a["score"] >= min_score]
    return {"total": len(matched), "items": matched}

@router.post("/{record_id}/feedback", status_code=status.HTTP_200_OK)
def mark_false_positive(record_id: str, is_false_positive: bool = Query(...)) -> Dict[str, Any]:
    for a in _ANOMALIES:
        if a["record_id"] == record_id:
            a["is_false_positive"] = is_false_positive
            return {"message": "Feedback recorded", "record_id": record_id, "is_false_positive": is_false_positive}
    raise HTTPException(status_code=404, detail="Anomaly record not found")