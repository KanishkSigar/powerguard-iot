"""PowerGuard IoT — Anomaly Scoring Unit Tests"""
import pytest

def compute_anomaly_score(value: float, mean: float, std_dev: float) -> dict:
    if std_dev <= 0: return {"z_score": 0.0, "severity": "normal"}
    z = abs(value - mean) / std_dev
    if z >= 3.0: sev = "critical"
    elif z >= 2.0: sev = "warning"
    else: sev = "normal"
    return {"z_score": round(z, 2), "severity": sev}

def test_anomaly_score_normal():
    res = compute_anomaly_score(232.0, 230.0, 5.0)
    assert res["z_score"] == 0.4
    assert res["severity"] == "normal"

def test_anomaly_score_critical():
    res = compute_anomaly_score(280.0, 230.0, 10.0)
    assert res["z_score"] == 5.0
    assert res["severity"] == "critical"