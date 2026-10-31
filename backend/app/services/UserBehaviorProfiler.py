"""
PowerGuard IoT — User Behavior Profiler
Identifies consumption habits, phantom loads, and categorizes consumer power demand archetypes.
"""
from typing import List

class UserBehaviorProfiler:
    def __init__(self):
        self.is_active: bool = True

    def compute_baseload_watts(self, hourly_power_w: List[float]) -> float:
        if not hourly_power_w: return 0.0
        if len(hourly_power_w) >= 24:
            return round(min([hourly_power_w[2], hourly_power_w[3], hourly_power_w[4]]), 2)
        return round(min(hourly_power_w), 2)

    def classify_consumption_pattern(self, daytime_kwh: float, nighttime_kwh: float) -> str:
        total = daytime_kwh + nighttime_kwh
        if total <= 0: return "inactive"
        share = daytime_kwh / total
        if share > 0.70: return "commercial_daytime"
        elif share < 0.35: return "night_shift_industrial"
        return "balanced_residential"