"""
PowerGuard IoT — Energy Alert Domain Model
Represents threshold violation alerts, overload warnings, and automated incident reports.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EnergyAlert(BaseModel):
    """Incident alert triggered when electrical parameters breach defined thresholds."""
    alert_id: str = Field(..., description="Unique alert identifier")
    device_id: str = Field(..., description="Source device ID")
    channel_id: Optional[str] = Field(None, description="Affected sensor channel")
    alert_type: str = Field(..., description="Classification: overcurrent, overvoltage, undervoltage, low_power_factor, high_consumption")
    severity: str = Field("warning", description="Severity level: info, warning, critical, emergency")
    trigger_value: float = Field(..., description="Observed parameter value that triggered the alert")
    threshold_value: float = Field(..., description="Configured threshold limit")
    message: str = Field(..., description="Human-readable alert summary")
    triggered_at: datetime = Field(default_factory=datetime.utcnow, description="Alert trigger timestamp")
    is_acknowledged: bool = Field(False, description="Whether alert has been acknowledged by operator")
    acknowledged_by: Optional[str] = Field(None, description="Username or system agent that acknowledged the alert")
    resolved_at: Optional[datetime] = Field(None, description="Timestamp when condition returned to normal")