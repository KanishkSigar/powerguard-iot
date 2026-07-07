"""
PowerGuard IoT — Backend Configuration

Loads environment variables and provides typed settings
for all backend services.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # MQTT
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_TOPIC_PREFIX: str = os.getenv("MQTT_TOPIC_PREFIX", "home/energy")

    # InfluxDB
    INFLUXDB_URL: str = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    INFLUXDB_TOKEN: str = os.getenv("INFLUXDB_TOKEN", "my-super-secret-token")
    INFLUXDB_ORG: str = os.getenv("INFLUXDB_ORG", "powerguard")
    INFLUXDB_BUCKET: str = os.getenv("INFLUXDB_BUCKET", "energy_data")
    INFLUXDB_RETENTION_DAYS: int = int(os.getenv("INFLUXDB_RETENTION_DAYS", "30"))

    # Tariff
    TARIFF_RATE: float = float(os.getenv("TARIFF_RATE", "6.50"))

    # Anomaly Detection
    ANOMALY_POWER_THRESHOLD: float = float(os.getenv("ANOMALY_POWER_THRESHOLD", "2000"))
    ANOMALY_LEFT_ON_SECONDS: int = int(os.getenv("ANOMALY_LEFT_ON_SECONDS", "7200"))

    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # Email
    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_RECIPIENT: str = os.getenv("EMAIL_RECIPIENT", "")

    # Server
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")


settings = Settings()
