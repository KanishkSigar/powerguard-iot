"""
PowerGuard IoT — Cost Optimization Analyzer
Computes Time-of-Use (ToU) electricity expenditures and identifies load-shifting opportunities.
"""
from typing import Dict, List, Set

class CostOptimizationAnalyzer:
    def __init__(self):
        self.is_active: bool = True

    def compute_tou_cost(self, hourly_kwh: List[float], peak_hours: Set[int], peak_rate: float, off_peak_rate: float) -> Dict[str, float]:
        peak_cost = sum(kwh * peak_rate for h, kwh in enumerate(hourly_kwh) if h in peak_hours)
        off_peak_cost = sum(kwh * off_peak_rate for h, kwh in enumerate(hourly_kwh) if h not in peak_hours)
        return {"total_cost": round(peak_cost + off_peak_cost, 2), "peak_cost": round(peak_cost, 2), "off_peak_cost": round(off_peak_cost, 2)}

    def recommend_load_shift(self, hourly_kw: List[float], peak_hours: Set[int]) -> Dict[str, float]:
        peak_energy = sum(hourly_kw[h] for h in peak_hours if h < len(hourly_kw))
        return {"shiftable_kwh": round(peak_energy * 0.30, 2), "peak_consumption_kwh": round(peak_energy, 2)}