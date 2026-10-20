"""
PowerGuard IoT — Domain Models Unit Test Suite
Verifies validation, field serialization, and instantiation of domain models.
"""

from datetime import datetime
import pytest
from app.models.Device import Device
from app.models.SensorChannel import SensorChannel
from app.models.EnergyReading import EnergyReading
from app.models.PowerQualityMetric import PowerQualityMetric
from app.models.TariffPlan import TariffPlan, TimeOfUseSlot
from app.models.EnergyAlert import EnergyAlert
from app.models.AnomalyRecord import AnomalyRecord
from app.models.LoadSchedule import LoadSchedule
from app.models.CarbonEmissionFactor import CarbonEmissionFactor
from app.models.FirmwareRelease import FirmwareRelease
from app.models.AuditLog import AuditLog
from app.models.ExportJob import ExportJob


def test_device_model_valid():
    device = Device(
        device_id="DEV-ESP32-101",
        name="Main Workshop Panel",
        mac_address="24:6F:28:B2:3C:44",
        ip_address="192.168.1.150",
    )
    assert device.device_id == "DEV-ESP32-101"
    assert device.status == "online"
    assert device.total_channels == 3
    assert device.sampling_interval_ms == 1000


def test_sensor_channel_model():
    channel = SensorChannel(
        channel_id="ch_main_phase_a",
        device_id="DEV-ESP32-101",
        channel_number=1,
        channel_name="Phase A Incoming",
        phase_type="phase_a",
        ct_rating_amps=100.0,
    )
    assert channel.channel_number == 1
    assert channel.is_active is True
    assert channel.calibration_multiplier == 1.0


def test_energy_reading_model():
    reading = EnergyReading(
        device_id="DEV-ESP32-101",
        channel_id="ch_main_phase_a",
        voltage_rms=230.5,
        current_rms=12.4,
        active_power_w=2800.0,
        apparent_power_va=2858.2,
        power_factor=0.98,
    )
    assert reading.voltage_rms == 230.5
    assert reading.power_factor == 0.98
    assert reading.grid_frequency_hz == 50.0


def test_power_quality_metric_model():
    metric = PowerQualityMetric(
        device_id="DEV-ESP32-101",
        thd_voltage_percent=2.1,
        thd_current_percent=4.8,
        power_quality_grade="A",
    )
    assert metric.thd_voltage_percent == 2.1
    assert metric.power_quality_grade == "A"


def test_tariff_plan_model():
    slot = TimeOfUseSlot(
        slot_name="Peak Hours",
        start_time="18:00",
        end_time="22:00",
        rate_per_kwh=9.50,
    )
    plan = TariffPlan(
        tariff_id="TARIFF-2026-COMM",
        provider_name="State Electricity Board",
        plan_name="Commercial Time-of-Day",
        currency="INR",
        tou_slots=[slot],
    )
    assert plan.currency == "INR"
    assert len(plan.tou_slots) == 1
    assert plan.tou_slots[0].rate_per_kwh == 9.50


def test_energy_alert_model():
    alert = EnergyAlert(
        alert_id="ALT-9041",
        device_id="DEV-ESP32-101",
        alert_type="overcurrent",
        severity="critical",
        trigger_value=112.5,
        threshold_value=100.0,
        message="Current threshold exceeded on Main Phase A",
    )
    assert alert.severity == "critical"
    assert alert.is_acknowledged is False


def test_anomaly_record_model():
    anomaly = AnomalyRecord(
        record_id="ANOM-301",
        device_id="DEV-ESP32-101",
        anomaly_score=0.92,
        classification="abnormal_spike",
    )
    assert anomaly.anomaly_score == 0.92
    assert anomaly.is_false_positive is False


def test_load_schedule_model():
    schedule = LoadSchedule(
        schedule_id="SCHED-01",
        device_id="DEV-ESP32-101",
        relay_pin=18,
        load_name="HVAC Chiller",
        start_time="08:00",
        duration_minutes=480,
    )
    assert schedule.relay_pin == 18
    assert schedule.is_enabled is True


def test_carbon_emission_factor_model():
    factor = CarbonEmissionFactor(
        region_code="IN-NR",
        emission_factor_gco2_per_kwh=680.0,
        renewable_share_percent=24.5,
    )
    assert factor.emission_factor_gco2_per_kwh == 680.0


def test_firmware_release_model():
    firmware = FirmwareRelease(
        release_id="FW-REL-2.4.1",
        version="2.4.1",
        binary_size_bytes=1048576,
        sha256_checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        download_url="https://firmware.powerguard.iot/bin/v2.4.1.bin",
    )
    assert firmware.version == "2.4.1"
    assert firmware.release_channel == "stable"


def test_audit_log_model():
    log = AuditLog(
        event_id="EVT-1002",
        action="device.reboot",
        resource_type="Device",
        resource_id="DEV-ESP32-101",
    )
    assert log.action == "device.reboot"
    assert log.status == "success"


def test_export_job_model():
    job = ExportJob(
        job_id="JOB-4819",
        requested_by="operator_admin",
        date_start=datetime(2026, 10, 1),
        date_end=datetime(2026, 10, 20),
    )
    assert job.job_id == "JOB-4819"
    assert job.status == "pending"