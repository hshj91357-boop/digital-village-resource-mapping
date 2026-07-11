"""
Infrastructure API endpoints.

Handles infrastructure feature management and queries.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.infrastructure import Infrastructure
from app.schemas.infrastructure import InfrastructureCreate, InfrastructureResponse

router = APIRouter()

@router.get("/{village_id}", response_model=List[InfrastructureResponse])
async def get_village_infrastructure(
    village_id: int,
    infra_type: str = None,
    db: Session = Depends(get_db)
):
    """
    Get infrastructure for a village.
    
    Args:
        village_id: Village ID
        infra_type: Optional filter by infrastructure type
        db: Database session
        
    Returns:
        List of infrastructure features
    """
    query = db.query(Infrastructure).filter(Infrastructure.village_id == village_id)
    
    if infra_type:
        query = query.filter(Infrastructure.type == infra_type)
    
    return query.all()

@router.post("/", response_model=InfrastructureResponse)
async def create_infrastructure(
    infrastructure: InfrastructureCreate,
    db: Session = Depends(get_db)
):
    """
    Create infrastructure record.
    
    Args:
        infrastructure: Infrastructure data
        db: Database session
        
    Returns:
        Created infrastructure
    """
    db_infra = Infrastructure(**infrastructure.dict())
    db.add(db_infra)
    db.commit()
    db.refresh(db_infra)
    return db_infra
