import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Report from './pages/Report';
import Community from './pages/Community';
import Profile from './pages/Profile';
import Auth from './pages/Auth';
import OfflineSync from './components/OfflineSync';
import './App.css';

function App() {
  const [authChecked, setAuthChecked] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(Boolean(localStorage.getItem('authToken')));
    setAuthChecked(true);
    const onStorage = (e) => {
      if (e.key === 'authToken') {
        setIsLoggedIn(Boolean(e.newValue));
      }
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  if (!authChecked) return null;

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={isLoggedIn ? <Home /> : <Navigate to="/auth" replace />} />
          <Route path="report" element={<Report />} />
          <Route path="community" element={<Community />} />
          <Route path="profile" element={<Profile />} />
          <Route path="auth" element={isLoggedIn ? <Navigate to="/" replace /> : <Auth />} />
        </Route>
      </Routes>
      {/* Show offline sync status for logged-in users */}
      {isLoggedIn && <OfflineSync />}
    </Router>
  );
}

export default App;
