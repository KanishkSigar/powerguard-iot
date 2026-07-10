# Forecasting Model

This document describes the energy forecasting model used in PowerGuard IoT to predict consumption trends for the upcoming week.

---

## 1. Algorithmic Overview

PowerGuard IoT employs **Holt-Winters Exponential Smoothing** (Triple Exponential Smoothing) via `statsmodels.tsa.holtwinters.ExponentialSmoothing` to project future daily energy usage (kWh).

### Why Holt-Winters?
IoT energy data exhibits two primary characteristics:
1. **Trend**: Gradual increases or decreases in seasonal consumption (e.g., higher cooling loads in summer).
2. **Seasonality**: Repeating patterns over fixed time periods (e.g., higher household consumption on weekends compared to weekdays).

Holt-Winters models these traits by maintaining three distinct smoothing components: level, trend, and seasonal index.

---

## 2. Model Selection Logic

Depending on the length of historical daily consumption aggregates available in InfluxDB, the forecasting service adapts its complexity:

### Case A: Short History ($3 \le N < 14$ days)
The service applies a **Holt's Linear Trend** model (level and trend components only, no seasonal component):
```python
ExponentialSmoothing(df['total_kwh'], trend='add', initialization_method="estimated")
```

### Case B: Long History ($N \ge 14$ days)
The service applies full **Triple Exponential Smoothing** with an additive weekly seasonal period ($L=7$):
```python
ExponentialSmoothing(df['total_kwh'], trend='add', seasonal='add', seasonal_periods=7, initialization_method="estimated")
```

### Case C: Insufficient Data ($N < 3$ days)
If there is not enough historical data, the forecaster falls back to a **Naive Flat Forecast**, projecting the last known daily kWh reading forward:
$$\hat{y}_{t+h} = y_t$$

---

## 3. API Integration

Clients query the forecast through the `GET /api/analytics/forecast` route, which:
1. Fetches daily aggregates from the database for the last 30 days.
2. Fits the Holt-Winters model on the `total_kwh` time-series data.
3. Generates out-of-sample predictions for the next **7 days**.
4. Filters out invalid negative predictions:
   $$\text{forecast\_kwh} = \max(0, \hat{y})$$
5. Formats dates and returns predictions to the frontend for charting.
