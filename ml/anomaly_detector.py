"""
PowerGuard IoT — Anomaly Detection Engine

Hybrid anomaly detection combining rule-based checks with
Isolation Forest machine learning model for detecting unusual
energy consumption patterns.
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import joblib

logger = logging.getLogger(__name__)

# Path to saved model
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")


class AnomalyDetector:
    """
    Hybrid anomaly detector combining:
    1. Rule-based checks (thresholds, time-based, duration)
    2. Isolation Forest ML model (pattern anomalies)
    """

    def __init__(self):
        self.model = None
        self.power_threshold = 2000.0  # watts
        self.left_on_seconds = 7200    # 2 hours
        self.channel_baselines: dict[str, dict] = {}
        self._load_model()

    def _load_model(self):
        """Load trained Isolation Forest model if available."""
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                logger.info("Loaded Isolation Forest model from %s", MODEL_PATH)
            except Exception as e:
                logger.error("Failed to load model: %s", e)
                self.model = None
        else:
            logger.info("No trained model found. Using rule-based detection only.")

    def update_thresholds(self, power_threshold: float = None,
                         left_on_seconds: int = None):
        """Update detection thresholds."""
        if power_threshold is not None:
            self.power_threshold = power_threshold
        if left_on_seconds is not None:
            self.left_on_seconds = left_on_seconds
        logger.info("Updated thresholds: power=%.0fW, left_on=%ds",
                     self.power_threshold, self.left_on_seconds)

    def update_baseline(self, channel: str, readings: list[dict]):
        """
        Update baseline statistics for a channel.

        Args:
            channel: Channel name (main, channel1, channel2)
            readings: List of recent readings with 'power_watts' field
        """
        if not readings:
            return

        powers = [r.get("power_watts", 0) for r in readings]
        self.channel_baselines[channel] = {
            "mean": np.mean(powers),
            "std": np.std(powers),
            "min": np.min(powers),
            "max": np.max(powers),
            "p95": np.percentile(powers, 95),
            "count": len(powers),
        }
        logger.debug("Updated baseline for %s: mean=%.1fW, std=%.1fW",
                     channel, self.channel_baselines[channel]["mean"],
                     self.channel_baselines[channel]["std"])

    def check_reading(self, reading: dict,
                      channel_history: Optional[list[dict]] = None) -> list[dict]:
        """
        Check a reading for anomalies.

        Args:
            reading: Current sensor reading dict
            channel_history: Recent readings for duration-based checks

        Returns:
            List of detected anomalies (empty if normal)
        """
        anomalies = []

        channel = reading.get("channel", "unknown")
        power = reading.get("power_watts", 0)
        pf = reading.get("power_factor", 1.0)

        # ---- Rule 1: Absolute Power Threshold ----
        if power > self.power_threshold:
            anomalies.append(self._create_anomaly(
                reading=reading,
                anomaly_type="threshold_breach",
                severity="high",
                description=f"Power ({power:.0f}W) exceeds threshold ({self.power_threshold:.0f}W)",
                score=-0.9,
            ))

        # ---- Rule 2: Statistical Outlier ----
        baseline = self.channel_baselines.get(channel)
        if baseline and baseline["count"] > 10:
            mean = baseline["mean"]
            std = baseline["std"]
            if std > 0 and power > mean + 3 * std:
                anomalies.append(self._create_anomaly(
                    reading=reading,
                    anomaly_type="statistical_outlier",
                    severity="medium",
                    description=f"Power ({power:.0f}W) is {((power - mean) / std):.1f}σ above normal ({mean:.0f}W ± {std:.0f}W)",
                    score=-0.7,
                ))

        # ---- Rule 3: Unusual Time of Day ----
        hour = datetime.now().hour
        if power > 500 and (0 <= hour <= 5):
            anomalies.append(self._create_anomaly(
                reading=reading,
                anomaly_type="unusual_time",
                severity="medium",
                description=f"High power ({power:.0f}W) detected at unusual hour ({hour}:00)",
                score=-0.6,
            ))

        # ---- Rule 4: Low Power Factor ----
        if pf < 0.5 and power > 100:
            anomalies.append(self._create_anomaly(
                reading=reading,
                anomaly_type="low_power_factor",
                severity="low",
                description=f"Low power factor ({pf:.2f}) with {power:.0f}W load — possible motor issue",
                score=-0.5,
            ))

        # ---- Rule 5: Appliance Left On (Duration) ----
        if channel_history and len(channel_history) > 5:
            continuous_power = self._check_continuous_usage(
                channel_history, threshold_watts=100
            )
            if continuous_power and continuous_power > self.left_on_seconds:
                hours = continuous_power / 3600
                anomalies.append(self._create_anomaly(
                    reading=reading,
                    anomaly_type="left_on",
                    severity="medium",
                    description=f"Appliance on {channel} running for {hours:.1f}h continuously",
                    score=-0.65,
                ))

        # ---- ML: Isolation Forest ----
        if self.model:
            ml_anomaly = self._check_ml_model(reading)
            if ml_anomaly:
                anomalies.append(ml_anomaly)

        return anomalies

    def _check_ml_model(self, reading: dict) -> Optional[dict]:
        """Run Isolation Forest on the reading features."""
        try:
            features = self._extract_features(reading)
            features_array = np.array([features])

            # Predict: -1 = anomaly, 1 = normal
            prediction = self.model.predict(features_array)[0]
            score = self.model.decision_function(features_array)[0]

            if prediction == -1:
                return self._create_anomaly(
                    reading=reading,
                    anomaly_type="pattern_anomaly",
                    severity="high" if score < -0.3 else "medium",
                    description=f"ML model detected unusual pattern (score: {score:.3f})",
                    score=score,
                )
        except Exception as e:
            logger.error("ML model prediction error: %s", e)

        return None

    def _extract_features(self, reading: dict) -> list[float]:
        """Extract features for ML model from a reading."""
        hour = datetime.now().hour
        return [
            hour,
            reading.get("power_watts", 0),
            reading.get("current_rms", 0),
            reading.get("voltage_rms", 230),
            reading.get("power_factor", 1.0),
        ]

    def _check_continuous_usage(self, history: list[dict],
                                 threshold_watts: float = 100) -> Optional[float]:
        """
        Check how long power has been above threshold continuously.
        Returns duration in seconds, or None if not above threshold.
        """
        if not history:
            return None

        # Check from most recent going backwards
        continuous_seconds = 0
        for reading in reversed(history):
            power = reading.get("power_watts", 0)
            if power > threshold_watts:
                continuous_seconds += 2  # Assumes 2s interval
            else:
                break

        return continuous_seconds if continuous_seconds > 0 else None

    def _create_anomaly(self, reading: dict, anomaly_type: str,
                        severity: str, description: str,
                        score: float) -> dict:
        """Create a standardized anomaly dict."""
        return {
            "device_id": reading.get("device_id", "unknown"),
            "channel": reading.get("channel", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "type": anomaly_type,
            "severity": severity,
            "description": description,
            "power_at_detection": reading.get("power_watts", 0),
            "anomaly_score": score,
        }


# Singleton instance
detector = AnomalyDetector()
