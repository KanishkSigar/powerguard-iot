"""
PowerGuard IoT — Reports API Router
Generates daily executive consumption reports and periodic analytics summaries.
"""
from typing import Dict, Any
from fastapi import APIRouter, Query, status

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/daily", status_code=status.HTTP_200_OK)
def get_daily_report(date: str = Query("2026-11-02", description="Report date in YYYY-MM-DD")) -> Dict[str, Any]:
    return {
        "date": date,
        "total_consumption_kwh": 182.4,
        "peak_demand_kw": 22.1,
        "off_peak_share_percent": 62.5,
        "carbon_footprint_kg_co2": 124.0,
        "estimated_cost_inr": 1368.0,
    }