import React, { useState, useEffect } from 'react';
import { 
  Shield, AlertTriangle, CheckCircle, Clock, MapPin, Users, MessageSquare, 
  BarChart3, Eye, UserCheck, X, Plus, Search, Filter, Grid, List, 
  Calendar, Edit, Trash2, User, Bell, Settings, TrendingUp,
  FileText, Activity, Award, Target
} from 'lucide-react';
import api from '../../utils/api';
import { getUserRole, getUserId } from '../../utils/auth';
import { useNavigate } from 'react-router-dom';
import TimelineModal from './TimelineModal';
import AnnouncementModal from './AnnouncementModal';
import ProfileModal from './ProfileModal';

const AuthorityDashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  const [stats, setStats] = useState({
    totalIssues: 25,
    resolved: 4,
    inProgress: 6,
    pending: 3
  });
  
  const [reports, setReports] = useState([]);
  const [userInfo, setUserInfo] = useState({
    name: 'Loading...',
    email: 'Loading...',
    role: 'authority'
  });
  const [selectedReport, setSelectedReport] = useState(null);
  const [showTimelineModal, setShowTimelineModal] = useState(false);
  const [showAnnouncementModal, setShowAnnouncementModal] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);

  // Mock data for development - Ocean Hazards
  const mockReports = [
    {
      id: 1,
      title: 'High Waves and Coastal Flooding Alert',
      description: 'Dangerous wave conditions reported near Marina Beach with potential flooding risk to coastal areas',
      category: 'Ocean Safety',
      priority: 'High',
      status: 'under_verification',
      location: 'Marina Beach, Chennai Coastal Area',
      reportedBy: 'Coastal Patrol Officer',
      reportedAt: '2025-09-25T14:13:46Z',
      image: '/api/placeholder/300/200',
      department: 'Marine Safety',
      hazardType: 'High Waves / Swell'
    },
    {
      id: 2,
      title: 'Tsunami Warning - Immediate Evacuation Required',
      description: 'Seismic activity detected in Indian Ocean, potential tsunami threat to eastern coastline',
      category: 'Emergency Alert',
      priority: 'Critical',
      status: 'under_verification',
      location: 'Visakhapatnam Coastal District',
      reportedBy: 'Seismic Monitoring Station',
      reportedAt: '2025-09-24T10:30:00Z',
      image: '/api/placeholder/300/200',
      department: 'Disaster Management',
      hazardType: 'Tsunami'
    },
    {
      id: 3,
      title: 'Marine Pollution and Oil Spill Detected',
      description: 'Large oil spill reported 15 nautical miles off Mumbai coast, affecting marine ecosystem',
      category: 'Environmental Hazard',
      priority: 'High',
      status: 'verified',
      location: 'Mumbai Offshore Waters',
      reportedBy: 'Coast Guard Patrol',
      reportedAt: '2025-09-23T16:45:00Z',
      image: '/api/placeholder/300/200',
      department: 'Environmental Protection',
      hazardType: 'Marine Debris / Pollution'
    },
    {
      id: 4,
      title: 'Dangerous Rip Current Activity',
      description: 'Strong rip currents observed at popular swimming areas, multiple rescue operations conducted',
      category: 'Water Safety',
      priority: 'Medium',
      status: 'rejected',
      location: 'Goa Beaches - Calangute and Baga',
      reportedBy: 'Lifeguard Team',
      reportedAt: '2025-09-22T09:15:00Z',
      image: '/api/placeholder/300/200',
      department: 'Beach Safety',
      hazardType: 'Rip Current'
    },
    {
      id: 5,
      title: 'Coastal Erosion Threatening Infrastructure',
      description: 'Severe coastal erosion observed near residential areas, immediate assessment required',
      category: 'Coastal Management',
      priority: 'Medium',
      status: 'under_verification',
      location: 'Puducherry Coastal Highway',
      reportedBy: 'Local Resident',
      reportedAt: '2025-09-21T18:30:00Z',
      image: '/api/placeholder/300/200',
      department: 'Coastal Engineering',
      hazardType: 'Coastal Erosion'
    }
  ];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch user information
      const userId = getUserId();
      if (userId) {
        try {
          const userResponse = await api.get(`/users/${userId}`);
          if (userResponse.data) {
            setUserInfo({
              name: userResponse.data.name || userResponse.data.username || 'Authority User',
              email: userResponse.data.email || 'authority@pravaah.com',
              role: userResponse.data.role || 'authority'
            });
          }
        } catch (userError) {
          console.error('Error fetching user data:', userError);
          // Use fallback user data
          setUserInfo({
            name: 'Authority User',
            email: 'authority@pravaah.com',
            role: 'authority'
          });
        }
      }
      
      // Try to fetch real data
      const reportsResponse = await api.get('/reports');
      const allReports = reportsResponse.data || [];
      
      // Calculate stats
      const totalIssues = allReports.length;
      const verified = allReports.filter(r => r.status === 'verified').length;
      const underVerification = allReports.filter(r => r.status === 'under_verification').length;
      const rejected = allReports.filter(r => r.status === 'rejected').length;
      
      setReports(allReports);
      setStats({ totalIssues, verified, underVerification, rejected });
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Use mock data on error
      setReports(mockReports);
      setStats({ 
        totalIssues: mockReports.length, 
        verified: mockReports.filter(r => r.status === 'verified').length,
        underVerification: mockReports.filter(r => r.status === 'under_verification').length,
        rejected: mockReports.filter(r => r.status === 'rejected').length
      });
      setUserInfo({
        name: 'Authority User',
        email: 'authority@pravaah.com',
        role: 'authority'
      });
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'verified': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'under_verification': return 'bg-yellow-100 text-yellow-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleReportAction = async (reportId, action) => {
    try {
      console.log(`${action} report ${reportId}`);
      
      if (action === 'verify') {
        // Update report status to verified
        setReports(reports.map(r => 
          r.id === reportId ? { ...r, status: 'verified' } : r
        ));
        
        // TODO: Make API call to backend
        // await api.post(`/reports/${reportId}/verify`);
        
      } else if (action === 'reject') {
        // Update report status to rejected
        setReports(reports.map(r => 
          r.id === reportId ? { ...r, status: 'rejected' } : r
        ));
        
        // TODO: Make API call to backend
        // await api.post(`/reports/${reportId}/reject`);
        
      } else if (action === 'delete') {
        setReports(reports.filter(r => r.id !== reportId));
      }
    } catch (error) {
      console.error(`Error ${action} report:`, error);
    }
  };

  const openTimelineModal = (report) => {
    setSelectedReport(report);
    setShowTimelineModal(true);
  };

  const handleLogout = async () => {
    try {
      console.log('Logging out...');
      
      // Clear all authentication data
      localStorage.clear(); // This clears all localStorage data
      
      // Alternative: Clear specific items if you want to preserve other data
      // localStorage.removeItem('authToken');
      // localStorage.removeItem('userRole');
      // localStorage.removeItem('userId');
      
      // Small delay to ensure localStorage is cleared
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Navigate to the root path which should redirect to auth
      window.location.href = '/';
      
    } catch (error) {
      console.error('Error during logout:', error);
      // Force reload as fallback
      window.location.reload();
    }
  };

  const filteredReports = reports.filter(report => {
    const matchesSearch = report.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.location?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || report.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Authority Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* CivicEye-style Navbar */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Left side - Logo and Brand */}
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                  <Shield className="w-5 h-5 text-white" />
                </div>
                <div className="text-left">
                  <h1 className="text-xl font-bold text-blue-600 text-left">Pravaah</h1>
                  <p className="text-xs text-gray-500 text-left">Building Better Communities</p>
                </div>
              </div>
            </div>

            {/* Right side - User info and actions */}
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="text-sm text-gray-700 font-medium">{userInfo.name}</div>
                <div className="text-xs text-gray-500">{userInfo.email}</div>
              </div>
              
              
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
                {userInfo.name.charAt(0).toUpperCase()}
              </div>
              
              <button className="text-gray-500 hover:text-gray-700">
                <Bell className="w-5 h-5" />
              </button>
              
              <button 
                onClick={() => setShowProfileModal(true)}
                className="text-gray-500 hover:text-gray-700"
              >
                <User className="w-5 h-5" />
              </button>
              
              <button className="text-gray-500 hover:text-gray-700">
                <Settings className="w-5 h-5" />
              </button>
              
              <button 
                onClick={handleLogout}
                className="text-gray-500 hover:text-gray-700 text-sm hover:text-red-600 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-start">
              <div className="text-left">
                <h1 className="text-2xl font-bold text-gray-900 text-left">Admin Dashboard</h1>
                <p className="text-gray-600 text-left">Monitor, manage, and resolve community issues efficiently.</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button 
                onClick={() => setShowAnnouncementModal(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
              >
                <Plus className="w-4 h-4 mr-2" />
                Create Announcement
              </button>
              <button className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors flex items-center">
                <Users className="w-4 h-4 mr-2" />
                Manage Announcements
              </button>
              <button 
                onClick={() => setShowProfileModal(true)}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors flex items-center"
              >
                <User className="w-4 h-4 mr-2" />
                Profile
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="container mx-auto px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Ocean Reports</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalIssues}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <div className="mt-2">
              <TrendingUp className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">Ocean hazard monitoring</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Verified Reports</p>
                <p className="text-3xl font-bold text-gray-900">{stats.verified || 0}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="mt-2">
              <CheckCircle className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">Confirmed hazards</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Under Review</p>
                <p className="text-3xl font-bold text-gray-900">{stats.underVerification || 0}</p>
              </div>
              <div className="bg-yellow-100 p-3 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
            </div>
            <div className="mt-2">
              <Clock className="w-4 h-4 text-yellow-500 inline mr-1" />
              <span className="text-sm text-yellow-600">Awaiting verification</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Rejected Reports</p>
                <p className="text-3xl font-bold text-gray-900">{stats.rejected || 0}</p>
              </div>
              <div className="bg-red-100 p-3 rounded-lg">
                <X className="w-6 h-6 text-red-600" />
              </div>
            </div>
            <div className="mt-2">
              <X className="w-4 h-4 text-red-500 inline mr-1" />
              <span className="text-sm text-red-600">False alarms</span>
            </div>
          </div>
        </div>

        {/* Search and Filter Bar */}
        <div className="bg-white rounded-xl shadow-sm border p-4 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search issues, locations, departments..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-80"
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <Filter className="w-5 h-5 text-gray-400" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">All Status</option>
                  <option value="under_verification">Under Verification</option>
                  <option value="verified">Verified</option>
                  <option value="rejected">Rejected</option>
                  <option value="in_progress">In Progress</option>
                </select>
              </div>
              
              <div className="flex items-center bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded-md transition-colors ${
                    viewMode === 'grid' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded-md transition-colors ${
                    viewMode === 'list' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Reports Grid */}
        <div className={`grid gap-6 mb-8 ${
          viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'
        }`}>
          {filteredReports.map((report) => (
            <div key={report.id} className="bg-white rounded-xl shadow-sm border hover:shadow-md transition-shadow">
              {/* Report Image */}
              <div className="relative h-48 bg-gray-200 rounded-t-xl overflow-hidden">
                <img 
                  src={report.image || '/api/placeholder/300/200'} 
                  alt={report.title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-4 left-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${
                    getPriorityColor(report.priority)
                  }`}>
                    {report.priority || 'Medium'}
                  </span>
                </div>
                <div className="absolute top-4 right-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    getStatusColor(report.status)
                  }`}>
                    {report.status?.replace('_', ' ').toUpperCase() || 'PENDING'}
                  </span>
                </div>
              </div>
              
              {/* Report Content */}
              <div className="p-6">
                <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{report.title}</h3>
                
                <div className="flex items-center text-sm text-gray-500 mb-3">
                  <div className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs mr-2">
                    {report.category || report.department}
                  </div>
                  {report.hazardType && (
                    <div className="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs">
                      {report.hazardType}
                    </div>
                  )}
                </div>
                
                <div className="flex items-center text-sm text-gray-500 mb-4">
                  <MapPin className="w-4 h-4 mr-1" />
                  <span className="truncate">{report.location}</span>
                </div>
                
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>Reported: {new Date(report.reportedAt || report.created_at).toLocaleDateString()}</span>
                  <span className="flex items-center">
                    <User className="w-3 h-3 mr-1" />
                    {report.reportedBy}
                  </span>
                </div>
                
                {/* Action Buttons */}
                <div className="pt-4 border-t space-y-3">
                  {/* Primary Actions - Verify/Reject */}
                  {report.status === 'under_verification' && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => handleReportAction(report.id, 'verify')}
                        className="flex-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center"
                      >
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Verify
                      </button>
                      <button
                        onClick={() => handleReportAction(report.id, 'reject')}
                        className="flex-1 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center"
                      >
                        <X className="w-4 h-4 mr-2" />
                        Reject
                      </button>
                    </div>
                  )}
                  
                  {/* Status Display for Verified/Rejected Reports */}
                  {(report.status === 'verified' || report.status === 'rejected') && (
                    <div className="text-center py-2">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                        report.status === 'verified' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {report.status === 'verified' ? (
                          <>
                            <CheckCircle className="w-4 h-4 mr-1" />
                            Verified Report
                          </>
                        ) : (
                          <>
                            <X className="w-4 h-4 mr-1" />
                            Rejected Report
                          </>
                        )}
                      </span>
                    </div>
                  )}
                  
                  {/* Secondary Actions */}
                  <div className="flex items-center justify-center space-x-4">
                    <button
                      onClick={() => setSelectedReport(report)}
                      className="flex items-center text-gray-600 hover:text-blue-600 transition-colors"
                      title="View Details"
                    >
                      <Eye className="w-4 h-4 mr-1" />
                      <span className="text-sm">View</span>
                    </button>
                    <button
                      onClick={() => openTimelineModal(report)}
                      className="flex items-center text-gray-600 hover:text-blue-600 transition-colors"
                      title="Timeline"
                    >
                      <Clock className="w-4 h-4 mr-1" />
                      <span className="text-sm">Timeline</span>
                    </button>
                    <button
                      className="flex items-center text-gray-600 hover:text-blue-600 transition-colors"
                      title="Assign"
                    >
                      <UserCheck className="w-4 h-4 mr-1" />
                      <span className="text-sm">Assign</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Timeline Modal */}
      {showTimelineModal && selectedReport && (
        <TimelineModal 
          report={selectedReport} 
          onClose={() => setShowTimelineModal(false)} 
        />
      )}

      {/* Announcement Modal */}
      {showAnnouncementModal && (
        <AnnouncementModal 
          onClose={() => setShowAnnouncementModal(false)} 
        />
      )}

      {/* Profile Modal */}
      {showProfileModal && (
        <ProfileModal 
          onClose={() => setShowProfileModal(false)} 
        />
      )}
    </div>
  );
};

export default AuthorityDashboard;
