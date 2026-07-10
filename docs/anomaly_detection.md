# Hybrid Anomaly Detection Engine

This document describes how PowerGuard IoT combines traditional deterministic rule checks with machine learning (Isolation Forest) to detect unusual or dangerous energy consumption patterns.

---

## 1. Hybrid Engine Design

Telemetry anomalies can be hardware failures (low power factor), user behavioral oversights (appliance left on), or electrical issues (current surges). To maximize coverage, the engine evaluates incoming readings through **five deterministic rules** and **one machine learning classifier**.

```
[ MQTT Message Payload ]
           │
           ├──► [ Rule 1: Absolute Threshold ] ──► (Trigger if > 2000W)
           │
           ├──► [ Rule 2: Statistical Outlier ] ─► (Trigger if > mean + 3σ)
           │
           ├──► [ Rule 3: Unusual Time Zone ] ──► (Trigger if > 500W at 12 AM - 5 AM)
           │
           ├──► [ Rule 4: Low Power Factor ] ───► (Trigger if PF < 0.5 & Power > 100W)
           │
           ├──► [ Rule 5: Appliance Left On ] ──► (Trigger if continuous load > 2 hrs)
           │
           └──► [ Isolation Forest Classifier ] ──► (Predict using Hour, V, I, W, PF)
```

---

## 2. Rule Specifications

### Rule 1: Absolute Power Threshold
- **Type**: `threshold_breach`
- **Severity**: `high`
- **Logic**: Evaluates whether active power exceeds a safety configuration limit.
- **Formula**:
  $$\text{power\_watts} > \text{power\_threshold}$$
- **Default Limit**: `2000.0 Watts`

### Rule 2: Statistical Outlier (Z-score)
- **Type**: `statistical_outlier`
- **Severity**: `medium`
- **Logic**: Flags a sudden load spike relative to the historical running baseline mean ($\mu$) and standard deviation ($\sigma$) of the channel.
- **Formula**:
  $$\frac{\text{power\_watts} - \mu}{\sigma} > 3.0$$
- **Prerequisite**: At least 10 baseline readings must be collected for the channel.

### Rule 3: Unusual Time of Day
- **Type**: `unusual_time`
- **Severity**: `medium`
- **Logic**: Flags significant power draw occurring during typical sleeping hours.
- **Conditions**:
  $$\text{power\_watts} > 500.0 \quad \text{AND} \quad \text{hour} \in [0, 5]$$

### Rule 4: Low Power Factor
- **Type**: `low_power_factor`
- **Severity**: `low`
- **Logic**: Flags highly inductive or capacitive loads drawing active power. Often indicates motor/pump wear.
- **Conditions**:
  $$\text{power\_factor} < 0.5 \quad \text{AND} \quad \text{power\_watts} > 100.0$$

### Rule 5: Appliance Left On (Duration-based)
- **Type**: `left_on`
- **Severity**: `medium`
- **Logic**: Flags when an appliance is left running continuously for an extended time.
- **Conditions**: Power remains above a baseline (`100W`) continuously for more than `7200 seconds` (2 hours).

---

## 3. Machine Learning: Isolation Forest Outliers

When the Isolation Forest model file is trained and loaded (`ml/models/isolation_forest.pkl`), the engine extracts features dynamically for each reading:
$$\vec{x} = [\text{hour}, \text{power\_watts}, \text{current\_rms}, \text{voltage\_rms}, \text{power\_factor}]$$

- **Prediction**: The model outputs `-1` for anomalies and `1` for normal.
- **Severity**: Classified as `high` if the decision score is $< -0.30$; otherwise, `medium`.
- **Response**: The anomaly is logged to InfluxDB and pushed to the frontend dashboard.
