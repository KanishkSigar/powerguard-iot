"""PowerGuard IoT — Telegram Alert Notification Tests"""
import re
import pytest

def escape_telegram_markdown(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

def build_telegram_alert_message(device_name: str, metric: str, value: float, threshold: float) -> str:
    raw = f"PowerGuard Alert\nDevice: {device_name}\nMetric: {metric}\nValue: {value} (Threshold: {threshold})"
    return escape_telegram_markdown(raw)

def test_telegram_markdown_escaping():
    escaped = escape_telegram_markdown("Alert! Voltage = 245.5V [CRITICAL]")
    assert r"\!" in escaped
    assert r"\=" in escaped
    assert r"\." in escaped
    assert r"\[" in escaped

def test_build_telegram_alert():
    msg = build_telegram_alert_message("Main Panel", "Current", 110.5, 100.0)
    assert "Main Panel" in msg
    assert "Current" in msg