import React, { useState } from 'react';
import { User, X, Mail, Phone, MapPin, Edit, Activity, Award, Shield, Calendar, Clock } from 'lucide-react';

const ProfileModal = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState('profile');
  
  // Mock user data
  const userData = {
    name: 'Authority User',
    role: 'Administrator',
    email: 'authority@pravaah.com',
    phone: '+91-9876543210',
    department: 'Public Administration',
    avatar: 'A',
    joinDate: '2024-01-15',
    lastLogin: '2025-09-26T10:30:00Z'
  };

  const handledIssues = [
    {
      id: 1,
      title: 'Messy Utility Cables',
      status: 'Pending',
      reportedBy: 'N/A',
      description: 'The image shows a utility pole with a significant amount of exposed and tangled cables. This poses a safety hazard to residents due to the potential for electrical shock or fire. The disorganized cables also create a visual blight in the neighborhood, diminishing the aesthetic appeal of the residential area. The jumbled wires indicate poor maintenance and repair work, potentially causing delays in service restoration if problems arise. The issue requires attention from the relevant utility companies to reorganize and secure the cables in a safe and orderly manner.',
      priority: 'Medium'
    }
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center text-white text-2xl font-bold mr-4">
                <Shield className="w-8 h-8" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">Administrator Profile</h2>
                <p className="text-blue-100">Manage your profile and track your activities</p>
              </div>
            </div>
            <button onClick={onClose} className="text-white hover:text-gray-200 transition-colors">
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        <div className="flex flex-1 min-h-0">
          {/* Left Sidebar */}
          <div className="w-1/3 bg-gray-50 p-6 border-r overflow-y-auto">
            {/* Profile Info */}
            <div className="text-center mb-6">
              <div className="w-24 h-24 bg-blue-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4 shadow-lg">
                {userData.avatar}
              </div>
              <h3 className="text-xl font-semibold text-gray-900">{userData.name}</h3>
              <p className="text-blue-600 text-sm font-medium">{userData.role}</p>
              <button className="text-blue-600 text-sm hover:text-blue-700 mt-3 flex items-center mx-auto bg-blue-50 px-3 py-1 rounded-full">
                <Edit className="w-4 h-4 mr-1" />
                Edit Profile
              </button>
            </div>

            {/* Contact Info */}
            <div className="space-y-3">
              <div className="bg-white p-2.5 rounded-lg border">
                <label className="block text-xs font-medium text-gray-500 mb-1">Full Name</label>
                <div className="flex items-center text-gray-900">
                  <User className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-sm">{userData.name}</span>
                </div>
              </div>
              
              <div className="bg-white p-2.5 rounded-lg border">
                <label className="block text-xs font-medium text-gray-500 mb-1">Email</label>
                <div className="flex items-center text-gray-900">
                  <Mail className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-sm">{userData.email}</span>
                </div>
              </div>
              
              <div className="bg-white p-2.5 rounded-lg border">
                <label className="block text-xs font-medium text-gray-500 mb-1">Phone</label>
                <div className="flex items-center text-gray-900">
                  <Phone className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-sm">{userData.phone}</span>
                </div>
              </div>
              
              <div className="bg-white p-2.5 rounded-lg border">
                <label className="block text-xs font-medium text-gray-500 mb-1">Department</label>
                <div className="flex items-center text-gray-900">
                  <MapPin className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-sm">{userData.department}</span>
                </div>
              </div>

              <div className="bg-white p-2.5 rounded-lg border">
                <label className="block text-xs font-medium text-gray-500 mb-1">Join Date</label>
                <div className="flex items-center text-gray-900">
                  <Calendar className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-sm">{new Date(userData.joinDate).toLocaleDateString()}</span>
                </div>
              </div>

              <div className="bg-white p-2.5 rounded-lg border">
                <label className="block text-xs font-medium text-gray-500 mb-1">Last Login</label>
                <div className="flex items-center text-gray-900">
                  <Clock className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-sm">{new Date(userData.lastLogin).toLocaleString()}</span>
                </div>
              </div>
            </div>

            {/* Activity Snapshot */}
            <div className="mt-6">
              <h4 className="font-medium text-gray-900 mb-4 flex items-center">
                <Activity className="w-4 h-4 mr-2 text-blue-600" />
                Activity Snapshot
              </h4>
              <div className="bg-white rounded-lg border p-4">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                      <Award className="w-5 h-5 text-green-600" />
                    </div>
                    <div className="text-xl font-bold text-gray-900">15</div>
                    <div className="text-xs text-gray-600">Resolved</div>
                  </div>
                  <div>
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                      <Activity className="w-5 h-5 text-blue-600" />
                    </div>
                    <div className="text-xl font-bold text-gray-900">8</div>
                    <div className="text-xs text-gray-600">In Progress</div>
                  </div>
                  <div>
                    <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-2">
                      <Clock className="w-5 h-5 text-orange-600" />
                    </div>
                    <div className="text-xl font-bold text-gray-900">3</div>
                    <div className="text-xs text-gray-600">Pending</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Content */}
          <div className="flex-1 p-6 overflow-y-auto bg-gray-50 min-h-0">
            <div className="mb-6">
              <div className="flex items-start justify-between mb-4">
                <div className="text-left">
                  <h3 className="text-xl font-semibold text-gray-900 text-left">Handled Issues Log</h3>
                  <p className="text-gray-600 text-left">Search and filter through all issues you've managed</p>
                </div>
                <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                  26 Total Issues
                </div>
              </div>
              
              {/* Search Bar */}
              <div className="mb-4">
                <input
                  type="text"
                  placeholder="Search by title or citizen name..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                />
              </div>

              {/* Filter Tabs */}
              <div className="flex space-x-1 mb-6 bg-white p-1 rounded-lg shadow-sm border">
                {['All', 'Resolved', 'In Progress', 'Pending', 'Rejected'].map((tab) => (
                  <button
                    key={tab}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                      tab === 'All' 
                        ? 'bg-blue-600 text-white shadow-sm' 
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            {/* Issues List */}
            <div className="space-y-4">
              {handledIssues.map((issue) => (
                <div key={issue.id} className="bg-white border rounded-lg p-5 hover:shadow-md transition-all duration-200">
                  <div className="flex items-start justify-between mb-3">
                    <h4 className="font-semibold text-gray-900 text-lg">{issue.title}</h4>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      issue.status === 'Pending' ? 'bg-orange-100 text-orange-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {issue.status}
                    </span>
                  </div>
                  
                  <div className="text-sm text-gray-500 mb-3 flex items-center">
                    <User className="w-4 h-4 mr-1" />
                    Reported by: {issue.reportedBy}
                  </div>
                  
                  <p className="text-gray-700 text-sm leading-relaxed mb-4 line-clamp-3">
                    {issue.description}
                  </p>
                  
                  <div className="flex items-center justify-between pt-3 border-t">
                    <div className="flex items-center space-x-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        issue.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {issue.priority} Priority
                      </span>
                      <span className="text-xs text-gray-500">
                        <Calendar className="w-3 h-3 inline mr-1" />
                        Sep 26, 2025
                      </span>
                    </div>
                    <button className="text-blue-600 hover:text-blue-700 text-sm font-medium bg-blue-50 px-3 py-1 rounded-lg hover:bg-blue-100 transition-colors">
                      View Details
                    </button>
                  </div>
                </div>
              ))}
              
              {/* Load More Button */}
              <div className="text-center pt-4">
                <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  Load More Issues
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileModal;
