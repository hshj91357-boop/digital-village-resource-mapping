"""
Infrastructure data model.

Represents infrastructure features like schools, hospitals, water tanks, etc.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from datetime import datetime
from app.core.database import Base

class Infrastructure(Base):
    """
    Infrastructure model for storing geographic features.
    """
    __tablename__ = "infrastructure"
    
    id = Column(Integer, primary_key=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id", ondelete="CASCADE"))
    type = Column(String(100), index=True)  # school, hospital, water_tank, road, etc.
    name = Column(String(255))
    location = Column(Geometry('Point', srid=4326), index=True)
    geom = Column(Geometry('Point', srid=4326))
    properties = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Infrastructure {self.name}>"
