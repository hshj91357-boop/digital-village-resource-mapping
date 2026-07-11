import React, { useState, useEffect } from 'react';
import api from '../services/api';
import '../styles/Dashboard.css';

interface Village {
  id: number;
  name: string;
  district: string;
  state: string;
  population: number;
  area_sqkm: number;
}

const Dashboard: React.FC = () => {
  const [villages, setVillages] = useState<Village[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchVillages();
  }, []);

  const fetchVillages = async () => {
    try {
      setLoading(true);
      const response = await api.get('/villages/');
      setVillages(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load villages');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>🏘️ Digital Village Resource Mapping</h1>
        <p className="subtitle">AI-powered GIS platform for Smart India Hackathon</p>
      </div>

      <div className="dashboard-content">
        <section className="kpi-section">
          <div className="kpi-card">
            <h3>Total Villages</h3>
            <p className="kpi-value">{villages.length}</p>
          </div>
          <div className="kpi-card">
            <h3>Total Population</h3>
            <p className="kpi-value">
              {villages.reduce((sum, v) => sum + (v.population || 0), 0).toLocaleString()}
            </p>
          </div>
          <div className="kpi-card">
            <h3>Total Area</h3>
            <p className="kpi-value">{villages.reduce((sum, v) => sum + (v.area_sqkm || 0), 0).toFixed(2)} km²</p>
          </div>
        </section>

        <section className="villages-section">
          <h2>Villages</h2>
          {loading ? (
            <p className="loading">Loading villages...</p>
          ) : error ? (
            <p className="error">Error: {error}</p>
          ) : villages.length === 0 ? (
            <p className="no-data">No villages found. Create one to get started!</p>
          ) : (
            <div className="villages-grid">
              {villages.map((village) => (
                <div key={village.id} className="village-card">
                  <h3>{village.name}</h3>
                  <p><strong>District:</strong> {village.district}</p>
                  <p><strong>State:</strong> {village.state}</p>
                  <p><strong>Population:</strong> {village.population?.toLocaleString()}</p>
                  <p><strong>Area:</strong> {village.area_sqkm} km²</p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
