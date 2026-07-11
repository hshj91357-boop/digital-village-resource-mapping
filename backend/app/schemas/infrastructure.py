"""
Infrastructure schema definitions.

Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class InfrastructureCreate(BaseModel):
    """
    Schema for creating infrastructure.
    """
    village_id: int
    type: str
    name: Optional[str] = None
    properties: Optional[Dict[str, Any]] = {}

class InfrastructureResponse(BaseModel):
    """
    Schema for infrastructure response.
    """
    id: int
    village_id: int
    type: str
    name: Optional[str]
    properties: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True
