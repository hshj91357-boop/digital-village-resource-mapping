import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, FeatureGroup, GeoJSON, LayerGroup } from 'react-leaflet';
import { EditControl } from 'react-leaflet-draw';
import L from 'leaflet';
import 'leaflet-draw/dist/leaflet.draw.css';
import api from '../services/api';
import '../styles/GISMap.css';

interface BaseMap {
  name: string;
  url: string;
  attribution: string;
}

interface GISLayer {
  name: string;
  data: any;
  visible: boolean;
  opacity: number;
}

const GISMap: React.FC = () => {
  const [baseMaps, setBaseMaps] = useState<Record<string, BaseMap>>({
    'OSM': {
      name: 'OpenStreetMap',
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; OpenStreetMap contributors'
    },
    'Satellite': {
      name: 'Satellite Imagery',
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attribution: '&copy; Tiles &copy; Esri'
    },
    'Terrain': {
      name: 'Terrain',
      url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
      attribution: '&copy; OpenTopoMap'
    },
    'CartoDB Dark': {
      name: 'CartoDB Dark',
      url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      attribution: '&copy; CartoDB'
    }
  });

  const [selectedBaseMap, setSelectedBaseMap] = useState<string>('OSM');
  const [layers, setLayers] = useState<GISLayer[]>([]);
  const [drawnItems, setDrawnItems] = useState<any>(null);
  const mapRef = useRef<any>(null);

  const defaultCenter: [number, number] = [23.1815, 79.9864]; // Central India

  // Fetch available layers
  useEffect(() => {
    fetchLayers();
  }, []);

  const fetchLayers = async () => {
    try {
      const response = await api.get('/api/gis/layers/');
      setLayers(response.data);
    } catch (error) {
      console.error('Failed to load layers:', error);
    }
  };

  // Handle layer visibility toggle
  const toggleLayerVisibility = async (layerName: string) => {
    try {
      const layer = layers.find(l => l.name === layerName);
      if (layer) {
        await api.patch(`/api/gis/layers/${layerName}`, {
          visible: !layer.visible
        });
        fetchLayers();
      }
    } catch (error) {
      console.error('Failed to toggle layer visibility:', error);
    }
  };

  // Handle layer opacity change
  const updateLayerOpacity = async (layerName: string, opacity: number) => {
    try {
      await api.patch(`/api/gis/layers/${layerName}`, {
        opacity: opacity
      });
      fetchLayers();
    } catch (error) {
      console.error('Failed to update layer opacity:', error);
    }
  };

  // Handle drawing completion
  const handleDraw = async (e: any) => {
    const { layer } = e;
    const geoJSON = layer.toGeoJSON();
    setDrawnItems(geoJSON);
    
    // Save to backend
    try {
      await api.post('/api/gis/layers/', {
        name: `drawn-${Date.now()}`,
        data: geoJSON,
        layer_type: 'drawn'
      });
      fetchLayers();
    } catch (error) {
      console.error('Failed to save drawn geometry:', error);
    }
  };

  // Handle file upload
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/api/gis/upload/boundary', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      console.log('Upload success:', response.data);
      fetchLayers();
    } catch (error) {
      console.error('Failed to upload boundary:', error);
    }
  };

  return (
    <div className="gis-map-container">
      {/* Controls Panel */}
      <div className="map-controls-panel">
        <div className="control-section">
          <h3>🗺️ Base Map</h3>
          <select 
            value={selectedBaseMap}
            onChange={(e) => setSelectedBaseMap(e.target.value)}
            className="select-control"
          >
            {Object.entries(baseMaps).map(([key, map]) => (
              <option key={key} value={key}>{map.name}</option>
            ))}
          </select>
        </div>

        <div className="control-section">
          <h3>📁 Layers</h3>
          <div className="layers-list">
            {layers.map((layer) => (
              <div key={layer.name} className="layer-item">
                <label className="layer-checkbox">
                  <input
                    type="checkbox"
                    checked={layer.visible}
                    onChange={() => toggleLayerVisibility(layer.name)}
                  />
                  {layer.name}
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={layer.opacity}
                  onChange={(e) => updateLayerOpacity(layer.name, parseFloat(e.target.value))}
                  className="opacity-slider"
                />
              </div>
            ))}
          </div>
        </div>

        <div className="control-section">
          <h3>📤 Upload Boundary</h3>
          <input
            type="file"
            accept=".geojson,.json,.shp,.zip"
            onChange={handleFileUpload}
            className="file-input"
          />
        </div>
      </div>

      {/* Map */}
      <MapContainer 
        center={defaultCenter} 
        zoom={9} 
        className="gis-map"
        ref={mapRef}
      >
        {/* Base Map Layer */}
        <TileLayer
          url={baseMaps[selectedBaseMap].url}
          attribution={baseMaps[selectedBaseMap].attribution}
        />

        {/* Drawing Layer */}
        <FeatureGroup>
          <EditControl
            position="topleft"
            onCreated={handleDraw}
            onEdited={handleDraw}
            onDeleted={handleDraw}
            draw={{
              rectangle: true,
              polygon: true,
              circle: false,
              circlemarker: false,
              marker: true,
              polyline: false
            }}
          />
        </FeatureGroup>

        {/* GIS Layers */}
        {layers.map((layer) => (
          layer.visible && (
            <GeoJSON
              key={layer.name}
              data={layer.data}
              style={{
                opacity: layer.opacity,
                fillOpacity: layer.opacity * 0.5,
                color: '#667eea',
                weight: 2
              }}
              onEachFeature={(feature, featureLayer) => {
                if (feature.properties) {
                  featureLayer.bindPopup(
                    `<div class="popup">
                      ${Object.entries(feature.properties)
                        .map(([key, value]) => `<p><strong>${key}:</strong> ${value}</p>`)
                        .join('')}
                    </div>`
                  );
                }
              }}
            />
          )
        ))}
      </MapContainer>
    </div>
  );
};

export default GISMap;
