"""
PowerGuard IoT — Data Simulator

Generates realistic fake sensor data and publishes it to MQTT,
simulating an ESP32 device. Useful for development and testing
without actual hardware.

Usage:
    python simulator.py
"""

import json
import math
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

# ----------------------
# Configuration
# ----------------------

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
DEVICE_ID = "meter_01"
TOPIC_PREFIX = "home/energy"
PUBLISH_INTERVAL = 2  # seconds

# ----------------------
# Simulation Parameters
# ----------------------

# Base load profiles (watts) — simulates realistic household patterns
# Key: hour of day, Value: base power for each channel
LOAD_PROFILES = {
    "main": {
        # Night (low), Morning (medium), Afternoon (high), Evening (peak)
        0: 150, 1: 120, 2: 100, 3: 100, 4: 100, 5: 120,
        6: 300, 7: 500, 8: 600, 9: 400, 10: 350, 11: 400,
        12: 500, 13: 450, 14: 400, 15: 350, 16: 400, 17: 500,
        18: 800, 19: 900, 20: 850, 21: 700, 22: 400, 23: 250,
    },
    "channel1": {  # Kitchen
        0: 50, 1: 30, 2: 20, 3: 20, 4: 20, 5: 30,
        6: 150, 7: 300, 8: 200, 9: 100, 10: 80, 11: 100,
        12: 250, 13: 200, 14: 100, 15: 80, 16: 100, 17: 200,
        18: 400, 19: 450, 20: 350, 21: 200, 22: 100, 23: 60,
    },
    "channel2": {  # Bedroom
        0: 80, 1: 70, 2: 60, 3: 60, 4: 60, 5: 70,
        6: 100, 7: 150, 8: 200, 9: 150, 10: 120, 11: 150,
        12: 180, 13: 150, 14: 130, 15: 120, 16: 150, 17: 180,
        18: 250, 19: 300, 20: 280, 21: 250, 22: 180, 23: 120,
    },
}

# Cumulative energy tracking
cumulative_energy = {"main": 0.0, "channel1": 0.0, "channel2": 0.0}


def get_simulated_reading(channel: str, hour: int) -> dict:
    """Generate a realistic simulated reading for a channel."""

    base_power = LOAD_PROFILES[channel].get(hour, 200)

    # Add realistic noise (±15%)
    noise = random.uniform(-0.15, 0.15)
    power = base_power * (1 + noise)

    # Simulate occasional spikes (appliance turning on)
    if random.random() < 0.05:  # 5% chance of spike
        spike = random.uniform(200, 800)
        power += spike

    # Ensure positive
    power = max(power, 10)

    # Calculate other values
    voltage = random.gauss(230, 3)  # Indian standard: 230V ±3V
    current = power / voltage
    power_factor = random.uniform(0.85, 0.99)
    real_power = power * power_factor
    apparent_power = power

    # Update cumulative energy (kWh)
    hours_elapsed = PUBLISH_INTERVAL / 3600.0
    cumulative_energy[channel] += real_power * hours_elapsed / 1000.0

    return {
        "device_id": DEVICE_ID,
        "channel": channel,
        "timestamp": int(time.time()),
        "voltage_rms": round(voltage, 1),
        "current_rms": round(current, 2),
        "power_watts": round(real_power, 1),
        "apparent_power_va": round(apparent_power, 1),
        "power_factor": round(power_factor, 2),
        "energy_kwh": round(cumulative_energy[channel], 4),
    }


def inject_anomaly(reading: dict, anomaly_type: str) -> dict:
    """Inject an anomaly into a reading for testing anomaly detection."""
    if anomaly_type == "spike":
        reading["power_watts"] = round(random.uniform(2500, 4000), 1)
        reading["current_rms"] = round(reading["power_watts"] / reading["voltage_rms"], 2)
    elif anomaly_type == "zero":
        reading["power_watts"] = 0
        reading["current_rms"] = 0
    elif anomaly_type == "low_pf":
        reading["power_factor"] = round(random.uniform(0.3, 0.5), 2)
    return reading


def main():
    """Run the data simulator."""

    print("=" * 50)
    print("  PowerGuard IoT — Data Simulator")
    print(f"  Device: {DEVICE_ID}")
    print(f"  Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"  Interval: {PUBLISH_INTERVAL}s")
    print("=" * 50)
    print()

    # Connect to MQTT broker
    client = mqtt.Client(client_id=f"simulator_{DEVICE_ID}")

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    except ConnectionRefusedError:
        print(f"[ERROR] Cannot connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
        print("[ERROR] Make sure Mosquitto is running.")
        return

    client.loop_start()

    # Publish device online status
    client.publish(f"{TOPIC_PREFIX}/{DEVICE_ID}/status", "online", retain=True)
    print(f"[STATUS] Device {DEVICE_ID} is online")

    reading_count = 0
    anomaly_interval = random.randint(50, 100)  # Inject anomaly every 50-100 readings

    try:
        while True:
            hour = datetime.now().hour
            reading_count += 1

            for channel in ["main", "channel1", "channel2"]:
                reading = get_simulated_reading(channel, hour)

                # Occasionally inject anomalies for testing
                if reading_count % anomaly_interval == 0 and channel == "main":
                    anomaly_type = random.choice(["spike", "low_pf"])
                    reading = inject_anomaly(reading, anomaly_type)
                    print(f"  ⚠️  ANOMALY INJECTED ({anomaly_type}) on {channel}")
                    anomaly_interval = random.randint(50, 100)

                # Publish to MQTT
                topic = f"{TOPIC_PREFIX}/{DEVICE_ID}/{channel}"
                payload = json.dumps(reading)
                client.publish(topic, payload)

            # Print summary
            main_r = get_simulated_reading("main", hour)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                  f"V: {main_r['voltage_rms']}V  "
                  f"Main: {main_r['power_watts']}W  "
                  f"Ch1: {reading_count}  "
                  f"Energy: {cumulative_energy['main']:.4f} kWh")

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\n[INFO] Simulator stopped by user.")
    finally:
        client.publish(f"{TOPIC_PREFIX}/{DEVICE_ID}/status", "offline", retain=True)
        client.loop_stop()
        client.disconnect()
        print("[STATUS] Device offline. Disconnected.")


if __name__ == "__main__":
    main()
