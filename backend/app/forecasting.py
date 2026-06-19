import logging
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

logger = logging.getLogger(__name__)

def generate_forecast(daily_data: list[dict], days_to_predict: int = 7) -> list[dict]:
    """
    Generate an energy consumption forecast for the next `days_to_predict` days
    using Holt-Winters Exponential Smoothing.
    """
    if not daily_data or len(daily_data) < 3:
        # Not enough data to forecast properly. Return naive flat forecast.
        last_val = daily_data[-1]["total_kwh"] if daily_data else 0
        last_date = pd.to_datetime(daily_data[-1]["date"]) if daily_data else pd.Timestamp.today()
        
        forecast = []
        for i in range(1, days_to_predict + 1):
            next_date = (last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d")
            forecast.append({
                "date": next_date,
                "forecast_kwh": round(last_val, 3)
            })
        return forecast

    # Prepare DataFrame
    df = pd.DataFrame(daily_data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    
    # Use Holt's linear trend model (Exponential Smoothing)
    # If len is enough, we could add seasonality, but for daily IoT data 30 days might be short for strong seasonal inference unless it's weekly (seasonal_periods=7)
    try:
        if len(df) >= 14:
            model = ExponentialSmoothing(df['total_kwh'], trend='add', seasonal='add', seasonal_periods=7, initialization_method="estimated")
        else:
            model = ExponentialSmoothing(df['total_kwh'], trend='add', initialization_method="estimated")
            
        fit_model = model.fit()
        forecast_series = fit_model.forecast(days_to_predict)
        
        forecast = []
        for date, val in forecast_series.items():
            # Prevent negative forecasts
            forecast_kwh = max(0, float(val))
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "forecast_kwh": round(forecast_kwh, 3)
            })
        return forecast
    except Exception as e:
        logger.error(f"Forecasting failed: {e}")
        # Fallback to naive
        last_val = df['total_kwh'].iloc[-1]
        last_date = df.index[-1]
        forecast = []
        for i in range(1, days_to_predict + 1):
            next_date = (last_date + pd.Timedelta(days=i)).strftime("%Y-%m-%d")
            forecast.append({
                "date": next_date,
                "forecast_kwh": round(float(last_val), 3)
            })
        return forecast
