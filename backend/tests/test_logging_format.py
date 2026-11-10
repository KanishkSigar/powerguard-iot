"""PowerGuard IoT — Structured Log Formatter Tests"""
import json
import pytest

def format_structured_log(level: str, message: str, context: dict = None) -> str:
    ctx = (context or {}).copy()
    for sensitive_key in ["password", "token", "secret", "api_key"]:
        if sensitive_key in ctx: ctx[sensitive_key] = "******"
    entry = {"level": level.upper(), "message": message, "context": ctx}
    return json.dumps(entry)

def test_structured_log_json():
    log_str = format_structured_log("info", "Service started", {"port": 8000})
    data = json.loads(log_str)
    assert data["level"] == "INFO"
    assert data["message"] == "Service started"
    assert data["context"]["port"] == 8000

def test_sensitive_field_masking():
    log_str = format_structured_log("warn", "Auth failed", {"username": "admin", "token": "secret_token_123"})
    data = json.loads(log_str)
    assert data["context"]["token"] == "******"