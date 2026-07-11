import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import MapPage from './pages/MapPage';
import Analysis from './pages/Analysis';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/analysis" element={<Analysis />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
