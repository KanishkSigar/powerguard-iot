# Database Schema & Retention Policy

PowerGuard IoT uses **InfluxDB** (version 2.x) to store real-time and historical energy telemetry data and anomaly detection events. InfluxDB is a time-series database optimized for fast writes, compression, and mathematical aggregation over time-based data windows.

---

## 1. Storage Organization

All measurements are stored within the following hierarchy:
- **Organization (`org`)**: `powerguard`
- **Bucket (`bucket`)**: `energy_data`
- **Retention Period**: Default configured to `30 days` (`30d`). Data older than this is automatically dropped by the InfluxDB engine to conserve disk storage.

---

## 2. Measurement: `energy_readings`

This measurement logs raw high-frequency electrical telemetry streaming from edge sensor nodes.

### Tags (Indexed)
Tags are indexed by InfluxDB, allowing fast search and filter queries.

| Tag Key | Type | Description | Example |
|---|---|---|---|
| `device_id` | String | Unique hardware client identifier | `pg_device_01` |
| `channel` | String | Monitored circuit branch name | `main`, `channel1`, `channel2` |

### Fields (Non-Indexed Values)
Fields contain the actual numerical values that are graphed and analyzed.

| Field Key | Type | Unit | Description |
|---|---|---|---|
| `voltage` | Float | Volts (RMS) | AC Root-Mean-Square voltage line reading |
| `current` | Float | Amps (RMS) | AC Root-Mean-Square current flow reading |
| `power` | Float | Watts (W) | Active/Real power consumed by load |
| `apparent_power` | Float | VA | Apparent power calculated ($V \times I$) |
| `power_factor` | Float | Ratio | Efficiency rating ratio (range `0.0` to `1.0`) |
| `energy_kwh` | Float | kWh | Cumulative lifetime energy consumed |

---

## 3. Measurement: `anomalies`

This measurement logs anomalous consumption incidents identified by the hybrid checking engine.

### Tags (Indexed)

| Tag Key | Type | Description | Example |
|---|---|---|---|
| `device_id` | String | Unique hardware client identifier | `pg_device_01` |
| `channel` | String | Monitored circuit branch name | `main` |
| `severity` | String | Event priority rating | `warning`, `critical` |

### Fields (Non-Indexed Values)

| Field Key | Type | Description | Example |
|---|---|---|---|
| `type` | String | Short name of the detected anomaly type | `High Load Spike` |
| `description` | String | Human-readable explanation of why the event fired | `Consumption of 2150W exceeded limits` |
| `power_at_detection` | Float | The measured power draw in Watts when detected | `2150.0` |
| `anomaly_score` | Float | The Isolation Forest score (negative = anomaly) | `-0.125` |

---

## 4. Aggregations and Windowing

To optimize rendering speeds on the frontend dashboard for long-term charts (e.g., `-7d` or `-30d`), the backend uses Flux query aggregates rather than loading raw metrics:

1. **Daily kWh Estimates**: Calculated by taking the mathematical mean of power (Watts) for each `1d` group window, multiplying by 24 hours, and dividing by 1000:
   $$\text{Daily kWh} = \frac{\text{Mean Power (Watts)} \times 24}{1000}$$
2. **Peak Hours Analysis**: Aggregates average power usage grouped by `hour` of the day over a sliding `7-day` window.
