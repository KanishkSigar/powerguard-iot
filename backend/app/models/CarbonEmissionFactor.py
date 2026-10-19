"""
PowerGuard IoT — Carbon Emission Factor Model
Models grid greenhouse gas intensity and renewable energy generation mix.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CarbonEmissionFactor(BaseModel):
    """Regional grid carbon intensity factor for carbon footprint tracking."""
    factor_id: Optional[str] = Field(None, description="Unique factor record identifier")
    region_code: str = Field("IN-NR", description="Regional grid zone code (e.g. IN-NR, US-CAISO, EU-DE)")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Validity timestamp")
    emission_factor_gco2_per_kwh: float = Field(..., ge=0, description="Grams of CO2 equivalent per kilowatt-hour")
    renewable_share_percent: float = Field(0.0, ge=0, le=100, description="Percentage of generation from renewable sources")
    fossil_share_percent: float = Field(100.0, ge=0, le=100, description="Percentage of generation from coal/gas/oil")
    source_attribution: str = Field("Central Electricity Authority", description="Reporting agency or provider API")
    is_forecast: bool = Field(False, description="True if value is predicted, False if actual measured data")