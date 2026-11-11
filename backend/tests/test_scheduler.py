"""PowerGuard IoT — Automation Task Scheduler Tests"""
from datetime import datetime, timedelta
import pytest

def calculate_next_run(last_run: datetime, interval_minutes: int) -> datetime:
    if interval_minutes <= 0:
        raise ValueError("Interval must be positive")
    return last_run + timedelta(minutes=interval_minutes)

def is_job_due(next_run: datetime, current_time: datetime) -> bool:
    return current_time >= next_run

def test_scheduler_next_run():
    now = datetime(2026, 11, 11, 10, 0, 0)
    next_time = calculate_next_run(now, interval_minutes=15)
    assert next_time == datetime(2026, 11, 11, 10, 15, 0)
    with pytest.raises(ValueError):
        calculate_next_run(now, interval_minutes=0)

def test_scheduler_job_due():
    scheduled = datetime(2026, 11, 11, 10, 15, 0)
    assert is_job_due(scheduled, datetime(2026, 11, 11, 10, 14, 59)) is False
    assert is_job_due(scheduled, datetime(2026, 11, 11, 10, 15, 0)) is True
    assert is_job_due(scheduled, datetime(2026, 11, 11, 10, 16, 0)) is True