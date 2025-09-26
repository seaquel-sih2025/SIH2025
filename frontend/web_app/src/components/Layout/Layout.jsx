import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import { getUserRole } from '../../utils/auth';

const Layout = () => {
  const location = useLocation();
  const userRole = getUserRole();
  
  // Don't show navbar for authority dashboard (it has its own integrated navbar)
  // Only hide navbar if we're specifically on the authority dashboard route
  const hideNavbar = location.pathname === '/dashboard/authority';
  
  return (
    <div className="min-h-screen bg-sky-100">
      {!hideNavbar && <Navbar />}
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
