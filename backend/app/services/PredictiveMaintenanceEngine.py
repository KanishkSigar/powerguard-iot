"""
PowerGuard IoT — Predictive Maintenance Engine
Estimates motor/transformer wear, insulation degradation, and Remaining Useful Life (RUL).
"""
class PredictiveMaintenanceEngine:
    def __init__(self):
        self.is_active: bool = True

    def calculate_degradation_index(self, current_pf: float, nominal_pf: float, operating_hours: float) -> float:
        pf_drop = max(0.0, nominal_pf - current_pf)
        hour_factor = min(1.0, operating_hours / 50000.0)
        return round(min(1.0, max(0.0, (pf_drop * 1.5) + (hour_factor * 0.5))), 3)

    def estimate_remaining_useful_life_hours(self, current_health_score: float, degradation_rate_per_hour: float) -> float:
        if degradation_rate_per_hour <= 0: return 999999.0
        remaining = max(0.0, current_health_score - 20.0)
        return round(max(0.0, remaining / degradation_rate_per_hour), 1)