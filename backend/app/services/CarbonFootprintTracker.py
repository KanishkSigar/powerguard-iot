"""
PowerGuard IoT — Carbon Footprint Tracker
Quantifies CO2 emissions and greenhouse gas offsets from renewable energy generation.
"""
from typing import Optional

class CarbonFootprintTracker:
    def __init__(self):
        self.default_grid_emission_factor_g_per_kwh: float = 680.0

    def calculate_emissions_kg(self, kwh: float, emission_factor_g_per_kwh: Optional[float] = None) -> float:
        factor = emission_factor_g_per_kwh if emission_factor_g_per_kwh is not None else self.default_grid_emission_factor_g_per_kwh
        return round(max(0.0, (kwh * factor) / 1000.0), 3)

    def calculate_avoided_emissions(self, solar_kwh: float, emission_factor_g_per_kwh: Optional[float] = None) -> float:
        return self.calculate_emissions_kg(solar_kwh, emission_factor_g_per_kwh)

    def get_trees_equivalent(self, kg_co2: float) -> float:
        return round(kg_co2 / 21.77, 2) if kg_co2 > 0 else 0.0