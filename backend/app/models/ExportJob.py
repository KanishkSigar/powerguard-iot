"""
PowerGuard IoT — Export Job Domain Model
Tracks background asynchronous data export jobs for CSV, Parquet, and PDF telemetry dumps.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ExportJob(BaseModel):
    """Asynchronous telemetry and analytics export task status."""
    job_id: str = Field(..., description="Unique background job identifier")
    requested_by: str = Field(..., description="User ID who initiated the export")
    device_id: Optional[str] = Field(None, description="Specific device ID or None for all devices")
    export_format: str = Field("csv", description="Output format: csv, parquet, xlsx, json, pdf")
    date_start: datetime = Field(..., description="Telemetry time window start (UTC)")
    date_end: datetime = Field(..., description="Telemetry time window end (UTC)")
    status: str = Field("pending", description="Job progress: pending, processing, completed, failed")
    progress_percentage: float = Field(0.0, ge=0.0, le=100.0, description="Job completion percentage")
    download_url: Optional[str] = Field(None, description="Temporary signed URL to download exported archive")
    file_size_bytes: Optional[int] = Field(None, ge=0, description="Generated file size in bytes")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Job creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")