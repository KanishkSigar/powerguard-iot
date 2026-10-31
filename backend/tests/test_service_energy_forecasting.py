"""PowerGuard IoT — Energy Forecasting & Solar Prediction Tests"""
import pytest
from app.services.EnergyUsageForecaster import EnergyUsageForecaster
from app.services.SolarGenerationPredictor import SolarGenerationPredictor

def test_energy_usage_forecaster_24h():
    forecaster = EnergyUsageForecaster()
    forecast = forecaster.forecast_next_24h([2.5] * 24)
    assert len(forecast) == 24
    assert all(f >= 0.0 for f in forecast)

def test_forecast_confidence_intervals():
    forecaster = EnergyUsageForecaster()
    intervals = forecaster.calculate_forecast_confidence_interval([10.0])
    assert intervals[0]["lower_bound"] <= 10.0 <= intervals[0]["upper_bound"]

def test_solar_instantaneous_power():
    predictor = SolarGenerationPredictor()
    assert 4.9 <= predictor.predict_instantaneous_power(5.0, 12.0) <= 5.1
    assert predictor.predict_instantaneous_power(5.0, 2.0) == 0.0

def test_solar_daily_yield():
    predictor = SolarGenerationPredictor()
    assert predictor.estimate_daily_yield_kwh(5.0, 5.0, 0.8) == 20.0