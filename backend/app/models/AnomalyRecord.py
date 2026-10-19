"""
PowerGuard IoT — Anomaly Record Domain Model
Stores machine learning anomaly detection events and inference scores.
"""

from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


class AnomalyRecord(BaseModel):
    """Machine learning inference record for detected electrical consumption anomalies."""
    record_id: str = Field(..., description="Unique anomaly record identifier")
    device_id: str = Field(..., description="Monitored device ID")
    channel_id: str = Field("main", description="Sensor channel where anomaly occurred")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Inference timestamp")
    anomaly_score: float = Field(..., ge=0.0, le=1.0, description="Normalized anomaly confidence score (0 to 1)")
    algorithm: str = Field("IsolationForest", description="ML model architecture: IsolationForest, Autoencoder, DBSCAN")
    classification: str = Field("abnormal_spike", description="Pattern category: abnormal_spike, equipment_leakage, phantom_load")
    features_snapshot: Dict[str, float] = Field(default_factory=dict, description="Input feature values fed to the ML model")
    is_false_positive: bool = Field(False, description="Feedback flag set by user or engineer")
    mitigation_notes: Optional[str] = Field(None, description="Corrective actions or engineering comments")