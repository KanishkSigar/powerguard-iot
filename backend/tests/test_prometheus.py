"""PowerGuard IoT — Prometheus Metrics Exposition Tests"""
import pytest

def format_prometheus_gauge(metric_name: str, value: float, labels: dict, help_text: str = "") -> str:
    label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    lines = []
    if help_text:
        lines.append(f"# HELP {metric_name} {help_text}")
        lines.append(f"# TYPE {metric_name} gauge")
    lines.append(f"{metric_name}{{{label_str}}} {value}")
    return "\n".join(lines)

def test_prometheus_gauge_formatting():
    output = format_prometheus_gauge(
        "powerguard_voltage_volts",
        230.5,
        {"device": "ESP32_01", "phase": "a"},
        help_text="RMS AC Voltage in Volts",
    )
    assert "# HELP powerguard_voltage_volts RMS AC Voltage in Volts" in output
    assert "# TYPE powerguard_voltage_volts gauge" in output
    assert 'powerguard_voltage_volts{device="ESP32_01",phase="a"} 230.5' in output