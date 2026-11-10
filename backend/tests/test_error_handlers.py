"""PowerGuard IoT — API Error Handling Tests"""
import pytest

def build_error_response(error_code: str, message: str, status_code: int = 400, details: dict = None) -> dict:
    return {
        "status_code": status_code,
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {},
        }
    }

def test_error_response_structure():
    err = build_error_response("ERR_DEVICE_OFFLINE", "Device DEV-1 is unreachable", status_code=503)
    assert err["status_code"] == 503
    assert err["error"]["code"] == "ERR_DEVICE_OFFLINE"
    assert "DEV-1" in err["error"]["message"]