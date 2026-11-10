"""PowerGuard IoT — Device Status Assessment Tests"""
import time, pytest

def calculate_device_status(last_heartbeat_s: float, timeout_s: float = 120.0, current_time: float = None) -> str:
    now = current_time if current_time is not None else time.time()
    diff = now - last_heartbeat_s
    if diff <= timeout_s: return "online"
    elif diff <= timeout_s * 3: return "warning"
    return "offline"

def test_device_online():
    assert calculate_device_status(950.0, timeout_s=100.0, current_time=1000.0) == "online"

def test_device_warning():
    assert calculate_device_status(850.0, timeout_s=100.0, current_time=1000.0) == "warning"

def test_device_offline():
    assert calculate_device_status(500.0, timeout_s=100.0, current_time=1000.0) == "offline"