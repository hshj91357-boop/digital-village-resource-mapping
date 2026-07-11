"""
Tile server and base map configuration.

Manages different map tile providers (satellite, terrain, etc.)
"""

class TileProviders:
    """
    Configuration for various tile providers.
    """
    
    # OpenStreetMap
    OSM = {
        "name": "OpenStreetMap",
        "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attribution": "&copy; OpenStreetMap contributors",
        "type": "raster"
    }
    
    # Satellite imagery (USGS)
    SATELLITE = {
        "name": "Satellite Imagery",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "attribution": "&copy; Tiles &copy; Esri",
        "type": "raster"
    }
    
    # Terrain
    TERRAIN = {
        "name": "Terrain",
        "url": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        "attribution": "&copy; OpenTopoMap",
        "type": "raster"
    }
    
    # CartoDB Light
    CARTODB_LIGHT = {
        "name": "CartoDB Light",
        "url": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        "attribution": "&copy; CartoDB",
        "type": "raster"
    }
    
    # CartoDB Dark
    CARTODB_DARK = {
        "name": "CartoDB Dark",
        "url": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        "attribution": "&copy; CartoDB",
        "type": "raster"
    }
    
    # Stamen Terrain
    STAMEN_TERRAIN = {
        "name": "Stamen Terrain",
        "url": "https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png",
        "attribution": "&copy; OpenStreetMap",
        "type": "raster"
    }
    
    @classmethod
    def get_all(cls):
        """
        Get all available tile providers.
        
        Returns:
            Dictionary of tile providers
        """
        return {
            'osm': cls.OSM,
            'satellite': cls.SATELLITE,
            'terrain': cls.TERRAIN,
            'cartodb_light': cls.CARTODB_LIGHT,
            'cartodb_dark': cls.CARTODB_DARK,
            'stamen_terrain': cls.STAMEN_TERRAIN,
        }
    
    @classmethod
    def get(cls, provider_name: str):
        """
        Get a specific tile provider.
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            Tile provider configuration
        """
        providers = cls.get_all()
        return providers.get(provider_name, cls.OSM)
