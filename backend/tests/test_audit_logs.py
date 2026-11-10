"""PowerGuard IoT — Security Audit Log Tracking Tests"""
import hashlib, json, pytest

def create_audit_entry(action: str, actor: str, resource_id: str, diff: dict) -> dict:
    entry = {
        "action": action,
        "actor": actor,
        "resource_id": resource_id,
        "diff": diff,
        "timestamp": 1794268800.0,
    }
    checksum = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    entry["checksum"] = checksum
    return entry

def test_audit_entry_creation():
    entry = create_audit_entry("threshold.update", "admin", "RULE-01", {"old": 2000, "new": 2500})
    assert entry["action"] == "threshold.update"
    assert "checksum" in entry
    assert len(entry["checksum"]) == 64