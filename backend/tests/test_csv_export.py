"""PowerGuard IoT — CSV Export Formatting Tests"""
import csv, io, pytest

def format_telemetry_csv(records: list) -> str:
    output = io.StringIO()
    if not records: return ""
    fields = ["timestamp", "device_id", "channel", "voltage", "current", "power_w"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for r in records:
        writer.writerow({f: r.get(f, "") for f in fields})
    return output.getvalue()

def test_csv_formatting():
    data = [{"timestamp": "2026-11-10T12:00:00Z", "device_id": "D1", "channel": "main", "voltage": 230.1, "current": 10.2, "power_w": 2347.0}]
    csv_str = format_telemetry_csv(data)
    assert "timestamp,device_id,channel,voltage,current,power_w" in csv_str
    assert "230.1,10.2,2347.0" in csv_str