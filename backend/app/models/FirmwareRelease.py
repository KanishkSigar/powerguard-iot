"""
PowerGuard IoT — Firmware Release Domain Model
Manages ESP32 Over-The-Air (OTA) firmware binaries, hashes, and rollouts.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class FirmwareRelease(BaseModel):
    """Over-The-Air (OTA) firmware binary release package metadata."""
    release_id: str = Field(..., description="Unique firmware release identifier")
    version: str = Field(..., description="Semantic version string (e.g. 2.4.1)")
    target_hardware: str = Field("ESP32-WROOM-32D", description="Target microcontroller chipset/board")
    binary_size_bytes: int = Field(..., gt=0, description="Size of binary payload in bytes")
    sha256_checksum: str = Field(..., min_length=64, max_length=64, description="Cryptographic SHA-256 hash")
    download_url: str = Field(..., description="HTTPS or S3 distribution URL for binary download")
    release_channel: str = Field("stable", description="Deployment track: alpha, beta, stable")
    minimum_bootloader_version: str = Field("1.0.0", description="Minimum bootloader compatibility version")
    release_notes: str = Field("", description="Markdown release notes and changelog")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Release publishing timestamp")
    is_mandatory: bool = Field(False, description="Whether edge devices must force immediate OTA update")