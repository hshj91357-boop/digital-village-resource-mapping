"""
GIS API routes - Layer management.

Handles GIS layer operations and spatial queries.
"""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.village import Village
from app.services.gis_service import GISLayerService, SpatialQueryService
from pydantic import BaseModel

router = APIRouter()

# Initialize GIS service
gis_service = GISLayerService()
spatial_service = SpatialQueryService()

class LayerCreate(BaseModel):
    """Schema for creating a layer."""
    name: str
    data: Dict[str, Any]
    layer_type: str = "feature"

class LayerUpdate(BaseModel):
    """Schema for updating layer properties."""
    visible: bool = None
    opacity: float = None

class SpatialQuery(BaseModel):
    """Schema for spatial queries."""
    layer_name: str
    bounds: Dict[str, float]

@router.post("/layers/")
async def create_layer(layer: LayerCreate, db: Session = Depends(get_db)):
    """
    Create a new GIS layer.
    
    Args:
        layer: Layer data
        db: Database session
        
    Returns:
        Created layer metadata
    """
    result = gis_service.add_layer(layer.name, layer.data)
    return result

@router.get("/layers/")
async def list_layers(db: Session = Depends(get_db)):
    """
    List all GIS layers.
    
    Args:
        db: Database session
        
    Returns:
        List of layer metadata
    """
    return gis_service.list_layers()

@router.get("/layers/{layer_name}")
async def get_layer(layer_name: str, db: Session = Depends(get_db)):
    """
    Get a specific layer.
    
    Args:
        layer_name: Name of the layer
        db: Database session
        
    Returns:
        Layer data
    """
    layer = gis_service.get_layer(layer_name)
    if not layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return layer

@router.patch("/layers/{layer_name}")
async def update_layer(layer_name: str, update: LayerUpdate, db: Session = Depends(get_db)):
    """
    Update layer properties.
    
    Args:
        layer_name: Name of the layer
        update: Update data
        db: Database session
        
    Returns:
        Updated layer
    """
    if update.visible is not None:
        gis_service.update_layer_visibility(layer_name, update.visible)
    if update.opacity is not None:
        gis_service.update_layer_opacity(layer_name, update.opacity)
    
    layer = gis_service.get_layer(layer_name)
    if not layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    return layer

@router.delete("/layers/{layer_name}")
async def delete_layer(layer_name: str, db: Session = Depends(get_db)):
    """
    Delete a layer.
    
    Args:
        layer_name: Name of the layer
        db: Database session
        
    Returns:
        Success message
    """
    success = gis_service.delete_layer(layer_name)
    if not success:
        raise HTTPException(status_code=404, detail="Layer not found")
    return {"message": "Layer deleted successfully"}

@router.post("/query/within-bounds")
async def query_features_in_bounds(query: SpatialQuery, db: Session = Depends(get_db)):
    """
    Query features within geographic bounds.
    
    Args:
        query: Spatial query parameters
        db: Database session
        
    Returns:
        List of features within bounds
    """
    features = gis_service.get_features_in_bounds(query.layer_name, query.bounds)
    return {
        "layer": query.layer_name,
        "count": len(features),
        "features": features
    }

@router.post("/query/point-in-polygon")
async def point_in_polygon(point: Dict[str, float], polygon_layer: str, db: Session = Depends(get_db)):
    """
    Check if point is inside polygon.
    
    Args:
        point: {"lat", "lon"}
        polygon_layer: Layer name containing polygon
        db: Database session
        
    Returns:
        Containment result
    """
    # Get first polygon from layer
    layer = gis_service.get_layer(polygon_layer)
    if not layer:
        raise HTTPException(status_code=404, detail="Layer not found")
    
    features = layer['data'].get('features', [])
    if not features:
        raise HTTPException(status_code=400, detail="No features in layer")
    
    polygon = features[0]['geometry']
    is_inside = spatial_service.point_in_polygon(point, polygon)
    
    return {"point": point, "layer": polygon_layer, "is_inside": is_inside}

@router.post("/query/distance")
async def calculate_distance(point1: Dict[str, float], point2: Dict[str, float], db: Session = Depends(get_db)):
    """
    Calculate distance between two points.
    
    Args:
        point1: First point {"lat", "lon"}
        point2: Second point {"lat", "lon"}
        db: Database session
        
    Returns:
        Distance in kilometers
    """
    distance = spatial_service.calculate_distance(point1, point2)
    return {
        "point1": point1,
        "point2": point2,
        "distance_km": round(distance, 2),
        "distance_m": round(distance * 1000, 0)
    }

@router.post("/upload/boundary")
async def upload_village_boundary(
    village_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload village boundary (GeoJSON or Shapefile).
    
    Args:
        village_id: Village ID
        file: Boundary file
        db: Database session
        
    Returns:
        Upload status
    """
    # Placeholder for file processing
    return {
        "status": "Boundary upload queued",
        "village_id": village_id,
        "filename": file.filename
    }
