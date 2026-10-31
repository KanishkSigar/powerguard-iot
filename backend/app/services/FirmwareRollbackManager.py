"""
PowerGuard IoT — Firmware Rollback Manager
Monitors OTA boot stability and orchestrates fail-safe rollback to previous stable partitions.
"""
from typing import Dict, Any

class FirmwareRollbackManager:
    def __init__(self):
        self.max_allowed_crashes: int = 3

    def canary_verification_passed(self, boot_count: int, crash_count: int) -> bool:
        if crash_count >= self.max_allowed_crashes: return False
        return boot_count >= 1

    def create_rollback_instruction(self, device_id: str, current_version: str, previous_version: str) -> Dict[str, Any]:
        return {
            "device_id": device_id,
            "action": "ota_rollback",
            "target_partition": "ota_0",
            "from_version": current_version,
            "to_version": previous_version,
            "reboot_delay_ms": 2000,
            "force": True,
        }