import React, { useState } from 'react';
import { MessageSquare, MapPin, Calendar, X } from 'lucide-react';

const AnnouncementModal = ({ onClose }) => {
  const [formData, setFormData] = useState({
    title: '',
    category: 'General',
    priority: 'Medium',
    description: '',
    locationName: '',
    pincode: '',
    scheduledDate: '',
    expiryDate: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Creating announcement:', formData);
    // Here you would make an API call to create the announcement
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="text-center w-full">
            <div className="bg-blue-600 p-3 rounded-lg inline-block mb-4">
              <MessageSquare className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-blue-600">Create Announcement</h2>
            <p className="text-gray-600 mt-2">Broadcast important information to citizens and keep your community informed with professional announcements</p>
          </div>
          <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information */}
          <div className="bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-4 rounded-lg">
            <h3 className="font-semibold flex items-center">
              <MessageSquare className="w-5 h-5 mr-2" />
              Basic Information
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Notice Title *</label>
              <input
                type="text"
                placeholder="e.g. Water Supply Disruption"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Priority *</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({...formData, priority: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
          </div>


          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Description *</label>
            <textarea
              placeholder="Provide detailed information about the announcement..."
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          {/* Location Information */}
          <div className="bg-gradient-to-r from-blue-500 to-purple-500 text-white p-4 rounded-lg">
            <h3 className="font-semibold flex items-center">
              <MapPin className="w-5 h-5 mr-2" />
              Location Information
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Location Name *</label>
              <input
                type="text"
                placeholder="e.g. Sector 21, Bangalore"
                value={formData.locationName}
                onChange={(e) => setFormData({...formData, locationName: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Pincode *</label>
              <input
                type="text"
                placeholder="560021"
                value={formData.pincode}
                onChange={(e) => setFormData({...formData, pincode: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
              <p className="text-xs text-gray-500 mt-1">6-digit Indian pincode</p>
            </div>
          </div>

          {/* Schedule Information */}
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4 rounded-lg">
            <h3 className="font-semibold flex items-center">
              <Calendar className="w-5 h-5 mr-2" />
              Schedule Information (Optional)
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Scheduled Date & Time</label>
              <input
                type="datetime-local"
                value={formData.scheduledDate}
                onChange={(e) => setFormData({...formData, scheduledDate: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">When this announcement applies</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Expiry Date & Time</label>
              <input
                type="datetime-local"
                value={formData.expiryDate}
                onChange={(e) => setFormData({...formData, expiryDate: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">When this announcement expires</p>
            </div>
          </div>

          <div className="flex justify-between pt-6 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center"
            >
              <MessageSquare className="w-4 h-4 mr-2" />
              Create Announcement
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AnnouncementModal;
