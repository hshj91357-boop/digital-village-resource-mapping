"""
GIS Layer management service.

Handles multi-layer map operations, spatial queries, and layer management.
"""

from typing import List, Dict, Any, Optional
import geopandas as gpd
from shapely.geometry import Point, Polygon, shape
import json

class GISLayerService:
    """
    Service for managing GIS layers and spatial operations.
    """
    
    def __init__(self):
        self.layers = {}
        self.active_layers = set()
    
    def add_layer(self, layer_name: str, layer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new GIS layer.
        
        Args:
            layer_name: Name of the layer
            layer_data: GeoJSON or layer configuration
            
        Returns:
            Layer metadata
        """
        self.layers[layer_name] = {
            'name': layer_name,
            'data': layer_data,
            'visible': True,
            'opacity': 1.0,
            'type': layer_data.get('type', 'feature'),
        }
        return self.layers[layer_name]
    
    def get_layer(self, layer_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific layer.
        
        Args:
            layer_name: Name of the layer
            
        Returns:
            Layer data or None
        """
        return self.layers.get(layer_name)
    
    def list_layers(self) -> List[Dict[str, Any]]:
        """
        List all available layers.
        
        Returns:
            List of layer metadata
        """
        return list(self.layers.values())
    
    def update_layer_visibility(self, layer_name: str, visible: bool) -> bool:
        """
        Toggle layer visibility.
        
        Args:
            layer_name: Name of the layer
            visible: Visibility status
            
        Returns:
            Success status
        """
        if layer_name in self.layers:
            self.layers[layer_name]['visible'] = visible
            if visible:
                self.active_layers.add(layer_name)
            else:
                self.active_layers.discard(layer_name)
            return True
        return False
    
    def update_layer_opacity(self, layer_name: str, opacity: float) -> bool:
        """
        Update layer opacity (0-1).
        
        Args:
            layer_name: Name of the layer
            opacity: Opacity value (0-1)
            
        Returns:
            Success status
        """
        if layer_name in self.layers and 0 <= opacity <= 1:
            self.layers[layer_name]['opacity'] = opacity
            return True
        return False
    
    def get_features_in_bounds(self, layer_name: str, bounds: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Get features within specified geographic bounds.
        
        Args:
            layer_name: Name of the layer
            bounds: {"min_lat", "max_lat", "min_lon", "max_lon"}
            
        Returns:
            List of features within bounds
        """
        layer = self.get_layer(layer_name)
        if not layer:
            return []
        
        # Create bounding box polygon
        bbox = Polygon([
            (bounds['min_lon'], bounds['min_lat']),
            (bounds['max_lon'], bounds['min_lat']),
            (bounds['max_lon'], bounds['max_lat']),
            (bounds['min_lon'], bounds['max_lat']),
        ])
        
        features_in_bounds = []
        for feature in layer['data'].get('features', []):
            geom = shape(feature['geometry'])
            if bbox.intersects(geom):
                features_in_bounds.append(feature)
        
        return features_in_bounds
    
    def delete_layer(self, layer_name: str) -> bool:
        """
        Delete a layer.
        
        Args:
            layer_name: Name of the layer
            
        Returns:
            Success status
        """
        if layer_name in self.layers:
            del self.layers[layer_name]
            self.active_layers.discard(layer_name)
            return True
        return False


class SpatialQueryService:
    """
    Service for spatial queries on geographic data.
    """
    
    @staticmethod
    def point_in_polygon(point: Dict[str, float], polygon: Dict[str, Any]) -> bool:
        """
        Check if a point is inside a polygon.
        
        Args:
            point: {"lat", "lon"}
            polygon: GeoJSON polygon
            
        Returns:
            True if point is inside polygon
        """
        p = Point(point['lon'], point['lat'])
        poly = shape(polygon)
        return poly.contains(p)
    
    @staticmethod
    def buffer_geometry(geometry: Dict[str, Any], distance_km: float) -> Dict[str, Any]:
        """
        Create a buffer around a geometry.
        
        Args:
            geometry: GeoJSON geometry
            distance_km: Buffer distance in kilometers
            
        Returns:
            Buffered geometry as GeoJSON
        """
        geom = shape(geometry)
        # Approximate conversion: 1 degree ≈ 111 km
        buffered = geom.buffer(distance_km / 111.0)
        return json.loads(json.dumps(
            {'type': buffered.geom_type, 'coordinates': list(buffered.coords)},
            default=str
        ))
    
    @staticmethod
    def calculate_distance(point1: Dict[str, float], point2: Dict[str, float]) -> float:
        """
        Calculate distance between two points in kilometers.
        
        Args:
            point1: {"lat", "lon"}
            point2: {"lat", "lon"}
            
        Returns:
            Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2
        
        lat1, lon1 = radians(point1['lat']), radians(point1['lon'])
        lat2, lon2 = radians(point2['lat']), radians(point2['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        # Earth's radius in km
        R = 6371
        return R * c
    
    @staticmethod
    def intersect_geometries(geom1: Dict[str, Any], geom2: Dict[str, Any]) -> bool:
        """
        Check if two geometries intersect.
        
        Args:
            geom1: GeoJSON geometry
            geom2: GeoJSON geometry
            
        Returns:
            True if geometries intersect
        """
        g1 = shape(geom1)
        g2 = shape(geom2)
        return g1.intersects(g2)
