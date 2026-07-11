import React, { useState } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import '../styles/Analysis.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Analysis: React.FC = () => {
  const [selectedAnalysis, setSelectedAnalysis] = useState('flood-risk');

  const floodRiskData = {
    labels: ['High Risk', 'Medium Risk', 'Low Risk'],
    datasets: [
      {
        label: 'Area (km²)',
        data: [25, 45, 130],
        backgroundColor: ['#e74c3c', '#f39c12', '#27ae60'],
      },
    ],
  };

  const infrastructureData = {
    labels: ['Schools', 'Hospitals', 'Water Tanks', 'Roads', 'Electricity'],
    datasets: [
      {
        label: 'Count',
        data: [5, 2, 8, 120, 150],
        backgroundColor: '#667eea',
        borderColor: '#764ba2',
        borderWidth: 1,
      },
    ],
  };

  const populationTrendData = {
    labels: ['2010', '2015', '2020', '2025'],
    datasets: [
      {
        label: 'Population',
        data: [8500, 9200, 10100, 11000],
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="analysis-page">
      <div className="analysis-header">
        <h1>📊 Analysis Dashboard</h1>
        <p>GIS Analytics and Predictions</p>
      </div>

      <div className="analysis-selector">
        <button
          className={selectedAnalysis === 'flood-risk' ? 'active' : ''}
          onClick={() => setSelectedAnalysis('flood-risk')}
        >
          🌊 Flood Risk
        </button>
        <button
          className={selectedAnalysis === 'infrastructure' ? 'active' : ''}
          onClick={() => setSelectedAnalysis('infrastructure')}
        >
          🏗️ Infrastructure
        </button>
        <button
          className={selectedAnalysis === 'population' ? 'active' : ''}
          onClick={() => setSelectedAnalysis('population')}
        >
          📈 Population Trend
        </button>
      </div>

      <div className="analysis-content">
        {selectedAnalysis === 'flood-risk' && (
          <div className="chart-container">
            <h2>Flood Risk Analysis</h2>
            <Pie data={floodRiskData} />
          </div>
        )}
        {selectedAnalysis === 'infrastructure' && (
          <div className="chart-container">
            <h2>Infrastructure Distribution</h2>
            <Bar data={infrastructureData} />
          </div>
        )}
        {selectedAnalysis === 'population' && (
          <div className="chart-container">
            <h2>Population Trend</h2>
            <Line data={populationTrendData} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Analysis;
