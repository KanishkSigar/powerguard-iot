"""
PowerGuard IoT — Device Domain Model
Defines the IoT edge device entity representing an ESP32 energy monitor node.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class Device(BaseModel):
    """IoT Energy Monitor Hardware Device Model."""
    device_id: str = Field(..., description="Unique hardware identifier or UUID")
    name: str = Field(..., description="User-assigned friendly name")
    mac_address: str = Field(..., description="Device MAC address")
    ip_address: Optional[str] = Field(None, description="Local LAN IP address")
    hardware_version: str = Field("v1.2-ESP32-WROOM", description="PCB and chipset hardware revision")
    firmware_version: str = Field("2.4.0", description="Currently running firmware build version")
    status: str = Field("online", description="Operational status: online, offline, maintenance, error")
    location: Optional[str] = Field("Main Distribution Panel", description="Physical installation site")
    total_channels: int = Field(3, ge=1, le=16, description="Number of CT current clamp channels")
    sampling_interval_ms: int = Field(1000, ge=100, le=60000, description="Telemetry sample rate in milliseconds")
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of latest ping")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom device configuration tags")