import React, { useState, useEffect } from 'react';
import { 
  Shield, AlertTriangle, CheckCircle, Clock, MapPin, Users, MessageSquare, 
  BarChart3, Eye, UserCheck, X, Plus, Search, Filter, Grid, List, 
  Calendar, Edit, Trash2, User, Bell, Settings, TrendingUp,
  FileText, Activity, Award, Target, Send, Radio, Layers, Zap,
  Navigation, Phone, Truck, Building, Heart, Home, Route,
  ChevronDown, MoreVertical, RefreshCw, Gauge, AlertCircle,
  Map, Crosshair, Wifi, WifiOff, Volume2, VolumeX, Star,
  Flag, Timer, Database, Globe, Satellite, Radar
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
  const [activeTab, setActiveTab] = useState('triage-queue');
  const [viewMode, setViewMode] = useState('grid');
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  const [stats, setStats] = useState({
    totalIssues: 25,
    verified: 4,
    underVerification: 6,
    rejected: 3
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

  // New state for authority-specific features
  const [triageQueue, setTriageQueue] = useState([]);
  const [criticalInfrastructure, setCriticalInfrastructure] = useState([]);
  const [incidentChat, setIncidentChat] = useState([]);
  const [urgencyScores, setUrgencyScores] = useState([]);
  const [ewsComparison, setEwsComparison] = useState({});
  const [activeIncident, setActiveIncident] = useState(null);
  const [chatMessage, setChatMessage] = useState('');
  const [mapOverlays, setMapOverlays] = useState({
    infrastructure: true,
    hazardZones: true,
    assets: true,
    reports: true
  });

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
    loadAuthorityData();
  }, []);

  const loadAuthorityData = () => {
    // Mock Triage Queue Data
    setTriageQueue([
      {
        id: 'T001',
        title: 'Tsunami Warning - Multiple Reports',
        location: 'Chennai Coast',
        priority: 'Critical',
        urgencyScore: 95,
        reportCount: 12,
        lastUpdated: '2 min ago',
        status: 'under_verification',
        sentiment: 'panic',
        sources: ['Social Media', 'Citizen Reports', 'Coast Guard']
      },
      {
        id: 'T002', 
        title: 'High Waves at Marina Beach',
        location: 'Marina Beach, Chennai',
        priority: 'High',
        urgencyScore: 78,
        reportCount: 8,
        lastUpdated: '5 min ago',
        status: 'under_verification',
        sentiment: 'concern',
        sources: ['Citizen Reports', 'Lifeguard Station']
      },
      {
        id: 'T003',
        title: 'Coastal Erosion Report',
        location: 'Puducherry Highway',
        priority: 'Medium',
        urgencyScore: 45,
        reportCount: 3,
        lastUpdated: '15 min ago',
        status: 'under_verification',
        sentiment: 'calm',
        sources: ['Local Residents']
      }
    ]);

    // Mock Critical Infrastructure Data
    setCriticalInfrastructure([
      {
        id: 'CI001',
        name: 'Chennai General Hospital',
        type: 'Hospital',
        status: 'Operational',
        capacity: '85%',
        coordinates: [13.0827, 80.2707],
        contact: '+91-44-2819-3000',
        emergencyReady: true
      },
      {
        id: 'CI002',
        name: 'Marina Beach Evacuation Center',
        type: 'Shelter',
        status: 'Ready',
        capacity: '0%',
        coordinates: [13.0500, 80.2824],
        contact: '+91-44-2819-4000',
        emergencyReady: true
      },
      {
        id: 'CI003',
        name: 'Coast Guard Station',
        type: 'Emergency Services',
        status: 'Active',
        capacity: '100%',
        coordinates: [13.1000, 80.3000],
        contact: '+91-44-2819-5000',
        emergencyReady: true
      },
      {
        id: 'CI004',
        name: 'ECR Evacuation Route',
        type: 'Route',
        status: 'Clear',
        capacity: 'Open',
        coordinates: [13.0000, 80.2500],
        contact: 'Traffic Control',
        emergencyReady: true
      }
    ]);

    // Mock Incident Chat Data
    setIncidentChat([
      {
        id: 'MSG001',
        sender: 'Coast Guard Chennai',
        message: 'Tsunami alert confirmed. All units to standby positions.',
        timestamp: '10:45 AM',
        priority: 'high',
        incident: 'T001'
      },
      {
        id: 'MSG002',
        sender: 'District Collector',
        message: 'Evacuation centers are being prepared. ETA 15 minutes.',
        timestamp: '10:47 AM',
        priority: 'medium',
        incident: 'T001'
      },
      {
        id: 'MSG003',
        sender: 'Police Control Room',
        message: 'Traffic diversions in place on ECR. All clear.',
        timestamp: '10:50 AM',
        priority: 'low',
        incident: 'T001'
      }
    ]);

    // Mock EWS Comparison Data
    setEwsComparison({
      incoisPredicted: {
        area: '150 sq km',
        affectedPopulation: '50,000',
        riskLevel: 'High',
        warningTime: '10:30 AM'
      },
      crowdsourcedActual: {
        area: '180 sq km',
        affectedPopulation: '65,000',
        riskLevel: 'Critical',
        firstReportTime: '10:15 AM'
      },
      variance: {
        areaVariance: '+20%',
        populationVariance: '+30%',
        timeAdvantage: '15 minutes earlier'
      }
    });
  };

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
        
        // Update triage queue
        setTriageQueue(triageQueue.filter(t => t.id !== reportId));
        
        // TODO: Make API call to backend
        // await api.post(`/reports/${reportId}/verify`);
        
      } else if (action === 'reject') {
        // Update report status to rejected
        setReports(reports.map(r => 
          r.id === reportId ? { ...r, status: 'rejected' } : r
        ));
        
        // Update triage queue
        setTriageQueue(triageQueue.filter(t => t.id !== reportId));
        
        // TODO: Make API call to backend
        // await api.post(`/reports/${reportId}/reject`);
        
      } else if (action === 'delete') {
        setReports(reports.filter(r => r.id !== reportId));
      }
    } catch (error) {
      console.error(`Error ${action} report:`, error);
    }
  };

  // Authority-specific handlers
  const handleTriageAction = async (triageId, action, notes = '') => {
    try {
      const updatedQueue = triageQueue.map(item => {
        if (item.id === triageId) {
          return {
            ...item,
            status: action,
            auditTrail: [
              ...(item.auditTrail || []),
              {
                action,
                timestamp: new Date().toISOString(),
                user: userInfo.name,
                notes
              }
            ]
          };
        }
        return item;
      });
      
      setTriageQueue(updatedQueue);
      
      // TODO: API call to update triage status
      // await api.post(`/triage/${triageId}/${action}`, { notes });
      
    } catch (error) {
      console.error(`Error updating triage item:`, error);
    }
  };

  const handleSendMessage = async () => {
    if (!chatMessage.trim() || !activeIncident) return;
    
    const newMessage = {
      id: `MSG${Date.now()}`,
      sender: userInfo.name,
      message: chatMessage,
      timestamp: new Date().toLocaleTimeString(),
      priority: 'medium',
      incident: activeIncident
    };
    
    setIncidentChat([...incidentChat, newMessage]);
    setChatMessage('');
    
    // TODO: API call to send message
    // await api.post('/incident-chat', newMessage);
  };

  const toggleMapOverlay = (overlay) => {
    setMapOverlays(prev => ({
      ...prev,
      [overlay]: !prev[overlay]
    }));
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
      {/* Pravaah Navbar */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
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

            {/* Right side actions */}
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
                onClick={handleLogout}
                className="bg-gray-100 hover:bg-gray-200 text-gray-800 px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Sign Out
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

      {/* Performance Metrics */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Incidents</p>
                <p className="text-3xl font-bold text-gray-900">{triageQueue.length}</p>
              </div>
              <div className="bg-red-100 p-3 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
            </div>
            <div className="mt-2">
              <Timer className="w-4 h-4 text-orange-500 inline mr-1" />
              <span className="text-sm text-orange-600">Requires immediate attention</span>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Response Teams</p>
                <p className="text-3xl font-bold text-gray-900">{criticalInfrastructure.filter(ci => ci.type === 'Emergency Services').length}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <Truck className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <div className="mt-2">
              <CheckCircle className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">All units operational</span>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Critical Infrastructure</p>
                <p className="text-3xl font-bold text-gray-900">{criticalInfrastructure.length}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <Building className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="mt-2">
              <Shield className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">Systems operational</span>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p className="text-3xl font-bold text-gray-900">8.5m</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <Zap className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <div className="mt-2">
              <TrendingUp className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">15% improvement</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8">
            {[
                { id: 'triage-queue', name: 'Triage & Verification', icon: Shield },
                { id: 'golden-hour-map', name: 'Interactive Map', icon: Map },
              { id: 'incident-chat', name: 'Incident Communication', icon: MessageSquare },
              { id: 'urgency-filter', name: 'Urgency Dashboard', icon: Gauge },
              { id: 'ews-comparison', name: 'EWS Comparison', icon: Radar }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-red-500 text-red-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4 mr-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="space-y-8">
          {/* Triage Queue & Verification Tab */}
          {activeTab === 'triage-queue' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm border">
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                      <Shield className="w-5 h-5 mr-2" />
                      Triage Queue & Verification Workflow
                    </h2>
                    <div className="flex items-center space-x-2">
                      <button className="bg-red-100 hover:bg-red-200 text-red-700 px-3 py-1 rounded-lg text-sm transition-colors">
                        High Priority ({triageQueue.filter(t => t.priority === 'Critical' || t.priority === 'High').length})
                      </button>
                      <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-lg text-sm transition-colors">
                        <RefreshCw className="w-3 h-3 mr-1" />
                        Refresh
                      </button>
                    </div>
                  </div>
                  <p className="text-gray-600 mt-2">Review and verify unverified crowdsourced reports with complete audit trail.</p>
                </div>
                
                <div className="p-6">
                  <div className="space-y-4">
                    {triageQueue.map((item) => (
                      <div key={item.id} className={`bg-white rounded-lg border-l-4 shadow-sm hover:shadow-md transition-shadow ${
                        item.priority === 'Critical' ? 'border-red-500' :
                        item.priority === 'High' ? 'border-orange-500' :
                        'border-yellow-500'
                      }`}>
                        {/* Header with title and actions */}
                        <div className="p-4 border-b border-gray-100">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <h3 className="font-semibold text-gray-900 text-lg">{item.title}</h3>
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                item.priority === 'Critical' ? 'bg-red-100 text-red-800' :
                                item.priority === 'High' ? 'bg-orange-100 text-orange-800' :
                                'bg-yellow-100 text-yellow-800'
                              }`}>
                                {item.priority}
                              </span>
                              <div className="flex items-center bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-medium">
                                <Gauge className="w-3 h-3 mr-1" />
                                {item.urgencyScore}% Urgency
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <button
                                onClick={() => handleTriageAction(item.id, 'verified', 'Verified after review')}
                                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center"
                              >
                                <CheckCircle className="w-4 h-4 mr-1" />
                                Verify
                              </button>
                              <button
                                onClick={() => handleTriageAction(item.id, 'rejected', 'Insufficient evidence')}
                                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center"
                              >
                                <X className="w-4 h-4 mr-1" />
                                Reject
                              </button>
                              <button className="text-gray-400 hover:text-gray-600 p-2">
                                <Eye className="w-4 h-4" />
                              </button>
                            </div>
                          </div>
                          
                          {/* Location */}
                          <div className="mt-2">
                            <p className="text-gray-600 font-medium">{item.location}</p>
                          </div>
                        </div>

                        {/* Content */}
                        <div className="p-4">
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                            <div className="flex items-center text-sm">
                              <Users className="w-4 h-4 text-gray-400 mr-2" />
                              <span className="text-gray-600">{item.reportCount} reports</span>
                            </div>
                            <div className="flex items-center text-sm">
                              <Clock className="w-4 h-4 text-gray-400 mr-2" />
                              <span className="text-gray-600">{item.lastUpdated}</span>
                            </div>
                            <div className="flex items-center text-sm">
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                item.sentiment === 'panic' ? 'bg-red-100 text-red-700' :
                                item.sentiment === 'concern' ? 'bg-orange-100 text-orange-700' :
                                'bg-green-100 text-green-700'
                              }`}>
                                {item.sentiment}
                              </span>
                            </div>
                            <div className="flex items-center text-sm">
                              <span className="text-gray-600">
                                {item.sources.length > 1 ? 'Multiple Sources' : item.sources[0]}
                              </span>
                            </div>
                          </div>

                          {/* Source tags */}
                          <div className="flex items-center space-x-2">
                            {item.sources.map((source, index) => (
                              <span key={index} className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs">
                                {source}
                              </span>
                            ))}
                          </div>

                          {/* Bottom actions */}
                          <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
                            <div className="flex items-center space-x-4">
                              <button className="flex items-center text-gray-600 hover:text-blue-600 transition-colors text-sm">
                                <Eye className="w-4 h-4 mr-1" />
                                View
                              </button>
                              <button className="flex items-center text-gray-600 hover:text-blue-600 transition-colors text-sm">
                                <Clock className="w-4 h-4 mr-1" />
                                Timeline
                              </button>
                              <button className="flex items-center text-gray-600 hover:text-blue-600 transition-colors text-sm">
                                <UserCheck className="w-4 h-4 mr-1" />
                                Assign
                              </button>
                            </div>
                            <div className="text-xs text-gray-500">
                              Status: {item.status.replace('_', ' ').toUpperCase()}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Golden Hour Map Tab */}
          {activeTab === 'golden-hour-map' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                    <Map className="w-5 h-5 mr-2" />
                    Interactive Map - Critical Infrastructure
                  </h2>
                  <div className="flex items-center space-x-2">
                    {Object.entries(mapOverlays).map(([key, value]) => (
                      <button
                        key={key}
                        onClick={() => toggleMapOverlay(key)}
                        className={`px-3 py-1 rounded-lg text-sm transition-colors ${
                          value 
                            ? 'bg-blue-100 text-blue-700' 
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        <Layers className="w-3 h-3 mr-1 inline" />
                        {key.charAt(0).toUpperCase() + key.slice(1)}
                      </button>
                    ))}
                  </div>
                </div>
                <p className="text-gray-600 mt-2">Real-time overlay of critical infrastructure, emergency assets, and predicted hazard zones.</p>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
                      <div className="text-center">
                        <Map className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-500">Interactive Map Component</p>
                        <p className="text-sm text-gray-400">Real-time infrastructure and hazard overlay</p>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Critical Infrastructure Status</h3>
                    {criticalInfrastructure.map((item) => (
                      <div key={item.id} className="bg-gray-50 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium text-sm">{item.name}</h4>
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            item.status === 'Operational' || item.status === 'Active' || item.status === 'Ready' || item.status === 'Clear'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {item.status}
                          </span>
                        </div>
                        <div className="flex items-center justify-between text-xs text-gray-500">
                          <span className="flex items-center">
                            {item.type === 'Hospital' && <Heart className="w-3 h-3 mr-1" />}
                            {item.type === 'Shelter' && <Home className="w-3 h-3 mr-1" />}
                            {item.type === 'Emergency Services' && <Truck className="w-3 h-3 mr-1" />}
                            {item.type === 'Route' && <Route className="w-3 h-3 mr-1" />}
                            {item.type}
                          </span>
                          <span>{item.capacity}</span>
                        </div>
                        <div className="flex items-center justify-between mt-2">
                          <span className="text-xs text-gray-500">{item.contact}</span>
                          <button className="text-blue-600 hover:text-blue-800">
                            <Phone className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Incident Communication Tab */}
          {activeTab === 'incident-chat' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                    <MessageSquare className="w-5 h-5 mr-2" />
                    Internal Incident Communication
                  </h2>
                  <div className="flex items-center space-x-2">
                    <select
                      value={activeIncident || ''}
                      onChange={(e) => setActiveIncident(e.target.value)}
                      className="border border-gray-300 rounded-lg px-3 py-1 text-sm"
                    >
                      <option value="">Select Incident</option>
                      {triageQueue.map((item) => (
                        <option key={item.id} value={item.id}>{item.title}</option>
                      ))}
                    </select>
                    <button className="bg-green-100 text-green-700 px-3 py-1 rounded-lg text-sm">
                      <Wifi className="w-3 h-3 mr-1 inline" />
                      Online
                    </button>
                  </div>
                </div>
                <p className="text-gray-600 mt-2">Secure, role-based messaging for coordinated emergency response.</p>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2">
                    <div className="bg-gray-50 rounded-lg h-80 p-4 overflow-y-auto mb-4">
                      {incidentChat.map((message) => (
                        <div key={message.id} className="mb-3">
                          <div className="flex items-start space-x-3">
                            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                              {message.sender.charAt(0)}
                            </div>
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="font-medium text-sm">{message.sender}</span>
                                <span className="text-xs text-gray-500">{message.timestamp}</span>
                                <span className={`px-2 py-1 rounded-full text-xs ${
                                  message.priority === 'high' ? 'bg-red-100 text-red-700' :
                                  message.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                                  'bg-green-100 text-green-700'
                                }`}>
                                  {message.priority}
                                </span>
                              </div>
                              <p className="text-sm text-gray-700">{message.message}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    
                    <div className="flex items-center space-x-2">
                      <input
                        type="text"
                        value={chatMessage}
                        onChange={(e) => setChatMessage(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                        onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      />
                      <button
                        onClick={handleSendMessage}
                        disabled={!chatMessage.trim() || !activeIncident}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
                      >
                        <Send className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h3 className="font-medium text-gray-900">Active Responders</h3>
                    <div className="space-y-2">
                      {['Coast Guard Chennai', 'District Collector', 'Police Control Room', 'Fire Department'].map((responder, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                          <span className="text-sm">{responder}</span>
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span className="text-xs text-gray-500">Online</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Urgency Dashboard Tab */}
          {activeTab === 'urgency-filter' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Gauge className="w-5 h-5 mr-2" />
                  Severity/Urgency Index Dashboard
                </h2>
                <p className="text-gray-600 mt-2">Automated urgency scoring based on NLP sentiment analysis and verified report count for resource prioritization.</p>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2 space-y-4">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-medium text-gray-900">Priority Queue (Auto-Sorted by Urgency)</h3>
                      <div className="flex items-center space-x-2">
                        <button className="bg-red-100 text-red-700 px-3 py-1 rounded-lg text-sm">
                          Critical (90%+)
                        </button>
                        <button className="bg-orange-100 text-orange-700 px-3 py-1 rounded-lg text-sm">
                          High (70-89%)
                        </button>
                        <button className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-lg text-sm">
                          Medium (50-69%)
                        </button>
                      </div>
                    </div>
                    
                    {triageQueue
                      .sort((a, b) => b.urgencyScore - a.urgencyScore)
                      .map((item) => (
                        <div key={item.id} className={`rounded-lg p-4 border-l-4 ${
                          item.urgencyScore >= 90 ? 'bg-red-50 border-red-500' :
                          item.urgencyScore >= 70 ? 'bg-orange-50 border-orange-500' :
                          'bg-yellow-50 border-yellow-500'
                        }`}>
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center space-x-3">
                              <h4 className="font-semibold text-gray-900">{item.title}</h4>
                              <div className={`flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                                item.urgencyScore >= 90 ? 'bg-red-100 text-red-800' :
                                item.urgencyScore >= 70 ? 'bg-orange-100 text-orange-800' :
                                'bg-yellow-100 text-yellow-800'
                              }`}>
                                <Gauge className="w-4 h-4 mr-1" />
                                {item.urgencyScore}% Urgency
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg text-sm">
                                Deploy Resources
                              </button>
                              <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-lg text-sm">
                                View Details
                              </button>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                            <div>
                              <span className="text-gray-500">Location:</span>
                              <p className="font-medium">{item.location}</p>
                            </div>
                            <div>
                              <span className="text-gray-500">Reports:</span>
                              <p className="font-medium">{item.reportCount} verified</p>
                            </div>
                            <div>
                              <span className="text-gray-500">Sentiment:</span>
                              <p className={`font-medium ${
                                item.sentiment === 'panic' ? 'text-red-600' :
                                item.sentiment === 'concern' ? 'text-orange-600' :
                                'text-green-600'
                              }`}>
                                {item.sentiment}
                              </p>
                            </div>
                            <div>
                              <span className="text-gray-500">Last Update:</span>
                              <p className="font-medium">{item.lastUpdated}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                  </div>
                  
                  <div className="space-y-6">
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h3 className="font-medium text-gray-900 mb-3">Urgency Scoring Algorithm</h3>
                      <div className="space-y-3 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Verified Reports (40%)</span>
                          <span className="font-medium">Weight: High</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Sentiment Analysis (30%)</span>
                          <span className="font-medium">Weight: High</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Time Sensitivity (20%)</span>
                          <span className="font-medium">Weight: Medium</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Geographic Spread (10%)</span>
                          <span className="font-medium">Weight: Low</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="bg-gray-50 rounded-lg p-4">
                      <h3 className="font-medium text-gray-900 mb-3">Resource Allocation</h3>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between p-2 bg-white rounded">
                          <span className="text-sm">Coast Guard Units</span>
                          <span className="text-sm font-medium text-green-600">3 Available</span>
                        </div>
                        <div className="flex items-center justify-between p-2 bg-white rounded">
                          <span className="text-sm">Emergency Vehicles</span>
                          <span className="text-sm font-medium text-green-600">12 Available</span>
                        </div>
                        <div className="flex items-center justify-between p-2 bg-white rounded">
                          <span className="text-sm">Medical Teams</span>
                          <span className="text-sm font-medium text-yellow-600">2 Available</span>
                        </div>
                        <div className="flex items-center justify-between p-2 bg-white rounded">
                          <span className="text-sm">Evacuation Centers</span>
                          <span className="text-sm font-medium text-green-600">5 Ready</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* EWS Comparison Tab */}
          {activeTab === 'ews-comparison' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Radar className="w-5 h-5 mr-2" />
                  Early Warning System Comparison
                </h2>
                <p className="text-gray-600 mt-2">Compare INCOIS predictions with actual crowdsourced impact data.</p>
              </div>
              
              <div className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h3 className="font-medium text-blue-900 mb-3 flex items-center">
                      <Satellite className="w-4 h-4 mr-2" />
                      INCOIS Predicted Impact
                    </h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-blue-700">Affected Area:</span>
                        <span className="text-sm font-medium text-blue-900">{ewsComparison.incoisPredicted?.area}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-blue-700">Population at Risk:</span>
                        <span className="text-sm font-medium text-blue-900">{ewsComparison.incoisPredicted?.affectedPopulation}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-blue-700">Risk Level:</span>
                        <span className="text-sm font-medium text-blue-900">{ewsComparison.incoisPredicted?.riskLevel}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-blue-700">Warning Issued:</span>
                        <span className="text-sm font-medium text-blue-900">{ewsComparison.incoisPredicted?.warningTime}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-orange-50 rounded-lg p-4">
                    <h3 className="font-medium text-orange-900 mb-3 flex items-center">
                      <Users className="w-4 h-4 mr-2" />
                      Crowdsourced Actual Impact
                    </h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-orange-700">Actual Area:</span>
                        <span className="text-sm font-medium text-orange-900">{ewsComparison.crowdsourcedActual?.area}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-orange-700">Actual Population:</span>
                        <span className="text-sm font-medium text-orange-900">{ewsComparison.crowdsourcedActual?.affectedPopulation}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-orange-700">Actual Risk Level:</span>
                        <span className="text-sm font-medium text-orange-900">{ewsComparison.crowdsourcedActual?.riskLevel}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-orange-700">First Report:</span>
                        <span className="text-sm font-medium text-orange-900">{ewsComparison.crowdsourcedActual?.firstReportTime}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 bg-gray-50 rounded-lg p-4">
                  <h3 className="font-medium text-gray-900 mb-3">Variance Analysis</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <p className="text-2xl font-bold text-red-600">{ewsComparison.variance?.areaVariance}</p>
                      <p className="text-sm text-gray-600">Area Variance</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold text-red-600">{ewsComparison.variance?.populationVariance}</p>
                      <p className="text-sm text-gray-600">Population Variance</p>
                    </div>
                    <div className="text-center">
                      <p className="text-2xl font-bold text-green-600">{ewsComparison.variance?.timeAdvantage}</p>
                      <p className="text-sm text-gray-600">Early Detection</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      {showTimelineModal && selectedReport && (
        <TimelineModal 
          report={selectedReport} 
          onClose={() => setShowTimelineModal(false)} 
        />
      )}

      {showAnnouncementModal && (
        <AnnouncementModal 
          onClose={() => setShowAnnouncementModal(false)} 
        />
      )}

      {showProfileModal && (
        <ProfileModal 
          onClose={() => setShowProfileModal(false)} 
        />
      )}
    </div>
  );
};

export default AuthorityDashboard;
