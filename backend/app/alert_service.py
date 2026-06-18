"""
PowerGuard IoT — Alert Service

Sends anomaly alerts via Telegram Bot and Email (SMTP).
Includes throttling to prevent alert spam.
"""

import logging
import time
from datetime import datetime
from typing import Optional

import requests

from app.config import settings

logger = logging.getLogger(__name__)


class AlertService:
    """
    Dispatches anomaly alerts through Telegram and Email.
    Includes throttling to avoid sending duplicate alerts.
    """

    def __init__(self):
        # Throttle: track last alert time per channel+type
        self._last_alert: dict[str, float] = {}
        self.throttle_seconds = 900  # 15 minutes between same alerts

        # Check if alert services are configured
        self.telegram_enabled = bool(settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID)
        self.email_enabled = bool(settings.EMAIL_SENDER and settings.EMAIL_PASSWORD)

        if self.telegram_enabled:
            logger.info("Telegram alerts enabled.")
        else:
            logger.info("Telegram alerts disabled (no bot token/chat ID configured).")

        if self.email_enabled:
            logger.info("Email alerts enabled.")
        else:
            logger.info("Email alerts disabled (no sender/password configured).")

    def send_alert(self, anomaly: dict):
        """
        Send an anomaly alert via all configured channels.
        Respects throttling to avoid spam.

        Args:
            anomaly: Anomaly dict with type, severity, description, etc.
        """
        # Check throttle
        throttle_key = f"{anomaly.get('channel', '')}:{anomaly.get('type', '')}"
        now = time.time()
        last_sent = self._last_alert.get(throttle_key, 0)

        if now - last_sent < self.throttle_seconds:
            remaining = int(self.throttle_seconds - (now - last_sent))
            logger.debug("Alert throttled for %s (next in %ds)", throttle_key, remaining)
            return

        # Update throttle
        self._last_alert[throttle_key] = now

        # Format message
        message = self._format_message(anomaly)

        # Send via configured channels
        if self.telegram_enabled:
            self._send_telegram(message)

        if self.email_enabled:
            self._send_email(anomaly, message)

        logger.info("Alert sent for %s on %s/%s",
                     anomaly.get("type"), anomaly.get("device_id"), anomaly.get("channel"))

    def _format_message(self, anomaly: dict) -> str:
        """Format anomaly into a human-readable alert message."""
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }

        emoji = severity_emoji.get(anomaly.get("severity", ""), "⚪")
        timestamp = anomaly.get("timestamp", datetime.utcnow().isoformat())

        # Try to make timestamp readable
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            time_str = dt.strftime("%d %b %Y, %H:%M:%S IST")
        except (ValueError, AttributeError):
            time_str = str(timestamp)

        message = (
            f"🚨 *ANOMALY DETECTED* {emoji}\n"
            f"\n"
            f"📍 *Channel:* {anomaly.get('channel', 'unknown')}\n"
            f"📊 *Type:* {anomaly.get('type', 'unknown').replace('_', ' ').title()}\n"
            f"⚠️ *Severity:* {anomaly.get('severity', 'unknown').upper()}\n"
            f"⚡ *Power:* {anomaly.get('power_at_detection', 0):.1f} W\n"
            f"🕐 *Time:* {time_str}\n"
            f"\n"
            f"📝 *Details:* {anomaly.get('description', 'No details')}\n"
            f"🎯 *Score:* {anomaly.get('anomaly_score', 0):.3f}\n"
            f"\n"
            f"_PowerGuard IoT — Smart Energy Monitor_"
        )
        return message

    def _send_telegram(self, message: str):
        """Send alert via Telegram Bot API."""
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("Telegram alert sent successfully.")
            else:
                logger.error("Telegram API error: %d — %s",
                             response.status_code, response.text)
        except requests.RequestException as e:
            logger.error("Failed to send Telegram alert: %s", e)

    def _send_email(self, anomaly: dict, message: str):
        """Send alert via SMTP email."""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        try:
            msg = MIMEMultipart()
            msg["From"] = settings.EMAIL_SENDER
            msg["To"] = settings.EMAIL_RECIPIENT
            msg["Subject"] = (
                f"⚡ PowerGuard Alert: {anomaly.get('type', 'anomaly').replace('_', ' ').title()} "
                f"on {anomaly.get('channel', 'unknown')}"
            )

            # Plain text version (strip markdown)
            plain_text = message.replace("*", "").replace("_", "")
            msg.attach(MIMEText(plain_text, "plain"))

            # Send via SMTP
            with smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
                server.send_message(msg)

            logger.info("Email alert sent to %s.", settings.EMAIL_RECIPIENT)

        except Exception as e:
            logger.error("Failed to send email alert: %s", e)


# Singleton instance
alert_service = AlertService()
