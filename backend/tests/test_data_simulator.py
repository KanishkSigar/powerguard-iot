"""PowerGuard IoT — Synthetic AC Waveform Simulation Tests"""
import math
import pytest

def simulate_sine_wave(amplitude: float, frequency_hz: float, sample_rate_hz: int, num_samples: int) -> list:
    samples = []
    for i in range(num_samples):
        t = i / sample_rate_hz
        val = amplitude * math.sin(2.0 * math.pi * frequency_hz * t)
        samples.append(round(val, 4))
    return samples

def test_sine_wave_generation():
    samples = simulate_sine_wave(amplitude=325.27, frequency_hz=50.0, sample_rate_hz=1000, num_samples=20)
    assert len(samples) == 20
    assert samples[0] == 0.0 # sin(0) = 0
    # Quarter cycle (5ms at 50Hz = 5 samples) should be near peak
    assert samples[5] == pytest.approx(325.27, rel=1e-2)