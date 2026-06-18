"""
PowerGuard IoT — Isolation Forest Training Script

Trains an Isolation Forest model on historical energy data
from InfluxDB. The model learns normal consumption patterns
and can detect anomalies in new readings.

Usage:
    python train_model.py
"""

import os
import sys
import logging

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.config import settings
from backend.app.database import db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ----------------------
# Configuration
# ----------------------

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "isolation_forest.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

# Training parameters
CONTAMINATION = 0.05    # Expected fraction of anomalies (5%)
N_ESTIMATORS = 100      # Number of trees
RANDOM_STATE = 42
DATA_DAYS = 7           # Use last 7 days of data for training


def fetch_training_data(channel: str = "main") -> pd.DataFrame:
    """Fetch historical data from InfluxDB for training."""
    logger.info("Fetching %d days of data for channel '%s'...", DATA_DAYS, channel)

    data = db.get_history(
        channel=channel,
        start=f"-{DATA_DAYS}d",
    )

    if not data:
        logger.warning("No data returned from InfluxDB. Is the database running?")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    logger.info("Fetched %d readings.", len(df))
    return df


def extract_features(df: pd.DataFrame) -> np.ndarray:
    """
    Extract features for Isolation Forest training.

    Features:
        1. Hour of day (0-23)
        2. Power (watts)
        3. Current (amps)
        4. Voltage (volts)
        5. Power factor
    """
    if df.empty:
        return np.array([])

    # Parse timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour

    features = df[['hour', 'power', 'current', 'voltage', 'power_factor']].copy()

    # Fill any NaN values
    features = features.fillna(0)

    logger.info("Extracted %d features from %d readings.", features.shape[1], len(features))
    return features.values


def generate_synthetic_data(n_samples: int = 5000) -> np.ndarray:
    """
    Generate synthetic training data when real data is not available.
    Simulates realistic household energy patterns.
    """
    logger.info("Generating %d synthetic training samples...", n_samples)

    np.random.seed(RANDOM_STATE)

    # Generate hour of day
    hours = np.random.randint(0, 24, n_samples)

    # Power varies by hour (higher during day, lower at night)
    base_power = np.array([
        150, 120, 100, 100, 100, 120,   # 0-5 (night)
        300, 500, 600, 400, 350, 400,   # 6-11 (morning)
        500, 450, 400, 350, 400, 500,   # 12-17 (afternoon)
        800, 900, 850, 700, 400, 250,   # 18-23 (evening)
    ])

    power = np.array([base_power[h] for h in hours])
    power = power + np.random.normal(0, power * 0.15)  # Add 15% noise
    power = np.maximum(power, 10)  # Floor at 10W

    # Voltage: ~230V with small variation
    voltage = np.random.normal(230, 3, n_samples)

    # Current derived from power and voltage
    current = power / voltage

    # Power factor: mostly 0.85-0.99
    pf = np.random.uniform(0.85, 0.99, n_samples)

    features = np.column_stack([hours, power, current, voltage, pf])
    logger.info("Generated synthetic data with shape: %s", features.shape)

    return features


def train_model(features: np.ndarray):
    """Train Isolation Forest model on the feature matrix."""
    logger.info("Training Isolation Forest (n_estimators=%d, contamination=%.2f)...",
                N_ESTIMATORS, CONTAMINATION)

    # Scale features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        max_features=1.0,
        bootstrap=False,
    )
    model.fit(features_scaled)

    # Evaluate on training data
    predictions = model.predict(features_scaled)
    scores = model.decision_function(features_scaled)

    n_normal = np.sum(predictions == 1)
    n_anomaly = np.sum(predictions == -1)
    logger.info("Training results: %d normal, %d anomalies (%.1f%%)",
                n_normal, n_anomaly, n_anomaly / len(predictions) * 100)
    logger.info("Score range: [%.3f, %.3f], mean=%.3f",
                scores.min(), scores.max(), scores.mean())

    return model, scaler


def save_model(model, scaler):
    """Save trained model and scaler to disk."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)
    logger.info("Model saved to %s", MODEL_PATH)

    joblib.dump(scaler, SCALER_PATH)
    logger.info("Scaler saved to %s", SCALER_PATH)


def main():
    """Main training pipeline."""
    logger.info("=" * 50)
    logger.info("  PowerGuard IoT — Model Training")
    logger.info("=" * 50)

    # Step 1: Fetch data
    df = fetch_training_data()

    # Step 2: Extract features (or generate synthetic)
    if df.empty or len(df) < 100:
        logger.warning("Insufficient real data (%d readings). Using synthetic data.",
                       len(df) if not df.empty else 0)
        features = generate_synthetic_data()
    else:
        features = extract_features(df)

    if len(features) == 0:
        logger.error("No features to train on. Exiting.")
        return

    # Step 3: Train
    model, scaler = train_model(features)

    # Step 4: Save
    save_model(model, scaler)

    logger.info("Training complete! Model ready for anomaly detection.")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
