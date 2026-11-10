"""PowerGuard IoT — User Session Lifecycle Tests"""
import time, pytest

class SessionHandler:
    def __init__(self, idle_timeout: float = 1800.0):
        self.idle_timeout = idle_timeout
        self.sessions = {}

    def create_session(self, user_id: str, session_id: str, current_time: float = None):
        now = current_time if current_time is not None else time.time()
        self.sessions[session_id] = {"user_id": user_id, "last_active": now}

    def is_session_active(self, session_id: str, current_time: float = None) -> bool:
        if session_id not in self.sessions: return False
        now = current_time if current_time is not None else time.time()
        active = (now - self.sessions[session_id]["last_active"]) <= self.idle_timeout
        if not active: del self.sessions[session_id]
        return active

def test_session_active_and_expiry():
    handler = SessionHandler(idle_timeout=600.0)
    handler.create_session("usr_1", "ses_1", current_time=1000.0)
    assert handler.is_session_active("ses_1", current_time=1200.0) is True
    assert handler.is_session_active("ses_1", current_time=1700.0) is False