"""PowerGuard IoT — Carbon & Grid Dependency Tests"""
import pytest
from app.services.CarbonFootprintTracker import CarbonFootprintTracker
from app.services.GridDependencyEvaluator import GridDependencyEvaluator

def test_carbon_emissions_calculation():
    tracker = CarbonFootprintTracker()
    assert tracker.calculate_emissions_kg(100.0, 680.0) == 68.0

def test_carbon_avoided_and_trees():
    tracker = CarbonFootprintTracker()
    assert tracker.calculate_avoided_emissions(50.0, 680.0) == 34.0
    assert tracker.get_trees_equivalent(217.7) == 10.0

def test_grid_self_sufficiency():
    evaluator = GridDependencyEvaluator()
    res = evaluator.calculate_self_sufficiency(30.0, 10.0, 40.0)
    assert res["self_sufficiency_percent"] == 75.0
    assert res["grid_dependency_percent"] == 25.0

def test_grid_net_energy():
    evaluator = GridDependencyEvaluator()
    assert evaluator.calculate_net_energy(50.0, 30.0) == 20.0