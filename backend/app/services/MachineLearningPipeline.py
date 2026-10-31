"""
PowerGuard IoT — Machine Learning Pipeline
Provides data preparation, min-max feature scaling, and windowing for anomaly detectors.
"""
from typing import List

class MachineLearningPipeline:
    def __init__(self):
        self.is_active: bool = True

    def normalize_features(self, raw_values: List[float], min_val: float, max_val: float) -> List[float]:
        if max_val <= min_val: return [0.5 for _ in raw_values]
        spread = max_val - min_val
        return [round(max(0.0, min(1.0, (v - min_val) / spread)), 4) for v in raw_values]

    def create_sliding_windows(self, series: List[float], window_size: int = 5, step: int = 1) -> List[List[float]]:
        if len(series) < window_size or window_size <= 0: return []
        return [series[i : i + window_size] for i in range(0, len(series) - window_size + 1, step)]