"""PowerGuard IoT — Cache Manager Unit Tests"""
import time, pytest

class SimpleTTLCache:
    def __init__(self, default_ttl: float = 60.0):
        self.default_ttl = default_ttl
        self._store = {}

    def set(self, key: str, value, ttl: float = None, current_time: float = None):
        now = current_time if current_time is not None else time.time()
        expiry = now + (ttl if ttl is not None else self.default_ttl)
        self._store[key] = (value, expiry)

    def get(self, key: str, current_time: float = None):
        if key not in self._store: return None
        val, expiry = self._store[key]
        now = current_time if current_time is not None else time.time()
        if now > expiry:
            del self._store[key]
            return None
        return val

def test_cache_hit_and_miss():
    cache = SimpleTTLCache()
    cache.set("k1", "v1")
    assert cache.get("k1") == "v1"
    assert cache.get("nonexistent") is None

def test_cache_expiration():
    cache = SimpleTTLCache()
    cache.set("temp", "val", ttl=5.0, current_time=100.0)
    assert cache.get("temp", current_time=100.0) == "val"
    assert cache.get("temp", current_time=106.0) is None