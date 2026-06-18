"""
PowerGuard IoT — API Routes

REST API endpoints for the web dashboard.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse

from app.database import db
from app.mqtt_service import get_latest_readings, get_device_status
from app.config import settings
from app.report_generator import generate_monthly_report_pdf

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Energy Monitoring"])


# ==============================
# Real-time Data
# ==============================

@router.get("/realtime")
async def get_realtime_data(device_id: Optional[str] = None):
    """
    Get the latest readings from all channels.
    Returns in-memory cached data for instant response.
    """
    readings = get_latest_readings()

    if device_id:
        readings = {k: v for k, v in readings.items() if k.startswith(device_id)}

    if not readings:
        return {
            "status": "no_data",
            "message": "No sensor data received yet. Ensure ESP32 is publishing.",
            "channels": {},
        }

    return {
        "status": "ok",
        "channels": readings,
        "last_updated": datetime.utcnow().isoformat(),
    }


# ==============================
# Historical Data
# ==============================

@router.get("/history")
async def get_history(
    channel: str = Query("main", description="Channel name"),
    range: str = Query("-24h", description="Time range (e.g., -1h, -24h, -7d, -30d)"),
    device_id: Optional[str] = None,
):
    """
    Get historical energy readings for a specific channel.
    Supports flexible time ranges.
    """
    # Validate range format
    valid_ranges = ["-1h", "-6h", "-12h", "-24h", "-7d", "-30d"]
    if range not in valid_ranges:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid range. Use one of: {', '.join(valid_ranges)}"
        )

    data = db.get_history(channel=channel, start=range, device_id=device_id)
    return {
        "channel": channel,
        "range": range,
        "count": len(data),
        "readings": data,
    }


# ==============================
# Usage Analytics
# ==============================

@router.get("/usage/daily")
async def get_daily_usage(
    channel: str = Query("main", description="Channel name"),
    days: int = Query(30, ge=1, le=365, description="Number of days"),
    device_id: Optional[str] = None,
):
    """Get daily energy consumption summary with cost estimates."""
    data = db.get_daily_usage(channel=channel, days=days, device_id=device_id)

    total_kwh = sum(d["total_kwh"] for d in data)
    total_cost = sum(d["cost_inr"] for d in data)

    return {
        "channel": channel,
        "days": days,
        "tariff_rate_inr": settings.TARIFF_RATE,
        "total_kwh": round(total_kwh, 3),
        "total_cost_inr": round(total_cost, 2),
        "daily_breakdown": data,
    }


@router.get("/usage/monthly")
async def get_monthly_usage(
    channel: str = Query("main", description="Channel name"),
    device_id: Optional[str] = None,
):
    """Get monthly energy consumption summary."""
    # Get last 30 days of daily data
    daily_data = db.get_daily_usage(channel=channel, days=30, device_id=device_id)

    if not daily_data:
        return {
            "channel": channel,
            "month": datetime.utcnow().strftime("%Y-%m"),
            "total_kwh": 0,
            "avg_daily_kwh": 0,
            "cost_inr": 0,
            "daily_breakdown": [],
        }

    total_kwh = sum(d["total_kwh"] for d in daily_data)
    avg_daily = total_kwh / len(daily_data) if daily_data else 0
    total_cost = total_kwh * settings.TARIFF_RATE

    # Find peak day
    peak_day = max(daily_data, key=lambda d: d["total_kwh"]) if daily_data else None

    return {
        "channel": channel,
        "month": datetime.utcnow().strftime("%Y-%m"),
        "total_kwh": round(total_kwh, 3),
        "avg_daily_kwh": round(avg_daily, 3),
        "cost_inr": round(total_cost, 2),
        "peak_day": peak_day,
        "daily_breakdown": daily_data,
    }


# ==============================
# Reports
# ==============================

@router.get("/reports/monthly")
async def download_monthly_report(
    channel: str = Query("main", description="Channel name"),
    device_id: Optional[str] = None,
):
    """Download a PDF report for the current month's usage."""
    # Re-use the existing logic to get monthly data
    daily_data = db.get_daily_usage(channel=channel, days=30, device_id=device_id)
    
    month_str = datetime.utcnow().strftime("%Y-%m")
    
    if not daily_data:
        data = {
            "total_kwh": 0,
            "avg_daily_kwh": 0,
            "cost_inr": 0,
            "daily_breakdown": [],
        }
    else:
        total_kwh = sum(d["total_kwh"] for d in daily_data)
        avg_daily = total_kwh / len(daily_data) if daily_data else 0
        total_cost = total_kwh * settings.TARIFF_RATE
        
        data = {
            "total_kwh": round(total_kwh, 3),
            "avg_daily_kwh": round(avg_daily, 3),
            "cost_inr": round(total_cost, 2),
            "daily_breakdown": daily_data,
        }
        
    pdf_buffer = generate_monthly_report_pdf(month_str, channel, data)
    
    filename = f"PowerGuard_Report_{channel}_{month_str}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ==============================
# Peak Hours Analysis
# ==============================

@router.get("/analytics/peak-hours")
async def get_peak_hours(
    channel: str = Query("main", description="Channel name"),
    device_id: Optional[str] = None,
):
    """
    Analyze peak usage hours over the last 7 days.
    Returns average power consumption per hour of the day.
    """
    data = db.get_history(channel=channel, start="-7d", device_id=device_id)

    if not data:
        return {"channel": channel, "peak_hours": [], "off_peak_hours": []}

    # Group by hour of day
    hourly_power: dict[int, list[float]] = {h: [] for h in range(24)}
    for reading in data:
        try:
            ts = datetime.fromisoformat(reading["timestamp"].replace("Z", "+00:00"))
            hour = ts.hour
            hourly_power[hour].append(reading.get("power", 0))
        except (ValueError, KeyError):
            continue

    # Calculate averages
    hourly_avg = []
    for hour in range(24):
        values = hourly_power[hour]
        avg = sum(values) / len(values) if values else 0
        hourly_avg.append({"hour": hour, "avg_power_watts": round(avg, 1)})

    # Sort to find peak and off-peak
    sorted_hours = sorted(hourly_avg, key=lambda h: h["avg_power_watts"], reverse=True)
    peak = sorted_hours[:6]      # Top 6 hours
    off_peak = sorted_hours[-6:]  # Bottom 6 hours

    return {
        "channel": channel,
        "hourly_breakdown": hourly_avg,
        "peak_hours": peak,
        "off_peak_hours": off_peak,
    }


# ==============================
# Anomaly Data
# ==============================

@router.get("/anomalies")
async def get_anomalies(
    hours: int = Query(24, ge=1, le=720, description="Hours to look back"),
    device_id: Optional[str] = None,
):
    """Get detected anomalies within a time range."""
    anomalies = db.get_anomalies(hours=hours, device_id=device_id)
    return {
        "count": len(anomalies),
        "hours": hours,
        "anomalies": anomalies,
    }


# ==============================
# Device Info
# ==============================

@router.get("/devices")
async def get_devices():
    """Get list of known devices and their status."""
    readings = get_latest_readings()

    # Extract unique devices and their channels
    devices: dict[str, dict] = {}
    for key, reading in readings.items():
        device_id = reading.get("device_id", "unknown")
        channel = reading.get("channel", "unknown")

        if device_id not in devices:
            devices[device_id] = {
                "device_id": device_id,
                "channels": [],
                "status": get_device_status(device_id),
            }
        if channel not in devices[device_id]["channels"]:
            devices[device_id]["channels"].append(channel)

    return {
        "count": len(devices),
        "devices": list(devices.values()),
    }


# ==============================
# Settings
# ==============================

# In-memory settings (would persist to DB in production)
_threshold_settings = {
    "power_threshold_watts": settings.ANOMALY_POWER_THRESHOLD,
    "left_on_seconds": settings.ANOMALY_LEFT_ON_SECONDS,
    "tariff_rate_inr": settings.TARIFF_RATE,
}


@router.get("/settings/thresholds")
async def get_thresholds():
    """Get current alert threshold settings."""
    return _threshold_settings


@router.post("/settings/thresholds")
async def update_thresholds(
    power_threshold_watts: Optional[float] = None,
    left_on_seconds: Optional[int] = None,
    tariff_rate_inr: Optional[float] = None,
):
    """Update alert threshold settings."""
    if power_threshold_watts is not None:
        _threshold_settings["power_threshold_watts"] = power_threshold_watts
    if left_on_seconds is not None:
        _threshold_settings["left_on_seconds"] = left_on_seconds
    if tariff_rate_inr is not None:
        _threshold_settings["tariff_rate_inr"] = tariff_rate_inr

    logger.info("Updated threshold settings: %s", _threshold_settings)
    return {"status": "updated", "settings": _threshold_settings}
