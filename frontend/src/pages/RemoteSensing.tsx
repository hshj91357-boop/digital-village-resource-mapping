import React, { useState } from 'react';
import api from '../services/api';
import '../styles/RemoteSensing.css';

interface SatelliteData {
  name: string;
  value: number;
  unit: string;
}

const RemoteSensing: React.FC = () => {
  const [selectedVillage, setSelectedVillage] = useState<string>('');
  const [analysisDate, setAnalysisDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [selectedIndex, setSelectedIndex] = useState<string>('ndvi');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const indices = [
    {
      id: 'ndvi',
      name: '🌿 NDVI - Vegetation Index',
      description: 'Normalized Difference Vegetation Index (healthy vegetation)',
      range: '[-1, 1]'
    },
    {
      id: 'ndbi',
      name: '🏢 NDBI - Built-up Index',
      description: 'Normalized Difference Built-up Index (urban areas)',
      range: '[-1, 1]'
    },
    {
      id: 'ndwi',
      name: '💧 NDWI - Water Index',
      description: 'Normalized Difference Water Index (water bodies)',
      range: '[-1, 1]'
    },
    {
      id: 'elevation',
      name: '⛰️ DEM - Elevation Data',
      description: 'Digital Elevation Model (terrain height)',
      range: '[meters]'
    },
    {
      id: 'rainfall',
      name: '🌧️ Rainfall Data',
      description: 'Annual rainfall statistics',
      range: '[mm/year]'
    }
  ];

  const runAnalysis = async () => {
    if (!selectedVillage) {
      setError('Please select a village');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Sample geometry (Central India)
      const geometry = {
        type: 'Polygon',
        coordinates: [[
          [79.9864, 23.1815],
          [80.0864, 23.1815],
          [80.0864, 23.0815],
          [79.9864, 23.0815],
          [79.9864, 23.1815]
        ]]
      };

      let response;

      switch (selectedIndex) {
        case 'ndvi':
          response = await api.post('/api/remote-sensing/indices/ndvi', {
            geometry,
            date: analysisDate
          });
          break;
        case 'ndbi':
          response = await api.post('/api/remote-sensing/indices/ndbi', {
            geometry,
            date: analysisDate
          });
          break;
        case 'ndwi':
          response = await api.post('/api/remote-sensing/indices/ndwi', {
            geometry,
            date: analysisDate
          });
          break;
        case 'elevation':
          response = await api.post('/api/remote-sensing/terrain/elevation', {
            geometry,
            date: analysisDate
          });
          break;
        case 'rainfall':
          const year = parseInt(analysisDate.split('-')[0]);
          response = await api.post('/api/remote-sensing/climate/rainfall', {
            geometry,
            year
          });
          break;
        default:
          setError('Invalid analysis type');
          return;
      }

      setResults(response.data);
    } catch (err: any) {
      setError(err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="remote-sensing-container">
      <div className="rs-header">
        <h1>🛰️ Remote Sensing Analysis</h1>
        <p>Satellite Imagery & Geospatial Indices</p>
      </div>

      <div className="rs-content">
        {/* Control Panel */}
        <div className="rs-controls">
          <div className="control-group">
            <label>Village</label>
            <select
              value={selectedVillage}
              onChange={(e) => setSelectedVillage(e.target.value)}
            >
              <option value="">Select Village</option>
              <option value="raoganj">Raoganj</option>
              <option value="khandwa">Khandwa</option>
              <option value="custom">Custom Area</option>
            </select>
          </div>

          <div className="control-group">
            <label>Analysis Date</label>
            <input
              type="date"
              value={analysisDate}
              onChange={(e) => setAnalysisDate(e.target.value)}
            />
          </div>

          <div className="control-group">
            <label>Spectral Index</label>
            <select
              value={selectedIndex}
              onChange={(e) => setSelectedIndex(e.target.value)}
            >
              {indices.map((idx) => (
                <option key={idx.id} value={idx.id}>
                  {idx.name}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={runAnalysis}
            disabled={loading}
            className="analyze-btn"
          >
            {loading ? '⏳ Analyzing...' : '▶️ Run Analysis'}
          </button>
        </div>

        {/* Index Description */}
        <div className="rs-description">
          {indices.find((i) => i.id === selectedIndex) && (
            <div className="description-card">
              <h3>{indices.find((i) => i.id === selectedIndex)!.name}</h3>
              <p>{indices.find((i) => i.id === selectedIndex)!.description}</p>
              <p className="range">
                <strong>Range:</strong> {indices.find((i) => i.id === selectedIndex)!.range}
              </p>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && <div className="error-message">❌ {error}</div>}

        {/* Results */}
        {results && (
          <div className="rs-results">
            <h2>📊 Analysis Results</h2>
            <div className="results-grid">
              <div className="result-card">
                <h3>Status</h3>
                <p className="result-value">{results.status || results.source || 'Completed'}</p>
              </div>
              <div className="result-card">
                <h3>Date</h3>
                <p className="result-value">{results.date || results.year || analysisDate}</p>
              </div>
              {results.index && (
                <div className="result-card">
                  <h3>Index</h3>
                  <p className="result-value">{results.index}</p>
                </div>
              )}
              {results.statistics && (
                <div className="result-card">
                  <h3>Mean Value</h3>
                  <p className="result-value">
                    {results.statistics.mean?.toFixed(3) || 'N/A'}
                  </p>
                </div>
              )}
            </div>

            {/* Detailed Statistics */}
            {results.statistics && (
              <div className="statistics-panel">
                <h3>📈 Detailed Statistics</h3>
                <table className="stats-table">
                  <tbody>
                    <tr>
                      <td>Minimum</td>
                      <td>{results.statistics.min?.toFixed(4) || 'N/A'}</td>
                    </tr>
                    <tr>
                      <td>Maximum</td>
                      <td>{results.statistics.max?.toFixed(4) || 'N/A'}</td>
                    </tr>
                    <tr>
                      <td>Mean</td>
                      <td>{results.statistics.mean?.toFixed(4) || 'N/A'}</td>
                    </tr>
                    <tr>
                      <td>Std Dev</td>
                      <td>{results.statistics.stdDev?.toFixed(4) || 'N/A'}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            )}

            {/* Interpretation */}
            <div className="interpretation">
              <h3>🔍 Interpretation</h3>
              <div className="interpretation-box">
                {selectedIndex === 'ndvi' && (
                  <p>NDVI values range from -1 (water/cloud) to 1 (dense vegetation). Values &gt; 0.5 indicate healthy vegetation.</p>
                )}
                {selectedIndex === 'ndbi' && (
                  <p>NDBI highlights built-up areas and urban development. Positive values indicate developed areas.</p>
                )}
                {selectedIndex === 'ndwi' && (
                  <p>NDWI identifies water bodies and moisture. Values &gt; 0.3 typically indicate water presence.</p>
                )}
                {selectedIndex === 'elevation' && (
                  <p>Elevation data (DEM) shows terrain height and topography. Useful for flood risk and accessibility analysis.</p>
                )}
                {selectedIndex === 'rainfall' && (
                  <p>Annual rainfall statistics help assess water availability and agricultural potential.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RemoteSensing;
