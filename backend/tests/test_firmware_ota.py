"""PowerGuard IoT — Firmware OTA Update Tests"""
import hashlib
import pytest

def compute_binary_checksum(binary_data: bytes) -> str:
    return hashlib.sha256(binary_data).hexdigest()

def is_firmware_upgrade_allowed(current_ver: str, candidate_ver: str) -> bool:
    cur_parts = tuple(map(int, current_ver.split(".")))
    cand_parts = tuple(map(int, candidate_ver.split(".")))
    return cand_parts > cur_parts

def test_binary_checksum():
    dummy_payload = b"\xAA\xBB\xCC\xDD" * 256
    chk = compute_binary_checksum(dummy_payload)
    assert len(chk) == 64
    assert chk == hashlib.sha256(dummy_payload).hexdigest()

def test_firmware_upgrade_eligibility():
    assert is_firmware_upgrade_allowed("2.4.0", "2.4.1") is True
    assert is_firmware_upgrade_allowed("2.4.0", "3.0.0") is True
    assert is_firmware_upgrade_allowed("2.4.1", "2.4.1") is False
    assert is_firmware_upgrade_allowed("2.5.0", "2.4.9") is False