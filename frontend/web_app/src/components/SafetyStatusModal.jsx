import React, { useState } from 'react';
import { Shield, AlertTriangle, MapPin } from 'lucide-react';

const SafetyStatusModal = ({ isOpen, onClose, notification, onStatusUpdate }) => {
  const [selectedStatus, setSelectedStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState(null);

  // Get current location when modal opens
  React.useEffect(() => {
    if (isOpen && !location) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          // Use default location or show error
          setLocation({ latitude: 12.9716, longitude: 77.5946 }); // Bangalore
        }
      );
    }
  }, [isOpen]);

  const handleStatusSubmit = async (isSafe) => {
    if (!location) {
      alert('Unable to get your location. Please enable location services.');
      return;
    }

    setLoading(true);
    try {
      const statusData = {
        report_id: notification.id,
        is_safe: isSafe,
        latitude: location.latitude,
        longitude: location.longitude,
        message: `User reported they are ${isSafe ? 'safe' : 'not safe'} in response to ${notification.hazardName}`
      };

      // Call API to update safety status
      const response = await fetch('/api/notifications/safety-status', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify(statusData)
      });

      if (response.ok) {
        const result = await response.json();
        onStatusUpdate && onStatusUpdate(result);
        
        // Show success message
        alert(`Thank you! You've been marked as ${isSafe ? 'Safe' : 'Not Safe'}. ${isSafe ? 'A green safety zone' : 'A danger zone'} has been created around your location.`);
        
        onClose();
      } else {
        throw new Error('Failed to update safety status');
      }
    } catch (error) {
      console.error('Error updating safety status:', error);
      alert('Failed to update your safety status. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="text-center mb-6">
          <AlertTriangle className="w-12 h-12 text-orange-500 mx-auto mb-3" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Safety Status Check
          </h2>
          <p className="text-gray-600">
            A <strong>{notification?.hazardName}</strong> has been reported in your area. 
            Are you safe?
          </p>
        </div>

        <div className="space-y-3 mb-6">
          <button
            onClick={() => handleStatusSubmit(true)}
            disabled={loading}
            className="w-full flex items-center justify-center px-4 py-3 bg-green-100 hover:bg-green-200 text-green-800 font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <Shield className="w-5 h-5 mr-2" />
            I'm Safe
            <span className="ml-2 text-xs">(Creates Green Zone)</span>
          </button>
          
          <button
            onClick={() => handleStatusSubmit(false)}
            disabled={loading}
            className="w-full flex items-center justify-center px-4 py-3 bg-purple-100 hover:bg-purple-200 text-purple-800 font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            <AlertTriangle className="w-5 h-5 mr-2" />
            I'm Not Safe
            <span className="ml-2 text-xs">(Creates Danger Zone)</span>
          </button>
        </div>

        {location && (
          <div className="flex items-center justify-center text-xs text-gray-500 mb-4">
            <MapPin className="w-3 h-3 mr-1" />
            Location: {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
          </div>
        )}

        <div className="flex space-x-3">
          <button
            onClick={onClose}
            disabled={loading}
            className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 disabled:opacity-50"
          >
            Maybe Later
          </button>
        </div>

        {loading && (
          <div className="mt-4 text-center text-sm text-gray-500">
            Updating your safety status...
          </div>
        )}
      </div>
    </div>
  );
};

export default SafetyStatusModal;