"""
PowerGuard IoT — Metrics API Router
Reports power quality harmonics, frequency stability, and carbon emissions.
"""
from typing import Dict, Any
from fastapi import APIRouter, status

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/power-quality", status_code=status.HTTP_200_OK)
def get_power_quality_metrics() -> Dict[str, Any]:
    return {
        "grid_frequency_hz": 50.02,
        "thd_voltage_percent": 1.8,
        "thd_current_percent": 3.4,
        "power_factor_avg": 0.98,
        "quality_index": "A",
    }

@router.get("/carbon", status_code=status.HTTP_200_OK)
def get_carbon_metrics() -> Dict[str, Any]:
    return {
        "today_kg_co2": 42.5,
        "avoided_kg_co2": 18.2,
        "trees_equivalent_saved": 0.84,
    }