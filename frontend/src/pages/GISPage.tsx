import React from 'react';
import GISMap from '../components/GISMap';
import LayerControl from '../components/LayerControl';
import '../styles/GISPage.css';

const GISPage: React.FC = () => {
  return (
    <div className="gis-page">
      <div className="gis-container">
        <GISMap />
        <div className="side-panel">
          <LayerControl />
        </div>
      </div>
    </div>
  );
};

export default GISPage;
