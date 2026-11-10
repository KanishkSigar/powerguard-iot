"""PowerGuard IoT — Input Data Validation Tests"""
import pytest

def validate_telemetry_reading(voltage: float, current: float, power_factor: float) -> dict:
    errors = []
    if not (0.0 <= voltage <= 500.0): errors.append(f"Voltage out of range: {voltage}")
    if not (0.0 <= current <= 200.0): errors.append(f"Current out of range: {current}")
    if not (-1.0 <= power_factor <= 1.0): errors.append(f"Power factor out of range: {power_factor}")
    return {"valid": len(errors) == 0, "errors": errors}

def test_valid_telemetry():
    res = validate_telemetry_reading(230.0, 15.0, 0.95)
    assert res["valid"] is True
    assert len(res["errors"]) == 0

def test_invalid_telemetry_out_of_bounds():
    res = validate_telemetry_reading(-10.0, 250.0, 1.5)
    assert res["valid"] is False
    assert len(res["errors"]) == 3