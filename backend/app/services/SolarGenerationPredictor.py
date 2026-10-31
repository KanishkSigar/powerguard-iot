"""
PowerGuard IoT — Solar Generation Predictor
Models photovoltaic yield and solar curve based on sun angle, panel rating, and cloud factor.
"""
import math

class SolarGenerationPredictor:
    def __init__(self):
        self.is_active: bool = True

    def predict_instantaneous_power(self, panel_capacity_kw: float, hour_of_day: float, cloud_cover_percent: float = 0.0) -> float:
        if hour_of_day < 6.0 or hour_of_day > 18.0 or panel_capacity_kw <= 0: return 0.0
        angle_rad = (hour_of_day - 6.0) * math.pi / 12.0
        clear_sky = panel_capacity_kw * math.sin(angle_rad)
        cloud_factor = max(0.1, 1.0 - (cloud_cover_percent / 100.0) * 0.8)
        return round(max(0.0, clear_sky * cloud_factor), 2)

    def estimate_daily_yield_kwh(self, panel_capacity_kw: float, peak_sun_hours: float = 5.2, performance_ratio: float = 0.8) -> float:
        if panel_capacity_kw <= 0 or peak_sun_hours <= 0: return 0.0
        return round(max(0.0, panel_capacity_kw * peak_sun_hours * performance_ratio), 2)