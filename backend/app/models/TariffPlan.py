"""
PowerGuard IoT — Tariff Plan Domain Model
Manages Time-of-Use (ToU) electricity rate structures and currency tariffs.
"""

from typing import List
from pydantic import BaseModel, Field


class TimeOfUseSlot(BaseModel):
    """Defines a time window and tariff rate for Time-of-Use billing."""
    slot_name: str = Field(..., description="Slot descriptor (e.g. Peak, Off-Peak, Super Off-Peak)")
    start_time: str = Field(..., description="Start time in HH:MM format (24h)")
    end_time: str = Field(..., description="End time in HH:MM format (24h)")
    rate_per_kwh: float = Field(..., ge=0, description="Cost per kilowatt-hour")


class TariffPlan(BaseModel):
    """Utility electricity billing tariff plan configuration."""
    tariff_id: str = Field(..., description="Unique tariff plan ID")
    provider_name: str = Field(..., description="Electricity utility company name")
    plan_name: str = Field(..., description="Commercial plan designation")
    currency: str = Field("INR", description="Three-letter ISO currency code")
    base_charge_monthly: float = Field(0.0, ge=0, description="Fixed monthly meter and connection charge")
    tou_slots: List[TimeOfUseSlot] = Field(default_factory=list, description="Time-of-Use rate schedule slots")
    solar_feedin_tariff: float = Field(0.0, ge=0, description="Credit per kWh fed back into the grid")
    tax_percentage: float = Field(18.0, ge=0, le=100, description="Electricity duty and regulatory tax rate")
    is_active: bool = Field(True, description="Whether this tariff schedule is actively applied")