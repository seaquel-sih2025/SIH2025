// JWT token utilities for role-based access control

/**
 * Decode JWT token payload (without verification - for client-side role routing only)
 * Note: This is not secure verification, just for UI routing decisions
 */
export const decodeJWT = (token) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding JWT:', error);
    return null;
  }
};

/**
 * Get user role from stored auth token
 */
export const getUserRole = () => {
  const token = localStorage.getItem('authToken');
  if (!token) return null;
  
  const payload = decodeJWT(token);
  return payload?.role || null;
};

/**
 * Get user ID from stored auth token
 */
export const getUserId = () => {
  const token = localStorage.getItem('authToken');
  if (!token) return null;
  
  const payload = decodeJWT(token);
  return payload?.sub || null;
};

/**
 * Check if user has specific role
 */
export const hasRole = (requiredRole) => {
  const userRole = getUserRole();
  return userRole === requiredRole;
};

/**
 * Check if user has any of the specified roles
 */
export const hasAnyRole = (roles) => {
  const userRole = getUserRole();
  return roles.includes(userRole);
};

/**
 * Get dashboard route based on user role
 */
export const getDashboardRoute = () => {
  const role = getUserRole();
  switch (role) {
    case 'citizen':
      return '/dashboard/citizen';
    case 'authority':
      return '/dashboard/authority';
    case 'analyst':
      return '/dashboard/analyst';
    default:
      return '/dashboard/citizen'; // Default fallback
  }
};

/**
 * Check if token is expired (basic check)
 */
export const isTokenExpired = () => {
  const token = localStorage.getItem('authToken');
  if (!token) return true;
  
  const payload = decodeJWT(token);
  if (!payload?.exp) return true;
  
  return Date.now() >= payload.exp * 1000;
};
