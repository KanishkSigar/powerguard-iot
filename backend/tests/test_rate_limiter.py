"""
PowerGuard IoT — Rate Limiter Unit Tests
Validates sliding-window request throttling and client quotas.
"""
from collections import defaultdict
import time
import pytest


class SlidingWindowRateLimiter:
    """In-memory rate limiter using sliding timestamp window."""

    def __init__(self, max_requests: int = 10, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history = defaultdict(list)

    def is_allowed(self, client_id: str, current_time: float = None) -> bool:
        now = current_time if current_time is not None else time.time()
        timestamps = self._history[client_id]
        cutoff = now - self.window_seconds
        # Remove expired timestamps
        valid = [t for t in timestamps if t > cutoff]
        self._history[client_id] = valid

        if len(valid) < self.max_requests:
            self._history[client_id].append(now)
            return True
        return False


def test_rate_limiter_allow():
    limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=60.0)
    for i in range(5):
        assert limiter.is_allowed("client_a", current_time=100.0 + i) is True


def test_rate_limiter_block_excess():
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=60.0)
    assert limiter.is_allowed("client_b", current_time=100.0) is True
    assert limiter.is_allowed("client_b", current_time=101.0) is True
    assert limiter.is_allowed("client_b", current_time=102.0) is True
    assert limiter.is_allowed("client_b", current_time=103.0) is False


def test_rate_limiter_window_slide():
    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=10.0)
    assert limiter.is_allowed("client_c", current_time=10.0) is True
    assert limiter.is_allowed("client_c", current_time=15.0) is True
    assert limiter.is_allowed("client_c", current_time=18.0) is False
    # After window passes
    assert limiter.is_allowed("client_c", current_time=22.0) is True


def test_rate_limiter_multiple_clients():
    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=60.0)
    assert limiter.is_allowed("client_1", current_time=10.0) is True
    assert limiter.is_allowed("client_1", current_time=11.0) is True
    assert limiter.is_allowed("client_1", current_time=12.0) is False
    # client_2 has independent quota
    assert limiter.is_allowed("client_2", current_time=12.0) is True