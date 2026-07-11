"""
Analysis API endpoints.

Handles GIS analysis operations and result retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.analysis import AnalysisResult
from app.schemas.analysis import AnalysisResultResponse

router = APIRouter()

@router.get("/{village_id}", response_model=List[AnalysisResultResponse])
async def get_village_analysis(
    village_id: int,
    analysis_type: str = None,
    db: Session = Depends(get_db)
):
    """
    Get analysis results for a village.
    
    Args:
        village_id: Village ID
        analysis_type: Optional filter by analysis type
        db: Database session
        
    Returns:
        List of analysis results
    """
    query = db.query(AnalysisResult).filter(AnalysisResult.village_id == village_id)
    
    if analysis_type:
        query = query.filter(AnalysisResult.analysis_type == analysis_type)
    
    return query.all()

@router.post("/trigger/{village_id}")
async def trigger_analysis(
    village_id: int,
    analysis_type: str,
    db: Session = Depends(get_db)
):
    """
    Trigger analysis for a village.
    
    Args:
        village_id: Village ID
        analysis_type: Type of analysis to run
        db: Database session
        
    Returns:
        Analysis status
    """
    # Placeholder for analysis trigger logic
    return {
        "status": "Analysis queued",
        "village_id": village_id,
        "analysis_type": analysis_type
    }
