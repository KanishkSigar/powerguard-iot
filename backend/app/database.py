"""
PowerGuard IoT — InfluxDB Database Service

Handles all database operations: writing sensor readings,
querying historical data, and aggregating usage statistics.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.config import settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for InfluxDB read/write operations."""

    def __init__(self):
        self.client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG,
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.bucket = settings.INFLUXDB_BUCKET
        self.org = settings.INFLUXDB_ORG
        logger.info("InfluxDB client initialized (url=%s, bucket=%s)", settings.INFLUXDB_URL, self.bucket)

    def close(self):
        """Close the InfluxDB client connection."""
        self.client.close()
        logger.info("InfluxDB client closed.")

    # ==========================
    # Write Operations
    # ==========================

    def write_reading(self, data: dict):
        """
        Write a sensor reading to InfluxDB.

        Args:
            data: Dict with keys: device_id, channel, voltage_rms, current_rms,
                  power_watts, apparent_power_va, power_factor, energy_kwh
        """
        try:
            point = (
                Point("energy_readings")
                .tag("device_id", data["device_id"])
                .tag("channel", data["channel"])
                .field("voltage", float(data["voltage_rms"]))
                .field("current", float(data["current_rms"]))
                .field("power", float(data["power_watts"]))
                .field("apparent_power", float(data["apparent_power_va"]))
                .field("power_factor", float(data["power_factor"]))
                .field("energy_kwh", float(data["energy_kwh"]))
                .time(datetime.utcnow(), WritePrecision.S)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            logger.debug("Written reading: device=%s channel=%s power=%.1fW",
                         data["device_id"], data["channel"], data["power_watts"])
        except Exception as e:
            logger.error("Failed to write reading: %s", e)

    def write_anomaly(self, anomaly: dict):
        """
        Write an anomaly detection event to InfluxDB.

        Args:
            anomaly: Dict with keys: device_id, channel, type, severity,
                     description, power_at_detection, anomaly_score
        """
        try:
            point = (
                Point("anomalies")
                .tag("device_id", anomaly["device_id"])
                .tag("channel", anomaly["channel"])
                .tag("severity", anomaly["severity"])
                .field("type", anomaly["type"])
                .field("description", anomaly["description"])
                .field("power_at_detection", float(anomaly["power_at_detection"]))
                .field("anomaly_score", float(anomaly["anomaly_score"]))
                .time(datetime.utcnow(), WritePrecision.S)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            logger.info("Written anomaly: %s on %s/%s",
                        anomaly["type"], anomaly["device_id"], anomaly["channel"])
        except Exception as e:
            logger.error("Failed to write anomaly: %s", e)

    # ==========================
    # Query Operations
    # ==========================

    def get_latest_readings(self, device_id: Optional[str] = None) -> list[dict]:
        """Get the most recent reading for each channel."""
        device_filter = ""
        if device_id:
            device_filter = f'|> filter(fn: (r) => r["device_id"] == "{device_id}")'

        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -5m)
          {device_filter}
          |> filter(fn: (r) => r["_measurement"] == "energy_readings")
          |> last()
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        try:
            tables = self.query_api.query(query, org=self.org)
            results = []
            for table in tables:
                for record in table.records:
                    results.append({
                        "device_id": record.values.get("device_id", ""),
                        "channel": record.values.get("channel", ""),
                        "timestamp": record.get_time().isoformat(),
                        "voltage_rms": record.values.get("voltage", 0),
                        "current_rms": record.values.get("current", 0),
                        "power_watts": record.values.get("power", 0),
                        "apparent_power_va": record.values.get("apparent_power", 0),
                        "power_factor": record.values.get("power_factor", 0),
                        "energy_kwh": record.values.get("energy_kwh", 0),
                    })
            return results
        except Exception as e:
            logger.error("Failed to query latest readings: %s", e)
            return []

    def get_history(self, channel: str = "main", start: str = "-24h",
                    stop: str = "now()", device_id: Optional[str] = None) -> list[dict]:
        """Get historical readings for a channel within a time range."""
        device_filter = ""
        if device_id:
            device_filter = f'|> filter(fn: (r) => r["device_id"] == "{device_id}")'

        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: {start}, stop: {stop})
          {device_filter}
          |> filter(fn: (r) => r["_measurement"] == "energy_readings")
          |> filter(fn: (r) => r["channel"] == "{channel}")
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> sort(columns: ["_time"])
        '''
        try:
            tables = self.query_api.query(query, org=self.org)
            results = []
            for table in tables:
                for record in table.records:
                    results.append({
                        "timestamp": record.get_time().isoformat(),
                        "voltage": record.values.get("voltage", 0),
                        "current": record.values.get("current", 0),
                        "power": record.values.get("power", 0),
                        "apparent_power": record.values.get("apparent_power", 0),
                        "power_factor": record.values.get("power_factor", 0),
                        "energy_kwh": record.values.get("energy_kwh", 0),
                    })
            return results
        except Exception as e:
            logger.error("Failed to query history: %s", e)
            return []

    def get_daily_usage(self, channel: str = "main", days: int = 30,
                        device_id: Optional[str] = None) -> list[dict]:
        """Get daily energy consumption summary."""
        device_filter = ""
        if device_id:
            device_filter = f'|> filter(fn: (r) => r["device_id"] == "{device_id}")'

        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -{days}d)
          {device_filter}
          |> filter(fn: (r) => r["_measurement"] == "energy_readings")
          |> filter(fn: (r) => r["channel"] == "{channel}")
          |> filter(fn: (r) => r["_field"] == "power")
          |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
          |> yield(name: "daily_avg")
        '''
        try:
            tables = self.query_api.query(query, org=self.org)
            results = []
            for table in tables:
                for record in table.records:
                    avg_power = record.get_value() or 0
                    # Estimate daily kWh: avg_power * 24h / 1000
                    daily_kwh = avg_power * 24 / 1000
                    results.append({
                        "date": record.get_time().strftime("%Y-%m-%d"),
                        "channel": channel,
                        "avg_power_watts": round(avg_power, 1),
                        "total_kwh": round(daily_kwh, 3),
                        "cost_inr": round(daily_kwh * settings.TARIFF_RATE, 2),
                    })
            return results
        except Exception as e:
            logger.error("Failed to query daily usage: %s", e)
            return []

    def get_anomalies(self, hours: int = 24, device_id: Optional[str] = None) -> list[dict]:
        """Get detected anomalies within a time range."""
        device_filter = ""
        if device_id:
            device_filter = f'|> filter(fn: (r) => r["device_id"] == "{device_id}")'

        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: -{hours}h)
          {device_filter}
          |> filter(fn: (r) => r["_measurement"] == "anomalies")
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> sort(columns: ["_time"], desc: true)
        '''
        try:
            tables = self.query_api.query(query, org=self.org)
            results = []
            for table in tables:
                for record in table.records:
                    results.append({
                        "device_id": record.values.get("device_id", ""),
                        "channel": record.values.get("channel", ""),
                        "severity": record.values.get("severity", ""),
                        "timestamp": record.get_time().isoformat(),
                        "type": record.values.get("type", ""),
                        "description": record.values.get("description", ""),
                        "power_at_detection": record.values.get("power_at_detection", 0),
                        "anomaly_score": record.values.get("anomaly_score", 0),
                    })
            return results
        except Exception as e:
            logger.error("Failed to query anomalies: %s", e)
            return []


# Singleton instance
db = DatabaseService()
