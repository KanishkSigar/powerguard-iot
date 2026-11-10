"""PowerGuard IoT — System Diagnostic Info Tests"""
import platform, sys, os, pytest

def get_runtime_environment_info() -> dict:
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.system(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count() or 1,
    }

def test_runtime_environment_info():
    info = get_runtime_environment_info()
    assert len(info["python_version"]) > 0
    assert info["platform"] in ["Windows", "Linux", "Darwin"]
    assert info["cpu_count"] >= 1