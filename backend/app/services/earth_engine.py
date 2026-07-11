"""
Google Earth Engine integration service.

Handles satellite imagery retrieval and geospatial analysis.
"""

import ee
import geemap
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from PIL import Image
import io

class EarthEngineService:
    """
    Service for Google Earth Engine operations.
    """
    
    def __init__(self, service_account_key: Optional[str] = None):
        """
        Initialize Earth Engine service.
        
        Args:
            service_account_key: Path to Earth Engine service account JSON key
        """
        try:
            if service_account_key:
                ee.Authenticate()
            ee.Initialize()
            self.initialized = True
        except Exception as e:
            print(f"Earth Engine initialization failed: {e}")
            self.initialized = False
    
    def get_sentinel_2_imagery(
        self,
        geometry: Dict[str, Any],
        start_date: str,
        end_date: str,
        cloud_cover: float = 20
    ) -> Dict[str, Any]:
        """
        Get Sentinel-2 satellite imagery.
        
        Args:
            geometry: GeoJSON polygon
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            cloud_cover: Maximum cloud cover percentage
            
        Returns:
            Sentinel-2 image collection metadata
        """
        if not self.initialized:
            return {"error": "Earth Engine not initialized"}
        
        try:
            # Convert GeoJSON to Earth Engine geometry
            coords = geometry['coordinates'][0]
            ee_geometry = ee.Geometry.Polygon(coords)
            
            # Filter Sentinel-2 imagery
            collection = (
                ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                .filterBounds(ee_geometry)
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_cover))
                .sort('system:time_start')
            )
            
            # Get metadata
            size = collection.size().getInfo()
            
            return {
                "status": "success",
                "collection": "Sentinel-2",
                "image_count": size,
                "date_range": {"start": start_date, "end": end_date},
                "cloud_cover_filter": f"<{cloud_cover}%"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_ndvi(
        self,
        geometry: Dict[str, Any],
        date: str
    ) -> Dict[str, Any]:
        """
        Calculate NDVI (Normalized Difference Vegetation Index).
        
        Args:
            geometry: GeoJSON polygon
            date: Date for NDVI calculation (YYYY-MM-DD)
            
        Returns:
            NDVI statistics and data
        """
        if not self.initialized:
            return {"error": "Earth Engine not initialized"}
        
        try:
            # Convert to EE geometry
            coords = geometry['coordinates'][0]
            ee_geometry = ee.Geometry.Polygon(coords)
            
            # Get Sentinel-2 image
            image = (
                ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                .filterBounds(ee_geometry)
                .filterDate(date, ee.Date(date).advance(1, 'day'))
                .first()
            )
            
            if image is None:
                return {"error": "No imagery available for date"}
            
            # Calculate NDVI: (NIR - RED) / (NIR + RED)
            ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            
            # Get statistics
            stats = ndvi.reduceRegion(
                reducer=ee.Reducer.statistics(),
                geometry=ee_geometry,
                scale=10
            ).getInfo()
            
            return {
                "status": "success",
                "index": "NDVI",
                "date": date,
                "statistics": stats.get('NDVI_mean', {})
            }
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_ndbi(
        self,
        geometry: Dict[str, Any],
        date: str
    ) -> Dict[str, Any]:
        """
        Calculate NDBI (Normalized Difference Built-up Index).
        Useful for detecting buildings and urban areas.
        
        Args:
            geometry: GeoJSON polygon
            date: Date for NDBI calculation
            
        Returns:
            NDBI statistics
        """
        if not self.initialized:
            return {"error": "Earth Engine not initialized"}
        
        try:
            coords = geometry['coordinates'][0]
            ee_geometry = ee.Geometry.Polygon(coords)
            
            image = (
                ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                .filterBounds(ee_geometry)
                .filterDate(date, ee.Date(date).advance(1, 'day'))
                .first()
            )
            
            if image is None:
                return {"error": "No imagery available for date"}
            
            # NDBI = (SWIR - NIR) / (SWIR + NIR)
            ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
            
            stats = ndbi.reduceRegion(
                reducer=ee.Reducer.statistics(),
                geometry=ee_geometry,
                scale=10
            ).getInfo()
            
            return {
                "status": "success",
                "index": "NDBI",
                "date": date,
                "statistics": stats.get('NDBI_mean', {})
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_elevation_data(
        self,
        geometry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get elevation data (DEM - Digital Elevation Model).
        
        Args:
            geometry: GeoJSON polygon
            
        Returns:
            Elevation statistics
        """
        if not self.initialized:
            return {"error": "Earth Engine not initialized"}
        
        try:
            coords = geometry['coordinates'][0]
            ee_geometry = ee.Geometry.Polygon(coords)
            
            # SRTM DEM
            dem = ee.Image('USGS/SRTMGL1_Ellip/SRTM30m')
            
            # Get elevation statistics
            stats = dem.reduceRegion(
                reducer=ee.Reducer.statistics(),
                geometry=ee_geometry,
                scale=30
            ).getInfo()
            
            return {
                "status": "success",
                "source": "SRTM 30m DEM",
                "elevation": stats
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_rainfall_data(
        self,
        geometry: Dict[str, Any],
        year: int
    ) -> Dict[str, Any]:
        """
        Get annual rainfall data.
        
        Args:
            geometry: GeoJSON polygon
            year: Year for rainfall data
            
        Returns:
            Rainfall statistics
        """
        if not self.initialized:
            return {"error": "Earth Engine not initialized"}
        
        try:
            coords = geometry['coordinates'][0]
            ee_geometry = ee.Geometry.Polygon(coords)
            
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            
            # CHIRPS rainfall data
            rainfall = (
                ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
                .filterBounds(ee_geometry)
                .filterDate(start_date, end_date)
                .sum()
            )
            
            stats = rainfall.reduceRegion(
                reducer=ee.Reducer.statistics(),
                geometry=ee_geometry,
                scale=5000
            ).getInfo()
            
            return {
                "status": "success",
                "source": "CHIRPS Daily Rainfall",
                "year": year,
                "rainfall_mm": stats
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_water_bodies(
        self,
        geometry: Dict[str, Any],
        date: str
    ) -> Dict[str, Any]:
        """
        Detect water bodies using NDWI (Normalized Difference Water Index).
        
        Args:
            geometry: GeoJSON polygon
            date: Date for water detection
            
        Returns:
            Water body statistics
        """
        if not self.initialized:
            return {"error": "Earth Engine not initialized"}
        
        try:
            coords = geometry['coordinates'][0]
            ee_geometry = ee.Geometry.Polygon(coords)
            
            image = (
                ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                .filterBounds(ee_geometry)
                .filterDate(date, ee.Date(date).advance(1, 'day'))
                .first()
            )
            
            if image is None:
                return {"error": "No imagery available for date"}
            
            # NDWI = (GREEN - NIR) / (GREEN + NIR)
            ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
            
            # Water pixels (NDWI > 0.3)
            water = ndwi.gt(0.3)
            
            water_area = water.reduceRegion(
                reducer=ee.Reducer.sum(),
                geometry=ee_geometry,
                scale=10
            ).getInfo()
            
            return {
                "status": "success",
                "index": "NDWI",
                "date": date,
                "water_detection": water_area
            }
        except Exception as e:
            return {"error": str(e)}
