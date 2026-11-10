"""PowerGuard IoT — Data Cleanup & Purge Tests"""
import time, pytest

def identify_purge_candidates(records: list, max_age_seconds: float, current_time: float = None) -> list:
    now = current_time if current_time is not None else time.time()
    cutoff = now - max_age_seconds
    return [r for r in records if r.get("timestamp_s", 0) < cutoff]

def test_purge_candidates():
    now = 10000.0
    records = [
        {"id": "R1", "timestamp_s": 1000.0},
        {"id": "R2", "timestamp_s": 8500.0},
        {"id": "R3", "timestamp_s": 9800.0},
    ]
    purged = identify_purge_candidates(records, max_age_seconds=2000.0, current_time=now)
    assert len(purged) == 1
    assert purged[0]["id"] == "R1"