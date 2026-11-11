"""PowerGuard IoT — Dashboard Metrics Aggregation Tests"""
import pytest

def aggregate_dashboard_kpis(device_telemetry: list) -> dict:
    if not device_telemetry:
        return {"total_power_kw": 0.0, "active_devices": 0, "avg_power_factor": 1.0}
    total_watts = sum(d.get("power_w", 0.0) for d in device_telemetry)
    pfs = [d.get("power_factor", 1.0) for d in device_telemetry if "power_factor" in d]
    avg_pf = round(sum(pfs) / len(pfs), 2) if pfs else 1.0
    active_count = len(set(d.get("device_id") for d in device_telemetry if d.get("device_id")))
    return {
        "total_power_kw": round(total_watts / 1000.0, 2),
        "active_devices": active_count,
        "avg_power_factor": avg_pf,
    }

def test_dashboard_kpi_aggregation():
    data = [
        {"device_id": "D1", "power_w": 2500.0, "power_factor": 0.98},
        {"device_id": "D2", "power_w": 3500.0, "power_factor": 0.96},
        {"device_id": "D1", "power_w": 1000.0, "power_factor": 0.94},
    ]
    kpis = aggregate_dashboard_kpis(data)
    assert kpis["total_power_kw"] == 7.0
    assert kpis["active_devices"] == 2
    assert kpis["avg_power_factor"] == 0.96

def test_dashboard_kpi_empty():
    kpis = aggregate_dashboard_kpis([])
    assert kpis["total_power_kw"] == 0.0
    assert kpis["active_devices"] == 0