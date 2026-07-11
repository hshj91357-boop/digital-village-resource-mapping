import React, { useState } from 'react';
import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

interface InfrastructureMarkerProps {
  id: number;
  name: string;
  type: string;
  lat: number;
  lon: number;
  properties: Record<string, any>;
}

const InfrastructureMarker: React.FC<InfrastructureMarkerProps> = ({
  id,
  name,
  type,
  lat,
  lon,
  properties
}) => {
  // Icon colors based on type
  const iconColors: Record<string, string> = {
    school: '#3498db',
    hospital: '#e74c3c',
    water_tank: '#2ecc71',
    road: '#f39c12',
    electricity: '#9b59b6',
    police: '#34495e'
  };

  const color = iconColors[type] || '#667eea';

  const icon = L.icon({
    iconUrl: `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='${encodeURIComponent(color)}'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z'/%3E%3C/svg%3E`,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
  });

  return (
    <Marker position={[lat, lon]} icon={icon}>
      <Popup>
        <div className="infrastructure-popup">
          <h3>{name}</h3>
          <p><strong>Type:</strong> {type}</p>
          {Object.entries(properties).map(([key, value]) => (
            <p key={key}><strong>{key}:</strong> {value}</p>
          ))}
        </div>
      </Popup>
    </Marker>
  );
};

export default InfrastructureMarker;
