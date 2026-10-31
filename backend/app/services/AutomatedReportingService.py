"""
PowerGuard IoT — Automated Reporting Service
Generates structured daily summaries, efficiency metrics, and executive energy reports.
"""
from typing import Dict, List, Any

class AutomatedReportingService:
    def __init__(self):
        self.is_active: bool = True

    def generate_daily_summary(self, device_id: str, date_str: str, hourly_readings_kwh: List[float]) -> Dict[str, Any]:
        total_kwh = sum(hourly_readings_kwh)
        peak_kwh = max(hourly_readings_kwh) if hourly_readings_kwh else 0.0
        peak_hour = hourly_readings_kwh.index(peak_kwh) if hourly_readings_kwh else -1
        return {"device_id": device_id, "date": date_str, "total_kwh": round(total_kwh, 2), "peak_hour": peak_hour, "peak_kwh": round(peak_kwh, 2)}

    def calculate_efficiency_score(self, peak_power_w: float, base_power_w: float, avg_power_w: float) -> float:
        if peak_power_w <= 0 or avg_power_w <= 0: return 100.0
        score = ((avg_power_w / peak_power_w) * 70.0) + (min(1.0, base_power_w / avg_power_w) * 30.0)
        return round(min(100.0, max(0.0, score)), 2)