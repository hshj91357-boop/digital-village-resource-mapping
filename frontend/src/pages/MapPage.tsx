import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import '../styles/MapPage.css';

const MapPage: React.FC = () => {
  const [villageGeoJSON, setVillageGeoJSON] = useState<any>(null);

  useEffect(() => {
    // Sample GeoJSON - replace with real data
    const sampleGeoJSON = {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [[
              [78.5, 23.2],
              [78.6, 23.2],
              [78.6, 23.1],
              [78.5, 23.1],
              [78.5, 23.2]
            ]]
          },
          properties: { name: 'Sample Village' }
        }
      ]
    };
    setVillageGeoJSON(sampleGeoJSON);
  }, []);

  const defaultCenter: [number, number] = [23.1815, 79.9864]; // Central India

  return (
    <div className="map-page">
      <div className="map-sidebar">
        <h2>Map Controls</h2>
        <div className="layer-control">
          <label>
            <input type="checkbox" defaultChecked /> Satellite Imagery
          </label>
          <label>
            <input type="checkbox" defaultChecked /> Buildings
          </label>
          <label>
            <input type="checkbox" /> Roads
          </label>
          <label>
            <input type="checkbox" /> Water Bodies
          </label>
          <label>
            <input type="checkbox" /> Infrastructure
          </label>
        </div>
      </div>

      <MapContainer center={defaultCenter} zoom={10} className="map-container">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        {villageGeoJSON && (
          <GeoJSON data={villageGeoJSON} />
        )}
      </MapContainer>
    </div>
  );
};

export default MapPage;
