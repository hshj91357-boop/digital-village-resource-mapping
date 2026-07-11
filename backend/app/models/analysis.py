"""
Analysis Result data model.

Stores analysis outputs like risk maps, priority zones, etc.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.core.database import Base

class AnalysisResult(Base):
    """
    Analysis Result model for storing GIS analysis outputs.
    """
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id", ondelete="CASCADE"))
    analysis_type = Column(String(100), index=True)  # flood_risk, water_scarcity, etc.
    result_data = Column(JSONB)  # Stores analysis output
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<AnalysisResult {self.analysis_type}>"
