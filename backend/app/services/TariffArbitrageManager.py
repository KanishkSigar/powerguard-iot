"""
PowerGuard IoT — Tariff Arbitrage Manager
Analyzes Time-of-Use rates to generate optimized Battery Energy Storage System (BESS) arbitrage schedules.
"""
from typing import Dict, List, Any

class TariffArbitrageManager:
    def __init__(self):
        self.is_active: bool = True

    def identify_arbitrage_windows(self, hourly_rates: List[float], charge_duration_h: int = 3, discharge_duration_h: int = 3) -> Dict[str, Any]:
        if len(hourly_rates) < 24: return {"charge_hours": [], "discharge_hours": [], "rate_spread": 0.0}
        ranked = sorted(range(len(hourly_rates)), key=lambda h: hourly_rates[h])
        ch = sorted(ranked[:charge_duration_h])
        dis = sorted(ranked[-discharge_duration_h:])
        ch_avg = sum(hourly_rates[h] for h in ch) / len(ch)
        dis_avg = sum(hourly_rates[h] for h in dis) / len(dis)
        return {"charge_hours": ch, "discharge_hours": dis, "avg_charge_rate": round(ch_avg, 2), "avg_discharge_rate": round(dis_avg, 2), "rate_spread": round(dis_avg - ch_avg, 2)}

    def calculate_potential_profit(self, battery_capacity_kwh: float, round_trip_efficiency: float, buy_rate: float, sell_rate: float) -> float:
        cost = battery_capacity_kwh * buy_rate
        revenue = (battery_capacity_kwh * round_trip_efficiency) * sell_rate
        return round(max(0.0, revenue - cost), 2)