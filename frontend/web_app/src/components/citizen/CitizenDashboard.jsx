import React from 'react';
import Home from '../../pages/Home/Home';

const CitizenDashboard = () => {
  // The citizen dashboard uses the existing Home component
  // This wrapper allows for future citizen-specific customizations
  return <Home />;
};

export default CitizenDashboard;
