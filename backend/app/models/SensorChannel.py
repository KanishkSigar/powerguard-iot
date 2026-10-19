"""
PowerGuard IoT — Sensor Channel Domain Model
Defines individual Current Transformer (CT) clamp and voltage sensor channel configuration.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SensorChannel(BaseModel):
    """Current Transformer (CT) and Voltage Sensing Channel Configuration."""
    channel_id: str = Field(..., description="Channel identifier (e.g. main_phase_a, ac_unit_1)")
    device_id: str = Field(..., description="Parent device ID")
    channel_number: int = Field(..., ge=1, le=16, description="Hardware ADC channel index")
    channel_name: str = Field(..., description="Descriptive circuit name (e.g. HVAC, Solar Inverter)")
    phase_type: str = Field("single_phase", description="Phase designation: single_phase, phase_a, phase_b, phase_c")
    ct_rating_amps: float = Field(100.0, gt=0, description="Rated primary current capacity of the CT clamp")
    calibration_multiplier: float = Field(1.0, gt=0, description="ADC calibration coefficient for current scaling")
    voltage_reference_channel: Optional[int] = Field(0, description="Index of associated AC voltage sensor")
    is_active: bool = Field(True, description="Whether channel data is actively sampled and recorded")
    alert_power_limit_watts: Optional[float] = Field(None, gt=0, description="Upper threshold for power warning")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Channel provisioning timestamp")