"""
PowerGuard IoT — Load Schedule Domain Model
Controls automated appliance load shifting and relay actuation schedules.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class LoadSchedule(BaseModel):
    """Automated schedule for controlling IoT relays and heavy electrical loads."""
    schedule_id: str = Field(..., description="Unique schedule identifier")
    device_id: str = Field(..., description="Target IoT smart controller device ID")
    relay_pin: int = Field(..., ge=0, le=40, description="GPIO pin controlling the mechanical or solid-state relay")
    load_name: str = Field(..., description="Connected appliance label (e.g. Water Heater, EV Charger)")
    action: str = Field("turn_off", description="Scheduled relay action: turn_on, turn_off, toggle, pwm_duty")
    cron_expression: Optional[str] = Field(None, description="Cron format recurrence expression")
    start_time: str = Field("22:00", description="Daily scheduled activation time (HH:MM)")
    duration_minutes: int = Field(120, ge=1, description="Active duration before reverting state")
    days_of_week: List[int] = Field(default=[0, 1, 2, 3, 4, 5, 6], description="Active days (0=Monday, 6=Sunday)")
    is_enabled: bool = Field(True, description="Whether schedule is currently active")