"""
PowerGuard IoT — Daily Energy Usage Calculation Tests
Validates daily consumption summaries, peak power tracking, and cost calculation.
"""
from typing import List, Dict, Any
import pytest


def aggregate_daily_usage(readings: List[Dict[str, Any]], tariff_rate: float) -> Dict[str, Any]:
    """Calculates daily summary metrics from individual channel telemetry readings."""
    if not readings:
        return {"total_kwh": 0.0, "peak_power_w": 0.0, "avg_power_w": 0.0, "cost_inr": 0.0, "sample_count": 0}
    
    total_kwh = sum(r.get("kwh", 0.0) for r in readings)
    powers = [r.get("power_w", 0.0) for r in readings]
    peak_w = max(powers) if powers else 0.0
    avg_w = sum(powers) / len(powers) if powers else 0.0
    cost = round(total_kwh * tariff_rate, 2)
    
    return {
        "total_kwh": round(total_kwh, 3),
        "peak_power_w": round(peak_w, 2),
        "avg_power_w": round(avg_w, 2),
        "cost_inr": cost,
        "sample_count": len(readings),
    }


def test_daily_usage_calculation():
    samples = [
        {"kwh": 1.2, "power_w": 2400.0},
        {"kwh": 1.5, "power_w": 3000.0},
        {"kwh": 0.8, "power_w": 1600.0},
    ]
    summary = aggregate_daily_usage(samples, tariff_rate=7.0)
    assert summary["total_kwh"] == 3.5
    assert summary["peak_power_w"] == 3000.0
    assert summary["avg_power_w"] == 2333.33
    assert summary["cost_inr"] == 24.50
    assert summary["sample_count"] == 3


def test_daily_usage_empty():
    summary = aggregate_daily_usage([], tariff_rate=7.0)
    assert summary["total_kwh"] == 0.0
    assert summary["cost_inr"] == 0.0
    assert summary["sample_count"] == 0