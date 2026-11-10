"""PowerGuard IoT — User Preferences Model Tests"""
import pytest

def convert_energy_units(kwh: float, target_unit: str) -> float:
    if target_unit == "MWh": return round(kwh / 1000.0, 4)
    elif target_unit == "GWh": return round(kwh / 1000000.0, 6)
    return round(kwh, 2)

def test_kwh_to_mwh():
    assert convert_energy_units(2500.0, "MWh") == 2.5
    assert convert_energy_units(100.0, "kWh") == 100.0