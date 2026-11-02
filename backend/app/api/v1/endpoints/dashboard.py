"""
PowerGuard IoT — Dashboard API Router
Provides aggregated metrics, key performance indicators (KPIs), and executive summary statistics.
"""
from typing import Dict, Any
from fastapi import APIRouter, status

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", status_code=status.HTTP_200_OK)
def get_dashboard_summary() -> Dict[str, Any]:
    return {
        "active_devices_count": 5,
        "total_power_kw": 18.4,
        "today_energy_kwh": 142.6,
        "monthly_cost_estimate_inr": 18450.0,
        "system_health": "optimal",
        "grid_dependency_percent": 35.0,
    }

@router.get("/chart-data", status_code=status.HTTP_200_OK)
def get_chart_data() -> Dict[str, Any]:
    return {
        "labels": [f"{h:02d}:00" for h in range(24)],
        "power_kw": [5.2 + (2.5 if 9 <= h <= 18 else 0.5) for h in range(24)],
    }