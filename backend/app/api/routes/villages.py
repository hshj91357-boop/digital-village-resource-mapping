"""
Village API endpoints.

Handles village CRUD operations and boundary management.
"""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.models.village import Village
from app.schemas.village import VillageCreate, VillageResponse

router = APIRouter()

@router.get("/", response_model=List[VillageResponse])
async def list_villages(db: Session = Depends(get_db)):
    """
    Get all villages.
    
    Returns:
        List of villages
    """
    villages = db.query(Village).all()
    return villages

@router.post("/", response_model=VillageResponse)
async def create_village(
    village: VillageCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new village.
    
    Args:
        village: Village data
        db: Database session
        
    Returns:
        Created village
    """
    # Check if village already exists
    existing = db.query(Village).filter(Village.name == village.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Village already exists")
    
    db_village = Village(**village.dict())
    db.add(db_village)
    db.commit()
    db.refresh(db_village)
    return db_village

@router.get("/{village_id}", response_model=VillageResponse)
async def get_village(village_id: int, db: Session = Depends(get_db)):
    """
    Get a specific village by ID.
    
    Args:
        village_id: Village ID
        db: Database session
        
    Returns:
        Village data
    """
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return village

@router.delete("/{village_id}")
async def delete_village(village_id: int, db: Session = Depends(get_db)):
    """
    Delete a village.
    
    Args:
        village_id: Village ID
        db: Database session
        
    Returns:
        Success message
    """
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    
    db.delete(village)
    db.commit()
    return {"message": "Village deleted successfully"}
