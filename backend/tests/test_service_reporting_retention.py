"""PowerGuard IoT — Reporting & Data Retention Policy Tests"""
import pytest
from app.services.AutomatedReportingService import AutomatedReportingService
from app.services.DataRetentionPolicyEngine import DataRetentionPolicyEngine

def test_automated_daily_summary():
    reporter = AutomatedReportingService()
    summary = reporter.generate_daily_summary("METER-01", "2026-10-31", [1.0, 2.0, 3.0, 1.5])
    assert summary["total_kwh"] == 7.5
    assert summary["peak_kwh"] == 3.0
    assert summary["peak_hour"] == 2

def test_efficiency_score():
    reporter = AutomatedReportingService()
    score = reporter.calculate_efficiency_score(1000.0, 400.0, 700.0)
    assert 0.0 <= score <= 100.0

def test_retention_tiers():
    retention = DataRetentionPolicyEngine()
    assert retention.determine_retention_tier(3) == "raw_realtime"
    assert retention.determine_retention_tier(15) == "1min_aggregated"
    assert retention.determine_retention_tier(100) == "1hour_rollup"
    assert retention.determine_retention_tier(400) == "expired"
    assert retention.should_purge(400, 365) is True