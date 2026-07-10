# Machine Learning Architecture

This document describes the model selection, feature engineering, and training pipeline of the machine learning anomaly detection system in PowerGuard IoT.

---

## 1. Model Selection: Isolation Forest

For identifying unusual multidimensional power patterns, PowerGuard IoT uses **Isolation Forest** (from `scikit-learn`).

### Why Isolation Forest?
1. **Unsupervised Nature**: Energy anomaly data is sparse. We lack tagged datasets of faults. Isolation Forest does not require labeled anomaly classes; it identifies anomalies by isolating outliers in feature space.
2. **Isolation Principle**: Outliers are far away from dense normal clusters. In a randomized decision tree, anomalous samples require fewer splits to be isolated (shorter path lengths from the root) than normal points.
3. **Execution Speed**: The model compiles into light binary structures, enabling fast inference times ($<2\,\text{ms}$) directly on incoming MQTT subscriber threads.

---

## 2. Feature Vector Engineering

The detector processes a five-dimensional feature vector $\vec{x}$ extracted from each incoming reading:

$$\vec{x} = \left[ x_{\text{hour}}, x_{\text{power}}, x_{\text{current}}, x_{\text{voltage}}, x_{\text{pf}} \right]$$

1. **`hour`** ($0-23$): Captures the diurnal patterns of energy consumption.
2. **`power`** (Watts): Real active power consumed.
3. **`current`** (Amps): Load current draw.
4. **`voltage`** (Volts): Network supply voltage.
5. **`power_factor`** ($0.0 - 1.0$): Supply quality metric.

---

## 3. Training & Validation Pipeline

The script `ml/train_model.py` runs the training pipeline.

```
       [ InfluxDB History ] (Last 7 Days)
                │
         (Query Fail?)
          ├──► Yes ──► [ Generate Synthetic Household Data ]
          └──► No  ──► [ Extract Feature DataFrame ]
                               │
                               ▼
                    [ Feature Scaling (StandardScaler) ]
                               │
                               ▼
               [ Fit Isolation Forest Model ]
                (Contamination = 5%, Trees = 100)
                               │
                               ▼
                 [ Export PKL Model & Scaler Artifacts ]
                    To: ml/models/isolation_forest.pkl
```

### Synthetic Household Simulation (Fallback)
If InfluxDB is empty during setup, the pipeline generates synthetic data representing normal house cycles:
- **Baseline sleeping loads** ($100\text{W}-200\text{W}$) between 12 AM and 6 AM.
- **Morning spikes** ($1500\text{W}-2500\text{W}$) around breakfast (7 AM - 9 AM) simulating kettles/toasters.
- **Evening peak loads** ($2000\text{W}-3000\text{W}$) between 6 PM and 10 PM.
- Adds random noise and shifts to voltage/power factor to train the model realistically.
