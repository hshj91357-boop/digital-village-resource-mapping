"""
Analysis schema definitions.

Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AnalysisResultResponse(BaseModel):
    """
    Schema for analysis result response.
    """
    id: int
    village_id: int
    analysis_type: str
    result_data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
