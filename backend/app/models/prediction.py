"""
AI Prediction data model.

Stores results from YOLOv11, SAM, and other AI models.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from datetime import datetime
from app.core.database import Base

class AIPrediction(Base):
    """
    AI Prediction model for storing computer vision results.
    """
    __tablename__ = "ai_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id", ondelete="CASCADE"))
    prediction_type = Column(String(100), index=True)  # building, road, water_tank, solar_panel, etc.
    geometry = Column(Geometry('Polygon', srid=4326), index=True)
    confidence = Column(Float)  # 0-1
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<AIPrediction {self.prediction_type}>"
