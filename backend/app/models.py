"""
PowerGuard IoT — Data Models

Pydantic models for request/response validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==============================
# Sensor Reading Models
# ==============================

class EnergyReading(BaseModel):
    """A single energy reading from a sensor channel."""
    device_id: str = Field(..., description="Unique device identifier")
    channel: str = Field(..., description="Sensor channel name (main, channel1, channel2)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC timestamp")
    voltage_rms: float = Field(..., ge=0, description="RMS voltage in volts")
    current_rms: float = Field(..., ge=0, description="RMS current in amps")
    power_watts: float = Field(..., description="Real power in watts")
    apparent_power_va: float = Field(..., ge=0, description="Apparent power in volt-amps")
    power_factor: float = Field(..., ge=-1, le=1, description="Power factor (-1 to 1)")
    energy_kwh: float = Field(..., ge=0, description="Cumulative energy in kWh")


class RealtimeResponse(BaseModel):
    """Response for /api/realtime — latest readings from all channels."""
    device_id: str
    channels: dict[str, EnergyReading]
    last_updated: datetime


# ==============================
# Usage / Analytics Models
# ==============================

class DailyUsage(BaseModel):
    """Daily energy consumption summary."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    channel: str
    total_kwh: float = Field(..., ge=0)
    avg_power_watts: float = Field(..., ge=0)
    max_power_watts: float = Field(..., ge=0)
    min_power_watts: float = Field(..., ge=0)
    cost_inr: float = Field(..., ge=0, description="Estimated cost in INR")


class MonthlyUsage(BaseModel):
    """Monthly energy consumption summary."""
    month: str = Field(..., description="Month in YYYY-MM format")
    channel: str
    total_kwh: float = Field(..., ge=0)
    avg_daily_kwh: float = Field(..., ge=0)
    peak_day: str = Field(..., description="Day with highest consumption")
    peak_day_kwh: float = Field(..., ge=0)
    cost_inr: float = Field(..., ge=0)


class PeakHoursResponse(BaseModel):
    """Peak usage hours analysis."""
    channel: str
    peak_hours: list[dict] = Field(..., description="List of {hour, avg_power_watts}")
    off_peak_hours: list[dict]


# ==============================
# Anomaly Models
# ==============================

class Anomaly(BaseModel):
    """A detected anomaly event."""
    id: Optional[str] = None
    device_id: str
    channel: str
    timestamp: datetime
    type: str = Field(..., description="Anomaly type: threshold_breach, unusual_time, left_on, pattern_anomaly")
    severity: str = Field(..., description="Severity: low, medium, high, critical")
    description: str
    power_at_detection: float
    anomaly_score: float = Field(..., description="ML anomaly score (-1 = anomaly, 1 = normal)")
    acknowledged: bool = Field(default=False)


# ==============================
# Settings Models
# ==============================

class ThresholdSettings(BaseModel):
    """Alert threshold configuration."""
    power_threshold_watts: float = Field(2000, ge=0, description="Power threshold for alerts")
    left_on_seconds: int = Field(7200, ge=0, description="Seconds before 'left on' alert")
    tariff_rate_inr: float = Field(6.50, ge=0, description="Electricity rate in INR/kWh")


# ==============================
# Device Models
# ==============================

class DeviceInfo(BaseModel):
    """Registered device information."""
    device_id: str
    channels: list[str]
    status: str = Field(..., description="online or offline")
    last_seen: Optional[datetime] = None
