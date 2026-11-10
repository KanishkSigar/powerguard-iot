"""PowerGuard IoT — Search & Query Filtering Tests"""
import pytest

def filter_telemetry(records: list, device_id: str = None, min_voltage: float = None, channel: str = None) -> list:
    res = records
    if device_id: res = [r for r in res if r.get("device_id") == device_id]
    if min_voltage is not None: res = [r for r in res if r.get("voltage", 0) >= min_voltage]
    if channel: res = [r for r in res if r.get("channel") == channel]
    return res

def test_filter_by_device_and_channel():
    data = [
        {"device_id": "DEV-1", "channel": "main", "voltage": 230.0},
        {"device_id": "DEV-1", "channel": "sub", "voltage": 220.0},
        {"device_id": "DEV-2", "channel": "main", "voltage": 240.0},
    ]
    res = filter_telemetry(data, device_id="DEV-1", channel="main")
    assert len(res) == 1
    assert res[0]["voltage"] == 230.0

def test_filter_by_voltage():
    data = [{"voltage": 210.0}, {"voltage": 230.0}, {"voltage": 245.0}]
    res = filter_telemetry(data, min_voltage=225.0)
    assert len(res) == 2