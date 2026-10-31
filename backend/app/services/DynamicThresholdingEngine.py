"""
PowerGuard IoT — Dynamic Thresholding Engine
Calculates adaptive statistical thresholds based on rolling baselines and standard deviations.
"""
from typing import Dict, List, Optional
import statistics

class DynamicThresholdingEngine:
    def __init__(self):
        self.default_sigma_multiplier: float = 3.0

    def calculate_adaptive_bounds(self, history: List[float], sigma_multiplier: Optional[float] = None) -> Dict[str, float]:
        if not history:
            return {"mean": 0.0, "std_dev": 0.0, "upper_bound": 0.0, "lower_bound": 0.0}
        mult = sigma_multiplier if sigma_multiplier is not None else self.default_sigma_multiplier
        mean_val = float(statistics.mean(history))
        std_val = float(statistics.stdev(history)) if len(history) > 1 else 0.0
        return {"mean": round(mean_val, 2), "std_dev": round(std_val, 2), "upper_bound": round(mean_val + (mult * std_val), 2), "lower_bound": round(max(0.0, mean_val - (mult * std_val)), 2)}

    def is_outlier(self, value: float, upper_bound: float, lower_bound: float) -> bool:
        return value > upper_bound or value < lower_bound