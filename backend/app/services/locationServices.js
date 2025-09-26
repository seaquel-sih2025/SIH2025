// frontend/web_app/src/services/locationService.js

/**
 * Service for handling user location updates and geolocation
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Get current user location
 * @returns {Promise<Object>} Location object with latitude, longitude, accuracy
 */
export const getCurrentLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation is not supported by this browser.'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          timestamp: new Date().toISOString()
        });
      },
      (error) => {
        let errorMessage = 'Unable to get your location.';
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location access denied by user. Please enable location access in your browser settings.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information is unavailable. Please check your device settings.';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timed out. Please try again.';
            break;
        }
        
        reject(new Error(errorMessage));
      },
      {
        enableHighAccuracy: true,
        timeout: 15000, // 15 seconds
        maximumAge: 300000 // 5 minutes
      }
    );
  });
};

/**
 * Update user location on the server
 * @param {Object} location - Location object with latitude, longitude
 * @returns {Promise<Object>} Server response
 */
export const updateUserLocation = async (location) => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/user/location`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        latitude: location.latitude,
        longitude: location.longitude,
        accuracy: location.accuracy
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating user location:', error);
    throw error;
  }
};

/**
 * Get user's stored location from server
 * @returns {Promise<Object>} User location data
 */
export const getUserLocation = async () => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_BASE_URL}/api/user/location`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching user location:', error);
    throw error;
  }
};

/**
 * Start watching user location and update server periodically
 * @param {Function} onLocationUpdate - Callback for location updates
 * @param {number} updateInterval - Update interval in milliseconds (default: 5 minutes)
 * @returns {number} Watch ID for stopping location watching
 */
export const startLocationWatching = (onLocationUpdate, updateInterval = 5 * 60 * 1000) => {
  let lastUpdateTime = 0;
  
  const watchId = navigator.geolocation.watchPosition(
    async (position) => {
      const now = Date.now();
      
      // Only update if enough time has passed or location has changed significantly
      if (now - lastUpdateTime < updateInterval) {
        return;
      }

      const location = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        timestamp: new Date().toISOString()
      };

      try {
        await updateUserLocation(location);
        lastUpdateTime = now;
        
        if (onLocationUpdate) {
          onLocationUpdate(location);
        }
        
        console.log('Location updated:', location);
      } catch (error) {
        console.error('Failed to update location on server:', error);
      }
    },
    (error) => {
      console.error('Location watching error:', error);
    },
    {
      enableHighAccuracy: false, // Use less accurate but more battery-friendly location
      timeout: 30000, // 30 seconds
      maximumAge: 600000 // 10 minutes
    }
  );

  return watchId;
};

/**
 * Stop watching user location
 * @param {number} watchId - Watch ID returned by startLocationWatching
 */
export const stopLocationWatching = (watchId) => {
  if (watchId) {
    navigator.geolocation.clearWatch(watchId);
  }
};

/**
 * Request location permission
 * @returns {Promise<string>} Permission status
 */
export const requestLocationPermission = async () => {
  try {
    const permission = await navigator.permissions.query({ name: 'geolocation' });
    return permission.state;
  } catch (error) {
    console.error('Error checking location permission:', error);
    return 'unknown';
  }
};

/**
 * Calculate distance between two coordinates in kilometers
 * @param {number} lat1 - First latitude
 * @param {number} lon1 - First longitude  
 * @param {number} lat2 - Second latitude
 * @param {number} lon2 - Second longitude
 * @returns {number} Distance in kilometers
 */
export const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Earth's radius in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
};

/**
 * Format distance for display
 * @param {number} distanceKm - Distance in kilometers
 * @returns {string} Formatted distance string
 */
export const formatDistance = (distanceKm) => {
  if (distanceKm < 1) {
    return `${Math.round(distanceKm * 1000)}m away`;
  } else if (distanceKm < 10) {
    return `${distanceKm.toFixed(1)}km away`;
  } else {
    return `${Math.round(distanceKm)}km away`;
  }
};