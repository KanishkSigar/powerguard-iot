"""PowerGuard IoT — Cost Optimization & Tariff Arbitrage Tests"""
import pytest
from app.services.CostOptimizationAnalyzer import CostOptimizationAnalyzer
from app.services.TariffArbitrageManager import TariffArbitrageManager

def test_cost_optimization_tou():
    analyzer = CostOptimizationAnalyzer()
    res = analyzer.compute_tou_cost([10.0, 10.0], {1}, 10.0, 5.0)
    assert res["total_cost"] == 150.0
    assert res["peak_cost"] == 100.0
    assert res["off_peak_cost"] == 50.0

def test_load_shift_recommendation():
    analyzer = CostOptimizationAnalyzer()
    rec = analyzer.recommend_load_shift([0.0, 20.0], {1})
    assert rec["shiftable_kwh"] == 6.0

def test_tariff_arbitrage_windows():
    manager = TariffArbitrageManager()
    windows = manager.identify_arbitrage_windows([float(i) for i in range(24)], 3, 3)
    assert windows["charge_hours"] == [0, 1, 2]
    assert windows["discharge_hours"] == [21, 22, 23]

def test_arbitrage_profit():
    manager = TariffArbitrageManager()
    profit = manager.calculate_potential_profit(10.0, 0.9, 4.0, 10.0)
    assert profit == 50.0