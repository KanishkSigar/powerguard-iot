"""PowerGuard IoT — Grafana Sync & Annotation Tests"""
import time
import pytest

def build_grafana_annotation(title: str, text: str, tags: list, timestamp_s: float = None) -> dict:
    epoch_ms = int((timestamp_s or time.time()) * 1000)
    return {
        "time": epoch_ms,
        "isRegion": False,
        "title": title,
        "text": text,
        "tags": tags,
    }

def test_grafana_annotation_structure():
    ann = build_grafana_annotation(
        title="Grid Sag Detected",
        text="Phase A dropped below 190V",
        tags=["power_anomaly", "phase_a"],
        timestamp_s=1794300000.0,
    )
    assert ann["time"] == 1794300000000
    assert ann["title"] == "Grid Sag Detected"
    assert "power_anomaly" in ann["tags"]
    assert ann["isRegion"] is False