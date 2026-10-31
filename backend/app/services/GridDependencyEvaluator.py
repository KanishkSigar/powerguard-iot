"""
PowerGuard IoT — Grid Dependency Evaluator
Measures microgrid autonomy, solar self-consumption, and grid dependency ratios.
"""
from typing import Dict

class GridDependencyEvaluator:
    def __init__(self):
        self.is_active: bool = True

    def calculate_self_sufficiency(self, solar_generation_kwh: float, grid_import_kwh: float, total_load_kwh: float) -> Dict[str, float]:
        if total_load_kwh <= 0:
            return {"self_sufficiency_percent": 100.0, "grid_dependency_percent": 0.0, "solar_coverage_ratio": 1.0}
        solar_consumed = min(solar_generation_kwh, total_load_kwh)
        self_suff = round((solar_consumed / total_load_kwh) * 100.0, 2)
        return {"self_sufficiency_percent": min(100.0, self_suff), "grid_dependency_percent": min(100.0, round(max(0.0, 100.0 - self_suff), 2)), "solar_coverage_ratio": round(solar_generation_kwh / total_load_kwh, 2)}

    def calculate_net_energy(self, solar_kwh: float, load_kwh: float) -> float:
        return round(solar_kwh - load_kwh, 2)