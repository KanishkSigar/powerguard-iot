"""
PowerGuard IoT — Anomaly Clustering Service
Groups correlated power disturbances and voltage sags across temporal windows.
"""
from typing import Dict, List, Any

class AnomalyClusteringService:
    def __init__(self):
        self.is_active: bool = True

    def cluster_events(self, events: List[Dict[str, Any]], time_window_seconds: int = 300) -> List[Dict[str, Any]]:
        if not events:
            return []
        sorted_events = sorted(events, key=lambda x: x.get("timestamp_s", 0))
        clusters = []
        current = [sorted_events[0]]
        for event in sorted_events[1:]:
            if event.get("timestamp_s", 0) - current[-1].get("timestamp_s", 0) <= time_window_seconds:
                current.append(event)
            else:
                clusters.append(self._format_cluster(current))
                current = [event]
        if current:
            clusters.append(self._format_cluster(current))
        return clusters

    def _format_cluster(self, cluster_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        types = list({e.get("alert_type", "unknown") for e in cluster_events})
        avg_score = sum(e.get("anomaly_score", 0.5) for e in cluster_events) / len(cluster_events)
        return {"size": len(cluster_events), "event_types": types, "avg_score": round(avg_score, 3)}

    def classify_cluster_severity(self, cluster: Dict[str, Any]) -> str:
        size = cluster.get("size", 1)
        score = cluster.get("avg_score", 0.0)
        if size >= 5 or score >= 0.85: return "critical"
        elif size >= 3 or score >= 0.65: return "high"
        elif size >= 2: return "medium"
        return "low"