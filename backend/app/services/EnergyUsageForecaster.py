"""
PowerGuard IoT — Energy Usage Forecaster
Generates multi-step short-term power consumption projections using weighted historical decay.
"""
from typing import Dict, List
import math

class EnergyUsageForecaster:
    def __init__(self):
        self.is_active: bool = True

    def forecast_next_24h(self, historical_hourly_kwh: List[float], decay_factor: float = 0.85) -> List[float]:
        if not historical_hourly_kwh:
            return [0.0] * 24
        recent = historical_hourly_kwh[-24:]
        base = sum(recent) / len(recent)
        forecasts = []
        for hour in range(24):
            mult = 1.0 + 0.3 * math.sin((hour - 9) * math.pi / 12)
            predicted = round(base * mult * decay_factor + base * (1.0 - decay_factor), 2)
            forecasts.append(max(0.0, predicted))
        return forecasts

    def calculate_forecast_confidence_interval(self, predictions: List[float], error_variance: float = 0.05) -> List[Dict[str, float]]:
        intervals = []
        for val in predictions:
            margin = round(val * error_variance * 1.96, 2)
            intervals.append({"forecast": val, "lower_bound": round(max(0.0, val - margin), 2), "upper_bound": round(val + margin, 2)})
        return intervals