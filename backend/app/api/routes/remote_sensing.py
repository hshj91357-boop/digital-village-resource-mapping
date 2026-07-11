"""
Remote Sensing API routes.

Handles satellite imagery retrieval and analysis requests.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.services.remote_sensing import RemoteSensingService
from pydantic import BaseModel

router = APIRouter()
remote_sensing = RemoteSensingService()

class SatelliteRequest(BaseModel):
    """Schema for satellite imagery request."""
    geometry: Dict[str, Any]
    start_date: str
    end_date: str
    cloud_cover: float = 20

class AnalysisRequest(BaseModel):
    """Schema for analysis request."""
    geometry: Dict[str, Any]
    date: str

class TimeSeriesRequest(BaseModel):
    """Schema for time series analysis."""
    geometry: Dict[str, Any]
    date1: str
    date2: str

@router.post("/satellite/sentinel-2")
async def get_sentinel_2(request: SatelliteRequest, db: Session = Depends(get_db)):
    """
    Get Sentinel-2 satellite imagery.
    
    Args:
        request: Satellite imagery request parameters
        db: Database session
        
    Returns:
        Sentinel-2 image collection metadata
    """
    result = remote_sensing.ee_service.get_sentinel_2_imagery(
        request.geometry,
        request.start_date,
        request.end_date,
        request.cloud_cover
    )
    return result

@router.post("/indices/ndvi")
async def calculate_ndvi(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Calculate NDVI (Vegetation Index).
    
    Args:
        request: Analysis request
        db: Database session
        
    Returns:
        NDVI statistics
    """
    result = remote_sensing.ee_service.calculate_ndvi(request.geometry, request.date)
    return result

@router.post("/indices/ndbi")
async def calculate_ndbi(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Calculate NDBI (Built-up Index).
    
    Args:
        request: Analysis request
        db: Database session
        
    Returns:
        NDBI statistics
    """
    result = remote_sensing.ee_service.calculate_ndbi(request.geometry, request.date)
    return result

@router.post("/indices/ndwi")
async def detect_water_bodies(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Detect water bodies using NDWI.
    
    Args:
        request: Analysis request
        db: Database session
        
    Returns:
        Water body detection results
    """
    result = remote_sensing.ee_service.get_water_bodies(request.geometry, request.date)
    return result

@router.post("/terrain/elevation")
async def get_elevation(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Get elevation data (DEM).
    
    Args:
        request: Analysis request
        db: Database session
        
    Returns:
        Elevation statistics
    """
    result = remote_sensing.ee_service.get_elevation_data(request.geometry)
    return result

@router.post("/climate/rainfall")
async def get_rainfall(geometry: Dict[str, Any], year: int, db: Session = Depends(get_db)):
    """
    Get annual rainfall data.
    
    Args:
        geometry: Village boundary
        year: Year for analysis
        db: Database session
        
    Returns:
        Rainfall statistics
    """
    result = remote_sensing.ee_service.get_rainfall_data(geometry, year)
    return result

@router.post("/analysis/resources")
async def analyze_resources(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Comprehensive village resource analysis.
    
    Args:
        request: Analysis request
        db: Database session
        
    Returns:
        Comprehensive analysis results
    """
    result = remote_sensing.analyze_village_resources(request.geometry, request.date)
    return result

@router.post("/analysis/water-scarcity")
async def analyze_water_scarcity(geometry: Dict[str, Any], year: int, db: Session = Depends(get_db)):
    """
    Analyze water scarcity indicators.
    
    Args:
        geometry: Village boundary
        year: Year for analysis
        db: Database session
        
    Returns:
        Water scarcity assessment
    """
    result = remote_sensing.detect_water_scarcity(geometry, year)
    return result

@router.post("/analysis/vegetation-stress")
async def analyze_vegetation_stress(request: TimeSeriesRequest, db: Session = Depends(get_db)):
    """
    Detect vegetation stress using temporal analysis.
    
    Args:
        request: Time series analysis request
        db: Database session
        
    Returns:
        Vegetation change analysis
    """
    result = remote_sensing.detect_vegetation_stress(
        request.geometry,
        request.date1,
        request.date2
    )
    return result

@router.post("/analysis/development-areas")
async def identify_development(request: AnalysisRequest, db: Session = Depends(get_db)):
    """
    Identify developed and undeveloped areas.
    
    Args:
        request: Analysis request
        db: Database session
        
    Returns:
        Development area identification
    """
    result = remote_sensing.identify_development_areas(request.geometry, request.date)
    return result
