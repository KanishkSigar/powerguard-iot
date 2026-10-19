"""
PowerGuard IoT — Energy Reading Telemetry Model
High-resolution AC power electrical telemetry measurement packet.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EnergyReading(BaseModel):
    """High-resolution energy measurement data point from an IoT sensor channel."""
    reading_id: Optional[str] = Field(None, description="Unique telemetry packet identifier")
    device_id: str = Field(..., description="Originating IoT device identifier")
    channel_id: str = Field(..., description="Sensor channel identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Measurement timestamp (UTC)")
    voltage_rms: float = Field(..., ge=0, le=600, description="Root-mean-square voltage in Volts")
    current_rms: float = Field(..., ge=0, le=1000, description="Root-mean-square current in Amperes")
    active_power_w: float = Field(..., description="Real active power consumption in Watts")
    reactive_power_var: float = Field(0.0, description="Reactive power in Volt-Amps Reactive")
    apparent_power_va: float = Field(..., ge=0, description="Apparent power in Volt-Amperes")
    power_factor: float = Field(1.0, ge=-1.0, le=1.0, description="Power factor ratio (-1.0 to 1.0)")
    grid_frequency_hz: float = Field(50.0, ge=40.0, le=70.0, description="Mains electrical frequency in Hertz")
    accumulated_kwh: float = Field(0.0, ge=0, description="Cumulative total energy consumed in kilowatt-hours")