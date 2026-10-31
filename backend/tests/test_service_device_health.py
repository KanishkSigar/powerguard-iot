"""PowerGuard IoT — Device Health & Firmware Rollback Tests"""
import pytest
from app.services.DeviceHealthMonitor import DeviceHealthMonitor
from app.services.FirmwareRollbackManager import FirmwareRollbackManager

def test_device_health_evaluation():
    monitor = DeviceHealthMonitor()
    health = monitor.evaluate_health(10.0, -50, 60000)
    assert health["status"] == "healthy"
    assert health["is_critical"] is False

def test_device_offline_detection():
    monitor = DeviceHealthMonitor()
    assert monitor.is_device_offline(150.0, 120.0) is True
    assert monitor.is_device_offline(30.0, 120.0) is False

def test_firmware_canary_verification():
    manager = FirmwareRollbackManager()
    assert manager.canary_verification_passed(2, 0) is True
    assert manager.canary_verification_passed(5, 3) is False

def test_firmware_rollback_instruction():
    manager = FirmwareRollbackManager()
    instr = manager.create_rollback_instruction("DEV-ESP-99", "2.4.1", "2.4.0")
    assert instr["device_id"] == "DEV-ESP-99"
    assert instr["action"] == "ota_rollback"