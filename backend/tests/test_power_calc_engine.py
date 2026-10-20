"""
PowerGuard IoT — Power Calculation Engine Tests
Validates electrical formulas: active, reactive, apparent power, power factor, and energy accumulation.
"""

import math
import pytest


def calculate_active_power(voltage_rms: float, current_rms: float, power_factor: float) -> float:
    """Calculates active real power (P in Watts)."""
    if voltage_rms < 0 or current_rms < 0:
        raise ValueError("Voltage and Current RMS must be non-negative")
    return round(voltage_rms * current_rms * power_factor, 2)


def calculate_apparent_power(voltage_rms: float, current_rms: float) -> float:
    """Calculates apparent power (S in VA)."""
    if voltage_rms < 0 or current_rms < 0:
        raise ValueError("Voltage and Current RMS must be non-negative")
    return round(voltage_rms * current_rms, 2)


def calculate_reactive_power(apparent_power_va: float, active_power_w: float) -> float:
    """Calculates reactive power (Q in VAR)."""
    diff = max(0.0, apparent_power_va**2 - active_power_w**2)
    return round(math.sqrt(diff), 2)


def calculate_power_factor(active_power_w: float, apparent_power_va: float) -> float:
    """Calculates power factor ratio (dimensionless, between 0.0 and 1.0)."""
    if apparent_power_va <= 0:
        return 1.0
    pf = active_power_w / apparent_power_va
    return round(min(1.0, max(-1.0, pf)), 4)


def calculate_energy_kwh(power_watts: float, duration_seconds: float) -> float:
    """Calculates cumulative energy consumed in kilowatt-hours (kWh)."""
    if power_watts < 0 or duration_seconds < 0:
        raise ValueError("Power and duration must be non-negative")
    return round((power_watts * duration_seconds) / (3600.0 * 1000.0), 6)


def calculate_crest_factor(peak_current: float, rms_current: float) -> float:
    """Calculates crest factor (ratio of peak to RMS value)."""
    if rms_current <= 0:
        return 0.0
    return round(peak_current / rms_current, 3)


def test_active_power():
    assert calculate_active_power(230.0, 10.0, 0.95) == 2185.0


def test_apparent_power():
    assert calculate_apparent_power(230.0, 10.0) == 2300.0


def test_reactive_power():
    q = calculate_reactive_power(2300.0, 2185.0)
    assert 718.0 <= q <= 720.0


def test_power_factor():
    assert calculate_power_factor(2185.0, 2300.0) == 0.95
    assert calculate_power_factor(0.0, 0.0) == 1.0


def test_energy_accumulation():
    assert calculate_energy_kwh(1000.0, 3600.0) == 1.0
    assert calculate_energy_kwh(2000.0, 1800.0) == 1.0


def test_crest_factor():
    assert calculate_crest_factor(14.14, 10.0) == 1.414