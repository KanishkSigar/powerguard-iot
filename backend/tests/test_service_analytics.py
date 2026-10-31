"""PowerGuard IoT — Analytics Services Unit Tests"""
import pytest
from app.services.AdvancedAnalyticsService import AdvancedAnalyticsService
from app.services.AnomalyClusteringService import AnomalyClusteringService

def test_analytics_summary_statistics():
    service = AdvancedAnalyticsService()
    stats = service.compute_summary_statistics([100.0, 200.0, 300.0])
    assert stats["count"] == 3
    assert stats["mean"] == 200.0
    assert stats["std_dev"] == 100.0

def test_analytics_papr():
    service = AdvancedAnalyticsService()
    assert 3.0 <= service.calculate_papr(2000.0, 1000.0) <= 3.05
    assert service.calculate_papr(0.0, 100.0) == 0.0

def test_analytics_detect_unbalanced_phases():
    service = AdvancedAnalyticsService()
    balanced = service.detect_unbalanced_phases(230.0, 232.0, 228.0)
    assert balanced["is_critical"] is False

def test_anomaly_clustering_events():
    service = AnomalyClusteringService()
    events = [{"timestamp_s": 100, "alert_type": "sag"}, {"timestamp_s": 150, "alert_type": "spike"}]
    clusters = service.cluster_events(events, time_window_seconds=300)
    assert len(clusters) == 1
    assert clusters[0]["size"] == 2

def test_anomaly_cluster_severity():
    service = AnomalyClusteringService()
    assert service.classify_cluster_severity({"size": 6, "avg_score": 0.9}) == "critical"
    assert service.classify_cluster_severity({"size": 1, "avg_score": 0.2}) == "low"