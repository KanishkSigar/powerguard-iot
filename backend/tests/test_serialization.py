"""
PowerGuard IoT — Model Serialization Unit Tests
Validates JSON schema dumps, datetime serialization, and roundtrip deserialization.
"""
import json
from datetime import datetime, timezone
import pytest
from app.models.Device import Device
from app.models.EnergyReading import EnergyReading
from app.models.TariffPlan import TariffPlan, TimeOfUseSlot


def test_device_json_serialization():
    dev = Device(
        device_id="ESP32-NODE-01",
        name="Main Feeder",
        mac_address="24:0A:C4:00:11:22",
        status="online",
    )
    data = dev.model_dump()
    assert data["device_id"] == "ESP32-NODE-01"
    assert data["total_channels"] == 3
    
    json_str = dev.model_dump_json()
    parsed = json.loads(json_str)
    assert parsed["mac_address"] == "24:0A:C4:00:11:22"


def test_energy_reading_roundtrip():
    now = datetime(2026, 11, 9, 12, 0, 0, tzinfo=timezone.utc)
    reading = EnergyReading(
        device_id="ESP32-NODE-01",
        channel_id="phase_a",
        timestamp=now,
        voltage_rms=230.2,
        current_rms=14.5,
        active_power_w=3300.0,
        apparent_power_va=3337.9,
        power_factor=0.99,
    )
    raw_json = reading.model_dump_json()
    reconstructed = EnergyReading.model_validate_json(raw_json)
    assert reconstructed.device_id == reading.device_id
    assert reconstructed.voltage_rms == 230.2
    assert reconstructed.active_power_w == 3300.0


def test_nested_tariff_serialization():
    slot = TimeOfUseSlot(slot_name="Peak", start_time="18:00", end_time="22:00", rate_per_kwh=10.5)
    plan = TariffPlan(
        tariff_id="TARIFF-2026",
        provider_name="National Grid",
        plan_name="Industrial ToU",
        tou_slots=[slot],
    )
    dumped = plan.model_dump()
    assert len(dumped["tou_slots"]) == 1
    assert dumped["tou_slots"][0]["rate_per_kwh"] == 10.5