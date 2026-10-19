"""
PowerGuard IoT — Audit Log Domain Model
Maintains compliance, authentication history, and device configuration change trails.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AuditLog(BaseModel):
    """Security audit log capturing system events, authentication, and device management."""
    event_id: str = Field(..., description="Unique audit event UUID")
    user_id: Optional[str] = Field(None, description="Operator user identifier, if authenticated")
    action: str = Field(..., description="Action taken (e.g. device.reboot, threshold.update, user.login)")
    resource_type: str = Field(..., description="Affected resource category (e.g. Device, AlertConfig, Tariff)")
    resource_id: Optional[str] = Field(None, description="Identifier of the modified entity")
    client_ip: Optional[str] = Field(None, description="Originating client IP address")
    user_agent: Optional[str] = Field(None, description="HTTP client user-agent string")
    status: str = Field("success", description="Execution outcome: success, failure, denied")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC event timestamp")
    details: Dict[str, Any] = Field(default_factory=dict, description="Structured before/after change payload")