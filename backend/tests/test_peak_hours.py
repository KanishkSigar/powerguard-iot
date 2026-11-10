"""PowerGuard IoT — Peak Hours & Time-of-Use Calculation Tests"""
from datetime import datetime, time
import pytest

def is_peak_hour(dt: datetime, peak_windows: list = None) -> bool:
    windows = peak_windows or [(time(18, 0), time(22, 0))]
    if dt.weekday() >= 5: return False
    t = dt.time()
    return any(start <= t <= end for start, end in windows)

def get_tariff_multiplier(dt: datetime) -> float:
    return 1.5 if is_peak_hour(dt) else (0.8 if dt.hour < 6 else 1.0)

def test_peak_hour_weekday_evening():
    dt = datetime(2026, 11, 10, 19, 30) # Tuesday 19:30
    assert is_peak_hour(dt) is True
    assert get_tariff_multiplier(dt) == 1.5

def test_offpeak_hour_weekend():
    dt = datetime(2026, 11, 15, 19, 30) # Sunday 19:30
    assert is_peak_hour(dt) is False