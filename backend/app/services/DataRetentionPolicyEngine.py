"""
PowerGuard IoT — Data Retention Policy Engine
Enforces tiered data lifecycle management, downsampling, and automated purging.
"""
class DataRetentionPolicyEngine:
    def __init__(self):
        self.raw_retention_days: int = 7
        self.minute_retention_days: int = 30
        self.hourly_retention_days: int = 365

    def determine_retention_tier(self, age_days: int) -> str:
        if age_days <= self.raw_retention_days: return "raw_realtime"
        elif age_days <= self.minute_retention_days: return "1min_aggregated"
        elif age_days <= self.hourly_retention_days: return "1hour_rollup"
        return "expired"

    def should_purge(self, age_days: int, max_retention_days: int = 365) -> bool:
        return age_days > max_retention_days

    def get_downsampling_factor(self, age_days: int) -> int:
        tier = self.determine_retention_tier(age_days)
        if tier == "raw_realtime": return 1
        elif tier == "1min_aggregated": return 60
        elif tier == "1hour_rollup": return 3600
        return 86400