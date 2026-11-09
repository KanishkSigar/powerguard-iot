"""
PowerGuard IoT — Monthly Energy Rollup Tests
Validates multi-day aggregation, peak day detection, and total monthly billing calculations.
"""
from typing import List, Dict, Any
import pytest


def aggregate_monthly_usage(daily_summaries: List[Dict[str, Any]], base_charge: float = 0.0) -> Dict[str, Any]:
    """Rolls up daily consumption summaries into monthly billing overview."""
    if not daily_summaries:
        return {"month_total_kwh": 0.0, "avg_daily_kwh": 0.0, "peak_day": "", "peak_day_kwh": 0.0, "total_cost_inr": base_charge, "days_recorded": 0}

    total_kwh = sum(d["kwh"] for d in daily_summaries)
    days = len(daily_summaries)
    avg_daily_kwh = round(total_kwh / days, 2) if days > 0 else 0.0
    peak_day = max(daily_summaries, key=lambda d: d["kwh"])
    total_cost = sum(d.get("cost_inr", 0.0) for d in daily_summaries) + base_charge

    return {
        "month_total_kwh": round(total_kwh, 2),
        "avg_daily_kwh": avg_daily_kwh,
        "peak_day": peak_day["date"],
        "peak_day_kwh": peak_day["kwh"],
        "total_cost_inr": round(total_cost, 2),
        "days_recorded": days,
    }


def test_monthly_usage_aggregation():
    dailies = [
        {"date": "2026-11-01", "kwh": 12.0, "cost_inr": 84.0},
        {"date": "2026-11-02", "kwh": 18.5, "cost_inr": 129.5},
        {"date": "2026-11-03", "kwh": 14.0, "cost_inr": 98.0},
    ]
    res = aggregate_monthly_usage(dailies, base_charge=150.0)
    assert res["month_total_kwh"] == 44.5
    assert res["avg_daily_kwh"] == 14.83
    assert res["peak_day"] == "2026-11-02"
    assert res["peak_day_kwh"] == 18.5
    assert res["total_cost_inr"] == 461.50
    assert res["days_recorded"] == 3


def test_monthly_usage_empty():
    res = aggregate_monthly_usage([], base_charge=100.0)
    assert res["month_total_kwh"] == 0.0
    assert res["total_cost_inr"] == 100.0
    assert res["days_recorded"] == 0