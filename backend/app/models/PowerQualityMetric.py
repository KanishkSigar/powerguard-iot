"""
PowerGuard IoT — Power Quality Metric Model
Tracks grid power quality anomalies including total harmonic distortion, sags, and swells.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PowerQualityMetric(BaseModel):
    """Grid power quality metrics, harmonic distortion, and transient event logs."""
    metric_id: Optional[str] = Field(None, description="Unique metric event identifier")
    device_id: str = Field(..., description="IoT device identifier")
    channel_id: str = Field("main", description="Monitored channel identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event or sample timestamp")
    thd_voltage_percent: float = Field(..., ge=0, le=100, description="Total Harmonic Distortion of Voltage (%)")
    thd_current_percent: float = Field(..., ge=0, le=100, description="Total Harmonic Distortion of Current (%)")
    voltage_sag_count: int = Field(0, ge=0, description="Occurrences of voltage drops below 90% nominal")
    voltage_swell_count: int = Field(0, ge=0, description="Occurrences of voltage surges above 110% nominal")
    crest_factor: float = Field(1.414, ge=1.0, description="Peak-to-RMS waveform ratio")
    frequency_deviation_hz: float = Field(0.0, description="Deviation from nominal grid frequency (50/60 Hz)")
    power_quality_grade: str = Field("A", description="Grid quality classification: A, B, C, D")