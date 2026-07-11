import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/LayerControl.css';

interface Layer {
  name: string;
  visible: boolean;
  opacity: number;
  type: string;
}

const LayerControl: React.FC = () => {
  const [layers, setLayers] = useState<Layer[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLayers();
  }, []);

  const fetchLayers = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/gis/layers/');
      setLayers(response.data);
    } catch (error) {
      console.error('Failed to fetch layers:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleLayer = async (layerName: string) => {
    try {
      const layer = layers.find(l => l.name === layerName);
      if (layer) {
        await api.patch(`/api/gis/layers/${layerName}`, {
          visible: !layer.visible
        });
        fetchLayers();
      }
    } catch (error) {
      console.error('Failed to toggle layer:', error);
    }
  };

  const updateOpacity = async (layerName: string, opacity: number) => {
    try {
      await api.patch(`/api/gis/layers/${layerName}`, {
        opacity: opacity
      });
      fetchLayers();
    } catch (error) {
      console.error('Failed to update opacity:', error);
    }
  };

  const deleteLayer = async (layerName: string) => {
    try {
      await api.delete(`/api/gis/layers/${layerName}`);
      fetchLayers();
    } catch (error) {
      console.error('Failed to delete layer:', error);
    }
  };

  return (
    <div className="layer-control">
      <h2>📚 Layer Control</h2>
      
      {loading ? (
        <p className="loading">Loading layers...</p>
      ) : layers.length === 0 ? (
        <p className="no-layers">No layers available</p>
      ) : (
        <div className="layers-list">
          {layers.map((layer) => (
            <div key={layer.name} className="layer-item">
              <div className="layer-header">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={layer.visible}
                    onChange={() => toggleLayer(layer.name)}
                  />
                  <span className="layer-name">{layer.name}</span>
                </label>
              </div>
              
              <div className="layer-controls">
                <label className="opacity-label">
                  Opacity: {Math.round(layer.opacity * 100)}%
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={layer.opacity}
                    onChange={(e) => updateOpacity(layer.name, parseFloat(e.target.value))}
                    className="opacity-slider"
                  />
                </label>
                
                <button
                  onClick={() => deleteLayer(layer.name)}
                  className="delete-btn"
                  title="Delete layer"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LayerControl;
