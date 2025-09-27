import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Report from './pages/Report';
import Community from './pages/Community';
import Profile from './pages/Profile';
import Auth from './pages/Auth';
import CitizenDashboard from './components/citizen/CitizenDashboard';
import AuthorityDashboard from './components/authority/AuthorityDashboard';
import AnalystDashboard from './components/analyst/AnalystDashboard';
import RoleBasedRoute from './components/shared/RoleBasedRoute';
import { getUserRole, getDashboardRoute, isTokenExpired } from './utils/auth';
import OfflineSync from './components/OfflineSync';
import './App.css';

function App() {
  const [authChecked, setAuthChecked] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const isValidToken = token && !isTokenExpired();
    setIsLoggedIn(isValidToken);
    
    // Clear invalid token
    if (token && !isValidToken) {
      localStorage.removeItem('authToken');
    }
    
    setAuthChecked(true);
    
    const onStorage = (e) => {
      if (e.key === 'authToken') {
        const newToken = e.newValue;
        const isValid = newToken && !isTokenExpired();
        setIsLoggedIn(isValid);
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
          {/* Redirect root to appropriate dashboard based on role */}
          <Route 
            index 
            element={
              isLoggedIn ? 
                <Navigate to={getDashboardRoute()} replace /> : 
                <Navigate to="/auth" replace />
            } 
          />
          
          {/* Role-based dashboards */}
          <Route 
            path="dashboard/citizen" 
            element={
              <RoleBasedRoute allowedRoles={['citizen']}>
                <CitizenDashboard />
              </RoleBasedRoute>
            } 
          />
          <Route 
            path="dashboard/authority" 
            element={
              <RoleBasedRoute allowedRoles={['authority']}>
                <AuthorityDashboard />
              </RoleBasedRoute>
            } 
          />
          <Route 
            path="dashboard/analyst" 
            element={
              <RoleBasedRoute allowedRoles={['analyst']}>
                <AnalystDashboard />
              </RoleBasedRoute>
            } 
          />
          
          {/* Legacy home route - redirect to appropriate dashboard */}
          <Route 
            path="home" 
            element={
              isLoggedIn ? 
                <Navigate to={getDashboardRoute()} replace /> : 
                <Navigate to="/auth" replace />
            } 
          />
          
          {/* Citizen-only routes */}
          <Route 
            path="report" 
            element={
              <RoleBasedRoute allowedRoles={['citizen']}>
                <Report />
              </RoleBasedRoute>
            } 
          />
          <Route 
            path="community" 
            element={
              <RoleBasedRoute allowedRoles={['citizen']}>
                <Community />
              </RoleBasedRoute>
            } 
          />
          <Route 
            path="profile" 
            element={
              <RoleBasedRoute allowedRoles={['citizen']}>
                <Profile />
              </RoleBasedRoute>
            } 
          />
          
          {/* Auth route */}
          <Route 
            path="auth" 
            element={
              isLoggedIn ? 
                <Navigate to={getDashboardRoute()} replace /> : 
                <Auth />
            } 
          />
        </Route>
      </Routes>
      {/* Show offline sync status for logged-in users */}
      {isLoggedIn && <OfflineSync />}
    </Router>
  );
}

export default App;
