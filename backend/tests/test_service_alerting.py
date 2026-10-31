"""PowerGuard IoT — Dynamic Thresholding & Alert Broker Tests"""
import pytest
from app.services.DynamicThresholdingEngine import DynamicThresholdingEngine
from app.services.RealTimeAlertingBroker import RealTimeAlertingBroker

def test_dynamic_threshold_bounds():
    engine = DynamicThresholdingEngine()
    bounds = engine.calculate_adaptive_bounds([100.0, 100.0, 100.0])
    assert bounds["mean"] == 100.0
    assert bounds["upper_bound"] == 100.0

def test_dynamic_threshold_outlier():
    engine = DynamicThresholdingEngine()
    assert engine.is_outlier(150.0, 120.0, 80.0) is True
    assert engine.is_outlier(100.0, 120.0, 80.0) is False

def test_alert_broker_throttling():
    broker = RealTimeAlertingBroker()
    assert broker.should_throttle_alert("DEV-1", "overvoltage", 60, current_time=1000.0) is False
    assert broker.should_throttle_alert("DEV-1", "overvoltage", 60, current_time=1020.0) is True
    assert broker.should_throttle_alert("DEV-1", "overvoltage", 60, current_time=1070.0) is False

def test_alert_payload_formatting():
    broker = RealTimeAlertingBroker()
    payload = broker.format_alert_payload("DEV-1", "critical", "voltage", 260.0, 240.0)
    assert payload["device_id"] == "DEV-1"
    assert payload["severity"] == "critical"