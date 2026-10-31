"""PowerGuard IoT — ML Pipeline, Maintenance & Profiling Tests"""
import pytest
from app.services.MachineLearningPipeline import MachineLearningPipeline
from app.services.PredictiveMaintenanceEngine import PredictiveMaintenanceEngine
from app.services.UserBehaviorProfiler import UserBehaviorProfiler

def test_ml_pipeline_normalization():
    pipeline = MachineLearningPipeline()
    assert pipeline.normalize_features([10.0, 20.0, 30.0], 10.0, 30.0) == [0.0, 0.5, 1.0]

def test_ml_sliding_windows():
    pipeline = MachineLearningPipeline()
    windows = pipeline.create_sliding_windows([1.0, 2.0, 3.0, 4.0, 5.0], 3, 1)
    assert len(windows) == 3
    assert windows[0] == [1.0, 2.0, 3.0]

def test_predictive_maintenance():
    engine = PredictiveMaintenanceEngine()
    assert 0.0 <= engine.calculate_degradation_index(0.85, 0.98, 20000.0) <= 1.0
    assert engine.estimate_remaining_useful_life_hours(80.0, 0.01) == 6000.0

def test_user_behavior_profiler():
    profiler = UserBehaviorProfiler()
    assert profiler.compute_baseload_watts([150.0] * 24) == 150.0
    assert profiler.classify_consumption_pattern(80.0, 20.0) == "commercial_daytime"
    assert profiler.classify_consumption_pattern(50.0, 50.0) == "balanced_residential"