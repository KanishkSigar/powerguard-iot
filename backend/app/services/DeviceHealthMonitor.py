"""
PowerGuard IoT — Device Health Monitor
Assesses edge microcontroller operational vitality, telemetry latency, and connectivity.
"""
from typing import Dict, Any

class DeviceHealthMonitor:
    def __init__(self):
        self.offline_timeout_seconds: float = 120.0

    def evaluate_health(self, last_heartbeat_delta_s: float, wifi_rssi: int, free_heap_bytes: int) -> Dict[str, Any]:
        if last_heartbeat_delta_s > self.offline_timeout_seconds:
            return {"status": "offline", "health_score": 0.0, "is_critical": True}
        rssi_score = max(0.0, min(1.0, (wifi_rssi + 90) / 60.0))
        heap_score = min(1.0, free_heap_bytes / 80000.0)
        overall_score = round((rssi_score * 0.4 + heap_score * 0.6) * 100.0, 1)
        status = "healthy" if overall_score >= 70 else ("degraded" if overall_score >= 40 else "warning")
        return {"status": status, "health_score": overall_score, "wifi_quality": "good" if wifi_rssi > -67 else "fair", "is_critical": overall_score < 40}

    def is_device_offline(self, last_seen_seconds: float, timeout_threshold: float = None) -> bool:
        limit = timeout_threshold if timeout_threshold is not None else self.offline_timeout_seconds
        return last_seen_seconds > limit