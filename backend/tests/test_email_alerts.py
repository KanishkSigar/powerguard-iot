"""PowerGuard IoT — Email Alert Dispatch Tests"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytest

def create_alert_email(recipient: str, subject: str, device_id: str, alert_message: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[PowerGuard] {subject}"
    msg["From"] = "alerts@powerguard.iot"
    msg["To"] = recipient
    plain_body = f"PowerGuard Alert Notification\nDevice: {device_id}\nDetails: {alert_message}\n"
    html_body = f"<h2>PowerGuard Alert</h2><p><b>Device:</b> {device_id}</p><p>{alert_message}</p>"
    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))
    return msg

def test_email_alert_composition():
    email_obj = create_alert_email("admin@site.com", "Overvoltage Detected", "DEV-01", "Voltage reached 260V")
    assert email_obj["To"] == "admin@site.com"
    assert "[PowerGuard] Overvoltage Detected" in email_obj["Subject"]
    payloads = email_obj.get_payload()
    assert len(payloads) == 2
    assert "DEV-01" in payloads[0].get_payload()