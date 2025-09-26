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

  // Mock data for development
  const mockReports = [
    {
      id: 1,
      title: 'Severe Illegal Dumping and Road Contamination',
      description: 'Large amounts of waste dumped on coastal road causing environmental hazard',
      category: 'Sanitation',
      priority: 'Low',
      status: 'pending',
      location: 'Sarjapur, Iyya Nagar, Bengaluru South City Corporation',
      reportedBy: 'Citizen Reporter',
      reportedAt: '2025-09-25T14:13:46Z',
      image: '/api/placeholder/300/200',
      department: 'Sanitation'
    },
    {
      id: 2,
      title: 'Illegal Dumping and Collapsed Infrastructure',
      description: 'Waste accumulation near residential area with damaged infrastructure',
      category: 'Health & Safety',
      priority: 'Critical',
      status: 'in_progress',
      location: 'Sandeep Vihar AWHO Apartments, Uttarahalli',
      reportedBy: 'Community Member',
      reportedAt: '2025-09-24T10:30:00Z',
      image: '/api/placeholder/300/200',
      department: 'Public Works'
    },
    {
      id: 3,
      title: 'Severe Illegal Dumping and Infrastructure Damage',
      description: 'Critical waste management issue affecting local infrastructure',
      category: 'Sanitation',
      priority: 'High',
      status: 'resolved',
      location: 'Sandeep Vihar AWHO Apartments, Uttarahalli',
      reportedBy: 'Local Authority',
      reportedAt: '2025-09-23T16:45:00Z',
      image: '/api/placeholder/300/200',
      department: 'Environment'
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
      const resolved = allReports.filter(r => r.status === 'resolved').length;
      const inProgress = allReports.filter(r => r.status === 'in_progress').length;
      const pending = allReports.filter(r => r.status === 'pending').length;
      
      setReports(allReports);
      setStats({ totalIssues, resolved, inProgress, pending });
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      // Use mock data on error
      setReports(mockReports);
      setStats({ totalIssues: 25, resolved: 4, inProgress: 6, pending: 3 });
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
      case 'resolved': return 'bg-green-100 text-green-800';
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleReportAction = async (reportId, action) => {
    try {
      console.log(`${action} report ${reportId}`);
      
      if (action === 'delete') {
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
                <p className="text-sm font-medium text-gray-600">Total Issues</p>
                <p className="text-3xl font-bold text-gray-900">{stats.totalIssues}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <div className="mt-2">
              <TrendingUp className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">+12% from last month</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Resolved</p>
                <p className="text-3xl font-bold text-gray-900">{stats.resolved}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="mt-2">
              <TrendingUp className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">+8% efficiency</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">In Progress</p>
                <p className="text-3xl font-bold text-gray-900">{stats.inProgress}</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <Activity className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <div className="mt-2">
              <Clock className="w-4 h-4 text-yellow-500 inline mr-1" />
              <span className="text-sm text-yellow-600">Avg 2.3 days</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-3xl font-bold text-gray-900">{stats.pending}</p>
              </div>
              <div className="bg-orange-100 p-3 rounded-lg">
                <Clock className="w-6 h-6 text-orange-600" />
              </div>
            </div>
            <div className="mt-2">
              <AlertTriangle className="w-4 h-4 text-orange-500 inline mr-1" />
              <span className="text-sm text-orange-600">Needs attention</span>
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
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
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
                  <div className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs mr-3">
                    {report.category || report.department}
                  </div>
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
                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => setSelectedReport(report)}
                      className="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
                      title="View Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => openTimelineModal(report)}
                      className="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
                      title="Timeline"
                    >
                      <Clock className="w-4 h-4" />
                    </button>
                    <button
                      className="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
                      title="Assign"
                    >
                      <UserCheck className="w-4 h-4" />
                    </button>
                    <button
                      className="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
                      title="Edit"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleReportAction(report.id, 'delete')}
                      className="flex items-center text-red-600 hover:text-red-800 transition-colors"
                      title="Remove"
                    >
                      <Trash2 className="w-4 h-4" />
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
