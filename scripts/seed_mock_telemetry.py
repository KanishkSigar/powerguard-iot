#!/usr/bin/env python3
"""
PowerGuard IoT — Synthetic Telemetry Seeding Utility
Generates realistic 3-phase electrical power measurements (voltage, current, power factor, harmonics)
for hardware simulation, API stress-testing, and database seeding.
"""

import argparse
import json
import math
import random
import sys
import time
from datetime import datetime, timezone


def generate_reading(device_id: str, channel: str, phase_angle_deg: float = 0.0) -> dict:
    """Generates a realistic power measurement dictionary."""
    base_voltage = 230.0 + random.uniform(-2.5, 2.5) + (2.0 * math.sin(time.time() / 60.0))
    current_amps = max(0.1, random.uniform(2.0, 15.0) + (1.5 * math.cos(time.time() / 45.0)))
    
    power_factor = round(random.uniform(0.88, 0.96), 3)
    active_power = round(base_voltage * current_amps * power_factor, 2)
    apparent_power = round(base_voltage * current_amps, 2)
    reactive_power = round(math.sqrt(max(0.0, apparent_power**2 - active_power**2)), 2)
    frequency = round(50.0 + random.uniform(-0.08, 0.08), 2)
    
    return {
        "device_id": device_id,
        "channel": channel,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "voltage_rms": round(base_voltage, 2),
        "current_rms": round(current_amps, 2),
        "active_power_w": active_power,
        "reactive_power_var": reactive_power,
        "apparent_power_va": apparent_power,
        "power_factor": power_factor,
        "grid_frequency_hz": frequency,
        "phase_angle_deg": phase_angle_deg,
    }


def main():
    parser = argparse.ArgumentParser(description="Seed synthetic IoT telemetry data")
    parser.add_argument("--device-id", default="ESP32-METER-01", help="Target device ID")
    parser.add_argument("--samples", type=int, default=5, help="Number of samples to generate")
    parser.add_argument("--format", choices=["json", "influx"], default="json", help="Output format")
    args = parser.parse_args()

    channels = [("phase_a", 0.0), ("phase_b", 120.0), ("phase_c", 240.0)]
    for i in range(args.samples):
        for ch_name, angle in channels:
            reading = generate_reading(args.device_id, ch_name, angle)
            if args.format == "json":
                print(json.dumps(reading))
            else:
                line = (
                    f"energy_readings,device_id={reading['device_id']},channel={reading['channel']} "
                    f"voltage={reading['voltage_rms']},current={reading['current_rms']},"
                    f"power={reading['active_power_w']},pf={reading['power_factor']} "
                    f"{int(time.time() * 1e9)}"
                )
                print(line)


if __name__ == "__main__":
    main()