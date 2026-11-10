"""PowerGuard IoT — Role & Permission Enforcement Tests"""
import fnmatch, pytest

def has_permission(user_permissions: list, required_permission: str) -> bool:
    for perm in user_permissions:
        if fnmatch.fnmatch(required_permission, perm):
            return True
    return False

def test_exact_permission():
    perms = ["devices.read", "readings.read"]
    assert has_permission(perms, "devices.read") is True
    assert has_permission(perms, "devices.write") is False

def test_wildcard_permission():
    perms = ["devices.*", "readings.read"]
    assert has_permission(perms, "devices.reboot") is True
    assert has_permission(perms, "tariffs.update") is False