import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, FileText, Users, User, Bell, Settings, Languages, Shield, BarChart3 } from 'lucide-react';
import { getUserRole, getDashboardRoute } from '../../utils/auth';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const isLoggedIn = Boolean(localStorage.getItem('authToken'));
  const userRole = getUserRole();

  const handleSignOut = () => {
    localStorage.removeItem('authToken');
    // notify other parts/tabs
    window.dispatchEvent(new StorageEvent('storage', { key: 'authToken', newValue: null }));
    navigate('/auth', { replace: true });
  };

  // Role-based navigation items
  const getRoleBasedNavItems = () => {
    const dashboardRoute = getDashboardRoute();
    const dashboardLabel = userRole === 'authority' ? 'Authority' : 
                          userRole === 'analyst' ? 'Analytics' : 'Dashboard';
    const dashboardIcon = userRole === 'authority' ? Shield : 
                         userRole === 'analyst' ? BarChart3 : Home;

    // Authority users only see their dashboard
    if (userRole === 'authority') {
      return [
        { path: dashboardRoute, label: dashboardLabel, icon: dashboardIcon }
      ];
    }

    // Analyst users only see their dashboard  
    if (userRole === 'analyst') {
      return [
        { path: dashboardRoute, label: dashboardLabel, icon: dashboardIcon }
      ];
    }

    // Citizens see all navigation options
    return [
      { path: dashboardRoute, label: dashboardLabel, icon: dashboardIcon },
      { path: '/report', label: 'Report', icon: FileText },
      { path: '/community', label: 'Community', icon: Users },
      { path: '/profile', label: 'Profile', icon: User },
    ];
  };

  const navItems = isLoggedIn ? getRoleBasedNavItems() : [
    { path: '/', label: 'Home', icon: Home },
    { path: '/report', label: 'Report', icon: FileText },
    { path: '/community', label: 'Community', icon: Users },
    { path: '/profile', label: 'Profile', icon: User },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-blue-600">
              Pravaah
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive(item.path)
                      ? 'text-blue-600 bg-blue-50'
                      : 'text-gray-700 hover:text-blue-600 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <button
                onClick={handleSignOut}
                className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Sign Out
              </button>
            ) : (
              <button
                onClick={() => navigate('/auth')}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Sign In/ Sign Up
              </button>
            )}
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md">
              <Languages className="w-5 h-5" />
            </button>
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md">
              <Settings className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <div className="flex items-center justify-around py-2 border-t">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex flex-col items-center space-y-1 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                    isActive(item.path)
                      ? 'text-blue-600'
                      : 'text-gray-700 hover:text-blue-600'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;