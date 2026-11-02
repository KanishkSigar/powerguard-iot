"""
PowerGuard IoT — Billing API Router
Calculates bill estimates, cost breakdowns, and tariff arbitrage projections.
"""
from typing import Dict, Any
from fastapi import APIRouter, Query, status

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.get("/estimate", status_code=status.HTTP_200_OK)
def estimate_bill(projected_days: int = Query(30, ge=1, le=90)) -> Dict[str, Any]:
    return {
        "projected_kwh": round(projected_days * 35.5, 2),
        "estimated_energy_cost_inr": round(projected_days * 35.5 * 7.5, 2),
        "fixed_charges_inr": 450.0,
        "estimated_tax_inr": round(projected_days * 35.5 * 7.5 * 0.18, 2),
        "currency": "INR",
    }