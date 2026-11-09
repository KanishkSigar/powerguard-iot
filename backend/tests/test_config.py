"""
PowerGuard IoT — Backend Configuration Tests
Validates Settings class environment variable parsing, default fallbacks, and typed conversion.
"""
import pytest
from app.config import Settings, settings


def test_default_settings():
    assert settings.MQTT_BROKER_PORT == 1883
    assert settings.TARIFF_RATE == 6.50
    assert settings.INFLUXDB_BUCKET == "energy_data"
    assert settings.API_PORT == 8000
    assert settings.INFLUXDB_RETENTION_DAYS == 30


def test_anomaly_threshold_settings():
    assert settings.ANOMALY_POWER_THRESHOLD == 2000.0
    assert settings.ANOMALY_LEFT_ON_SECONDS == 7200


def test_cors_origins_format():
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) >= 1


def test_email_and_telegram_defaults():
    assert isinstance(settings.EMAIL_SMTP_HOST, str)
    assert settings.EMAIL_SMTP_PORT == 587
    assert isinstance(settings.TELEGRAM_BOT_TOKEN, str)