import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Download, 
  Search, 
  Filter,
  Calendar,
  Users,
  AlertCircle,
  Clock,
  Target,
  Database,
  FileText,
  Activity,
  Brain,
  Zap,
  Shield,
  Globe,
  Hash,
  MessageSquare,
  Star,
  Award,
  Eye,
  Settings,
  RefreshCw,
  ChevronDown,
  Plus,
  X,
  MoreVertical,
  ArrowUpRight,
  ArrowDownRight,
  TrendingDown,
  MapPin,
  Layers,
  Code,
  ExternalLink,
  BarChart,
  PieChart,
  LineChart
} from 'lucide-react';

const AnalystDashboard = () => {
  const [activeTab, setActiveTab] = useState('query-builder');
  const [queryFilters, setQueryFilters] = useState({
    event_types: [],
    keywords: '',
    location: '',
    start_date: '',
    end_date: '',
    status: '',
    min_confidence: 0,
    max_confidence: 100,
    social_media_source: '',
    sentiment: '',
    time_window: '24h'
  });
  
  const [queryResults, setQueryResults] = useState([]);
  const [lagAnalysis, setLagAnalysis] = useState([]);
  const [nlpTrends, setNlpTrends] = useState([]);
  const [reliabilityScores, setReliabilityScores] = useState([]);
  const [socialMediaData, setSocialMediaData] = useState([]);
  const [performanceMetrics, setPerformanceMetrics] = useState({});
  const [loading, setLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState(false);

  // Mock data - replace with actual API calls
  useEffect(() => {
    // Load comprehensive mock data
    setLagAnalysis([
      { 
        date: '2024-01-15', 
        avg_verification_time_minutes: 45, 
        report_count: 12, 
        hazard_type: 'Tsunami',
        incois_warning_delay: 23,
        first_report_time: '10:15',
        warning_issued_time: '10:38'
      },
      { 
        date: '2024-01-14', 
        avg_verification_time_minutes: 32, 
        report_count: 8, 
        hazard_type: 'High Waves',
        incois_warning_delay: 18,
        first_report_time: '14:22',
        warning_issued_time: '14:40'
      },
      { 
        date: '2024-01-13', 
        avg_verification_time_minutes: 28, 
        report_count: 15, 
        hazard_type: 'Storm Surge',
        incois_warning_delay: 35,
        first_report_time: '09:45',
        warning_issued_time: '10:20'
      }
    ]);
    
    setNlpTrends([
      { 
        keyword: 'tsunami', 
        frequency: 2847, 
        sentiment_score: 8.5, 
        time_period: 'last_24h',
        trend_direction: 'up',
        geographic_spread: ['Chennai', 'Visakhapatnam', 'Mumbai'],
        hashtags: ['#TsunamiAlert', '#CoastalSafety', '#EvacuateNow'],
        misinformation_detected: true
      },
      { 
        keyword: 'flooding', 
        frequency: 1923, 
        sentiment_score: 6.2, 
        time_period: 'last_24h',
        trend_direction: 'stable',
        geographic_spread: ['Kerala', 'Tamil Nadu', 'Odisha'],
        hashtags: ['#CoastalFlooding', '#HighTides', '#SafetyFirst'],
        misinformation_detected: false
      },
      { 
        keyword: 'evacuation', 
        frequency: 1456, 
        sentiment_score: 7.8, 
        time_period: 'last_24h',
        trend_direction: 'up',
        geographic_spread: ['Andhra Pradesh', 'West Bengal'],
        hashtags: ['#Evacuation', '#EmergencyResponse', '#StaySafe'],
        misinformation_detected: false
      },
      { 
        keyword: 'high waves', 
        frequency: 1234, 
        sentiment_score: 5.9, 
        time_period: 'last_24h',
        trend_direction: 'down',
        geographic_spread: ['Goa', 'Karnataka', 'Maharashtra'],
        hashtags: ['#HighWaves', '#BeachSafety', '#MarineWarning'],
        misinformation_detected: true
      }
    ]);
    
    setReliabilityScores([
      { 
        user_id: '1', 
        user_name: 'Dr. Rajesh Kumar', 
        total_reports: 156, 
        verified_reports: 142, 
        reliability_percentage: 91, 
        avg_confidence_score: 0.89,
        location: 'Chennai Marine Research',
        expertise: 'Tsunami Expert',
        recent_activity: '2 hours ago'
      },
      { 
        user_id: '2', 
        user_name: 'Priya Sharma', 
        total_reports: 89, 
        verified_reports: 81, 
        reliability_percentage: 91, 
        avg_confidence_score: 0.87,
        location: 'Mumbai Coast Guard',
        expertise: 'Coastal Observer',
        recent_activity: '4 hours ago'
      },
      { 
        user_id: '3', 
        user_name: 'Captain Arjun Singh', 
        total_reports: 203, 
        verified_reports: 178, 
        reliability_percentage: 88, 
        avg_confidence_score: 0.85,
        location: 'Visakhapatnam Port',
        expertise: 'Marine Operations',
        recent_activity: '1 hour ago'
      },
      { 
        user_id: '4', 
        user_name: 'Meera Nair', 
        total_reports: 67, 
        verified_reports: 58, 
        reliability_percentage: 87, 
        avg_confidence_score: 0.83,
        location: 'Kochi Fisheries',
        expertise: 'Local Observer',
        recent_activity: '6 hours ago'
      }
    ]);

    setSocialMediaData([
      {
        platform: 'Twitter',
        mentions: 15234,
        sentiment: 'negative',
        top_hashtags: ['#TsunamiAlert', '#CoastalSafety', '#EvacuateNow'],
        verified_accounts: 45,
        misinformation_posts: 23,
        geographic_hotspots: ['Chennai', 'Mumbai', 'Visakhapatnam']
      },
      {
        platform: 'Facebook',
        mentions: 8967,
        sentiment: 'mixed',
        top_hashtags: ['#StaySafe', '#CoastalFlooding', '#EmergencyUpdate'],
        verified_accounts: 12,
        misinformation_posts: 8,
        geographic_hotspots: ['Kerala', 'Tamil Nadu', 'Goa']
      },
      {
        platform: 'Instagram',
        mentions: 5432,
        sentiment: 'neutral',
        top_hashtags: ['#BeachSafety', '#HighWaves', '#MarineLife'],
        verified_accounts: 23,
        misinformation_posts: 3,
        geographic_hotspots: ['Goa', 'Karnataka', 'Andhra Pradesh']
      }
    ]);

    setPerformanceMetrics({
      model_accuracy: 87.3,
      false_positive_rate: 8.2,
      false_negative_rate: 4.5,
      avg_processing_time: 2.3,
      data_quality_score: 92.1,
      api_uptime: 99.7,
      total_processed_reports: 45678,
      verified_reports: 39234,
      rejected_reports: 6444
    });
  }, []);

  const handleCustomQuery = async () => {
    setLoading(true);
    // TODO: Implement API call to /api/analyst/query
    setTimeout(() => {
      setQueryResults([
        {
          id: '1',
          user_name: 'John Doe',
          hazard_type: 'High Waves / Swell',
          description: 'Large waves observed near coastline',
          confidence_score: 0.85,
          status: 'verified',
          created_at: '2024-01-15T10:30:00Z'
        },
        {
          id: '2',
          user_name: 'Jane Smith',
          hazard_type: 'Coastal Flooding',
          description: 'Water levels rising in coastal areas',
          confidence_score: 0.72,
          status: 'under_verification',
          created_at: '2024-01-15T09:15:00Z'
        }
      ]);
      setLoading(false);
    }, 1000);
  };

  const handleExportData = async (format) => {
    // TODO: Implement API call to /api/analyst/export
    const queryString = new URLSearchParams({
      format,
      filters: JSON.stringify(queryFilters)
    }).toString();
    
    // For now, just log the action
    console.log(`Exporting data as ${format} with filters:`, queryFilters);
    
    // In real implementation, this would trigger a download
    alert(`Export initiated for ${format.toUpperCase()} format`);
  };

  const getSentimentColor = (score) => {
    if (score >= 8) return 'text-red-600 bg-red-100';
    if (score >= 6) return 'text-orange-600 bg-orange-100';
    return 'text-yellow-600 bg-yellow-100';
  };

  const getReliabilityColor = (percentage) => {
    if (percentage >= 85) return 'text-green-600 bg-green-100';
    if (percentage >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center mr-4">
                <Brain className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Advanced Analytics Hub</h1>
                <p className="text-gray-600 mt-1">Deep insights into ocean hazard data and social media intelligence</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => handleExportData('csv')}
                disabled={exportLoading}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center disabled:opacity-50"
              >
                <Download className="w-4 h-4 mr-2" />
                Export CSV
              </button>
              <button
                onClick={() => handleExportData('json')}
                disabled={exportLoading}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center disabled:opacity-50"
              >
                <Code className="w-4 h-4 mr-2" />
                Export JSON
              </button>
              <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors flex items-center">
                <ExternalLink className="w-4 h-4 mr-2" />
                API Access
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
                <p className="text-sm font-medium text-gray-600">Model Accuracy</p>
                <p className="text-3xl font-bold text-gray-900">{performanceMetrics.model_accuracy}%</p>
              </div>
              <div className="bg-green-100 p-3 rounded-lg">
                <Target className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="mt-2">
              <ArrowUpRight className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">+2.3% from last week</span>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p className="text-3xl font-bold text-gray-900">{performanceMetrics.avg_processing_time}s</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-lg">
                <Zap className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <div className="mt-2">
              <ArrowDownRight className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">-0.8s improvement</span>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Data Quality</p>
                <p className="text-3xl font-bold text-gray-900">{performanceMetrics.data_quality_score}%</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-lg">
                <Shield className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <div className="mt-2">
              <ArrowUpRight className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">High quality data</span>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">API Uptime</p>
                <p className="text-3xl font-bold text-gray-900">{performanceMetrics.api_uptime}%</p>
              </div>
              <div className="bg-orange-100 p-3 rounded-lg">
                <Activity className="w-6 h-6 text-orange-600" />
              </div>
            </div>
            <div className="mt-2">
              <Activity className="w-4 h-4 text-green-500 inline mr-1" />
              <span className="text-sm text-green-600">System healthy</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'query-builder', name: 'Advanced Query Builder', icon: Search },
              { id: 'lag-analysis', name: 'Response Time Analysis', icon: Clock },
              { id: 'nlp-dashboard', name: 'Social Media Intelligence', icon: Brain },
              { id: 'reliability-scores', name: 'Community Reliability', icon: Users },
              { id: 'export-api', name: 'Data Export & API', icon: Download }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
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
          {/* Advanced Query Builder */}
          {activeTab === 'query-builder' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm border">
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                      <Search className="w-5 h-5 mr-2" />
                      Advanced Query Builder
                    </h2>
                    <div className="flex items-center space-x-2">
                      <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-lg text-sm transition-colors">
                        Save Query
                      </button>
                      <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1 rounded-lg text-sm transition-colors">
                        Load Template
                      </button>
                    </div>
                  </div>
                  <p className="text-gray-600 mt-2">Build complex queries to analyze crowdsourced and social media data with advanced filtering options.</p>
                </div>
              
                <div className="p-6 space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Event Types</label>
                      <select multiple className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500">
                        <option value="Tsunami">Tsunami</option>
                        <option value="High Waves">High Waves</option>
                        <option value="Coastal Flooding">Coastal Flooding</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Keywords</label>
                      <input type="text" placeholder="infrastructure damage, evacuation..." className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                      <input type="text" placeholder="Chennai, Mumbai..." className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm" />
                    </div>
                  </div>
                  <div className="flex justify-end">
                    <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium flex items-center">
                      <Search className="w-4 h-4 mr-2" />
                      Run Advanced Query
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Response Time Analysis Tab */}
          {activeTab === 'lag-analysis' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Clock className="w-5 h-5 mr-2" />
                  Report-to-Warning Lag Analysis
                </h2>
              </div>
              <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                  {lagAnalysis.map((item, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex justify-between items-center">
                        <div>
                          <h4 className="font-medium">{item.hazard_type}</h4>
                          <p className="text-sm text-gray-500">{item.date}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-lg font-bold text-red-600">{item.incois_warning_delay}m</p>
                          <p className="text-xs text-gray-500">delay</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="space-y-4">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h3 className="font-medium text-blue-900">Average Warning Delay</h3>
                    <p className="text-2xl font-bold text-blue-900">25.3 min</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Social Media Intelligence Tab */}
          {activeTab === 'nlp-dashboard' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Brain className="w-5 h-5 mr-2" />
                  Social Media Intelligence
                </h2>
              </div>
              <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="font-medium">Trending Keywords</h3>
                  {nlpTrends.map((trend, index) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium">#{trend.keyword}</p>
                        <p className="text-sm text-gray-500">{trend.frequency} mentions</p>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full ${getSentimentColor(trend.sentiment_score)}`}>
                        {trend.sentiment_score.toFixed(1)}
                      </span>
                    </div>
                  ))}
                </div>
                <div className="space-y-4">
                  <h3 className="font-medium">Platform Overview</h3>
                  {socialMediaData.map((platform, index) => (
                    <div key={index} className="bg-gray-50 rounded-lg p-4">
                      <h4 className="font-medium">{platform.platform}</h4>
                      <p className="text-sm text-gray-600">{platform.mentions} mentions</p>
                      <p className="text-sm text-gray-600">{platform.misinformation_posts} misinformation posts</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Community Reliability Tab */}
          {activeTab === 'reliability-scores' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Users className="w-5 h-5 mr-2" />
                  Community Reliability Scorecard
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {reliabilityScores.map((user, index) => (
                    <div key={user.user_id} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex justify-between items-center">
                        <div>
                          <h4 className="font-medium">{user.user_name}</h4>
                          <p className="text-sm text-gray-500">{user.location}</p>
                          <p className="text-sm text-gray-500">{user.total_reports} reports • {user.expertise}</p>
                        </div>
                        <div className="text-right">
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getReliabilityColor(user.reliability_percentage)}`}>
                            {user.reliability_percentage}%
                          </span>
                          <p className="text-xs text-gray-500 mt-1">{user.recent_activity}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Data Export & API Tab */}
          {activeTab === 'export-api' && (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Download className="w-5 h-5 mr-2" />
                  Raw Data Export & API Access
                </h2>
              </div>
              <div className="p-6 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h3 className="font-medium">Export Options</h3>
                    <div className="space-y-2">
                      <button onClick={() => handleExportData('csv')} className="w-full bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center justify-center">
                        <Download className="w-4 h-4 mr-2" />
                        Export as CSV
                      </button>
                      <button onClick={() => handleExportData('json')} className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center justify-center">
                        <Code className="w-4 h-4 mr-2" />
                        Export as JSON
                      </button>
                      <button className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg flex items-center justify-center">
                        <ExternalLink className="w-4 h-4 mr-2" />
                        API Documentation
                      </button>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <h3 className="font-medium">API Endpoints</h3>
                    <div className="bg-gray-50 rounded-lg p-4 text-sm font-mono">
                      <p>GET /api/analyst/reports</p>
                      <p>GET /api/analyst/social-media</p>
                      <p>GET /api/analyst/reliability</p>
                      <p>POST /api/analyst/query</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalystDashboard;
