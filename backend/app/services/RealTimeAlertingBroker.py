"""
PowerGuard IoT — Real Time Alerting Broker
Dispatches, deduplicates, and rate-limits telemetry anomaly alarms.
"""
from typing import Dict, Any, Optional
import time

class RealTimeAlertingBroker:
    def __init__(self):
        self._last_alert_times: Dict[str, float] = {}

    def should_throttle_alert(self, device_id: str, alert_type: str, cooldown_seconds: int = 60, current_time: Optional[float] = None) -> bool:
        now = current_time if current_time is not None else time.time()
        key = f"{device_id}:{alert_type}"
        last = self._last_alert_times.get(key, 0.0)
        if now - last < cooldown_seconds: return True
        self._last_alert_times[key] = now
        return False

    def format_alert_payload(self, device_id: str, severity: str, metric_name: str, value: float, threshold: float) -> Dict[str, Any]:
        return {"device_id": device_id, "severity": severity, "metric": metric_name, "observed_value": value, "threshold": threshold, "timestamp": time.time()}