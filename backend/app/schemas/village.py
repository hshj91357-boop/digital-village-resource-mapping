"""
Village schema definitions.

Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class VillageCreate(BaseModel):
    """
    Schema for creating a village.
    """
    name: str
    state: Optional[str] = None
    district: Optional[str] = None
    area_sqkm: Optional[float] = None
    population: Optional[int] = None
    boundary: Optional[Dict[str, Any]] = None

class VillageResponse(BaseModel):
    """
    Schema for village response.
    """
    id: int
    name: str
    state: Optional[str]
    district: Optional[str]
    area_sqkm: Optional[float]
    population: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
