"""
PowerGuard IoT — Advanced Analytics Service
Computes statistical telemetry metrics, power ratios, and phase balance evaluations.
"""
from typing import Dict, List, Any
import math, statistics

class AdvancedAnalyticsService:
    def __init__(self):
        self.is_active: bool = True

    def compute_summary_statistics(self, readings: List[float]) -> Dict[str, float]:
        if not readings:
            return {"count": 0, "mean": 0.0, "std_dev": 0.0, "min": 0.0, "max": 0.0}
        count = len(readings)
        avg = float(statistics.mean(readings))
        std = float(statistics.stdev(readings)) if count > 1 else 0.0
        return {"count": count, "mean": round(avg, 2), "std_dev": round(std, 2), "min": round(min(readings), 2), "max": round(max(readings), 2)}

    def calculate_papr(self, peak_power: float, average_power: float) -> float:
        if average_power <= 0 or peak_power <= 0:
            return 0.0
        return round(10.0 * math.log10(peak_power / average_power), 2)

    def detect_unbalanced_phases(self, phase_a: float, phase_b: float, phase_c: float) -> Dict[str, Any]:
        avg_phase = (phase_a + phase_b + phase_c) / 3.0
        if avg_phase <= 0:
            return {"unbalance_percent": 0.0, "is_critical": False}
        max_deviation = max(abs(phase_a - avg_phase), abs(phase_b - avg_phase), abs(phase_c - avg_phase))
        unbalance_percent = round((max_deviation / avg_phase) * 100.0, 2)
        return {"unbalance_percent": unbalance_percent, "is_critical": unbalance_percent > 3.0}