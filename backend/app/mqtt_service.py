"""
PowerGuard IoT — MQTT Subscriber Service

Listens to MQTT topics for incoming sensor readings from ESP32
devices and writes them to InfluxDB.
"""

import json
import logging
import threading

import paho.mqtt.client as mqtt

from app.config import settings
from app.database import db

logger = logging.getLogger(__name__)

# In-memory store for the latest reading per channel (for /api/realtime)
latest_readings: dict[str, dict] = {}
# Lock for thread-safe access to latest_readings
readings_lock = threading.Lock()

# Device status tracking
device_status: dict[str, str] = {}


def on_connect(client, userdata, flags, rc):
    """Callback when MQTT client connects to the broker."""
    if rc == 0:
        logger.info("Connected to MQTT broker at %s:%d",
                     settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT)

        # Subscribe to all energy topics
        topic = f"{settings.MQTT_TOPIC_PREFIX}/#"
        client.subscribe(topic)
        logger.info("Subscribed to topic: %s", topic)
    else:
        logger.error("MQTT connection failed with code: %d", rc)


def on_message(client, userdata, msg):
    """Callback when a message is received on a subscribed topic."""
    topic = msg.topic
    payload = msg.payload.decode("utf-8")

    logger.debug("Received message on %s: %s", topic, payload[:100])

    try:
        # Parse topic structure: home/energy/{device_id}/{channel_or_status}
        parts = topic.split("/")
        if len(parts) < 4:
            logger.warning("Unexpected topic format: %s", topic)
            return

        device_id = parts[2]
        channel_or_status = parts[3]

        # Handle device status messages (online/offline)
        if channel_or_status == "status":
            device_status[device_id] = payload
            logger.info("Device %s is now %s", device_id, payload)
            return

        # Handle sensor reading messages
        channel = channel_or_status
        data = json.loads(payload)

        # Validate required fields
        required_fields = ["voltage_rms", "current_rms", "power_watts",
                          "apparent_power_va", "power_factor", "energy_kwh"]
        if not all(field in data for field in required_fields):
            logger.warning("Missing fields in payload from %s", topic)
            return

        # Ensure device_id and channel are set
        data["device_id"] = device_id
        data["channel"] = channel

        # Update in-memory latest readings (thread-safe)
        key = f"{device_id}/{channel}"
        with readings_lock:
            latest_readings[key] = data

        # Write to InfluxDB
        db.write_reading(data)

    except json.JSONDecodeError as e:
        logger.error("Invalid JSON payload on %s: %s", topic, e)
    except Exception as e:
        logger.error("Error processing message on %s: %s", topic, e)


def on_disconnect(client, userdata, rc):
    """Callback when MQTT client disconnects."""
    if rc != 0:
        logger.warning("Unexpected MQTT disconnect (rc=%d). Will auto-reconnect.", rc)
    else:
        logger.info("MQTT client disconnected gracefully.")


def get_latest_readings() -> dict[str, dict]:
    """Get the latest readings from in-memory cache (thread-safe)."""
    with readings_lock:
        return dict(latest_readings)


def get_device_status(device_id: str) -> str:
    """Get the current status of a device."""
    return device_status.get(device_id, "unknown")


class MQTTService:
    """MQTT subscriber service that runs in a background thread."""

    def __init__(self):
        self.client = mqtt.Client(client_id="powerguard_backend", protocol=mqtt.MQTTv311)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect
        self._thread: threading.Thread | None = None

    def start(self):
        """Start the MQTT subscriber in a background thread."""
        logger.info("Starting MQTT subscriber...")

        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                keepalive=60,
            )
            # Start network loop in background thread
            self.client.loop_start()
            logger.info("MQTT subscriber started.")
        except Exception as e:
            logger.error("Failed to start MQTT subscriber: %s", e)

    def stop(self):
        """Stop the MQTT subscriber."""
        logger.info("Stopping MQTT subscriber...")
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("MQTT subscriber stopped.")


# Singleton instance
mqtt_service = MQTTService()
