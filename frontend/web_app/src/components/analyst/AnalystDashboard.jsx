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
  Activity
} from 'lucide-react';

const AnalystDashboard = () => {
  const [queryFilters, setQueryFilters] = useState({
    event_types: [],
    keywords: '',
    start_date: '',
    end_date: '',
    status: '',
    min_confidence: 0,
    max_confidence: 100
  });
  
  const [queryResults, setQueryResults] = useState([]);
  const [lagAnalysis, setLagAnalysis] = useState([]);
  const [nlpTrends, setNlpTrends] = useState([]);
  const [reliabilityScores, setReliabilityScores] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock data - replace with actual API calls
  useEffect(() => {
    // Load initial data
    setLagAnalysis([
      { date: '2024-01-15', avg_verification_time_minutes: 45, report_count: 12, hazard_type: 'Tsunami' },
      { date: '2024-01-14', avg_verification_time_minutes: 32, report_count: 8, hazard_type: 'High Waves' },
      { date: '2024-01-13', avg_verification_time_minutes: 28, report_count: 15, hazard_type: 'Storm Surge' }
    ]);
    
    setNlpTrends([
      { keyword: 'tsunami', frequency: 25, sentiment_score: 8.5, time_period: 'last_7_days' },
      { keyword: 'flooding', frequency: 18, sentiment_score: 6.2, time_period: 'last_7_days' },
      { keyword: 'evacuation', frequency: 12, sentiment_score: 7.8, time_period: 'last_7_days' },
      { keyword: 'emergency', frequency: 10, sentiment_score: 8.1, time_period: 'last_7_days' }
    ]);
    
    setReliabilityScores([
      { user_id: '1', user_name: 'John Doe', total_reports: 25, verified_reports: 22, reliability_percentage: 88, avg_confidence_score: 0.82 },
      { user_id: '2', user_name: 'Jane Smith', total_reports: 18, verified_reports: 16, reliability_percentage: 89, avg_confidence_score: 0.85 },
      { user_id: '3', user_name: 'Mike Johnson', total_reports: 32, verified_reports: 24, reliability_percentage: 75, avg_confidence_score: 0.78 }
    ]);
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
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <BarChart3 className="w-8 h-8 text-purple-600 mr-3" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Analyst Dashboard</h1>
                <p className="text-gray-600">Data analysis and insights</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => handleExportData('csv')}
                className="bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center"
              >
                <Download className="w-4 h-4 mr-2" />
                Export CSV
              </button>
              <button
                onClick={() => handleExportData('json')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center"
              >
                <Download className="w-4 h-4 mr-2" />
                Export JSON
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Database className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Reports</p>
                <p className="text-2xl font-bold text-gray-900">1,247</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Target className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Accuracy</p>
                <p className="text-2xl font-bold text-gray-900">82.5%</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Clock className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p className="text-2xl font-bold text-gray-900">35 min</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Trend Score</p>
                <p className="text-2xl font-bold text-gray-900">+12%</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Custom Query Builder */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                  <Search className="w-5 h-5 mr-2" />
                  Custom Data Query Builder
                </h2>
              </div>
              
              <div className="p-6 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Event Types</label>
                    <select 
                      multiple
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.event_types}
                      onChange={(e) => setQueryFilters({
                        ...queryFilters,
                        event_types: Array.from(e.target.selectedOptions, option => option.value)
                      })}
                    >
                      <option value="Tsunami">Tsunami</option>
                      <option value="High Waves / Swell">High Waves / Swell</option>
                      <option value="Coastal Flooding">Coastal Flooding</option>
                      <option value="Storm Surge">Storm Surge</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Keywords</label>
                    <input
                      type="text"
                      placeholder="Enter keywords..."
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.keywords}
                      onChange={(e) => setQueryFilters({...queryFilters, keywords: e.target.value})}
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                    <input
                      type="date"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.start_date}
                      onChange={(e) => setQueryFilters({...queryFilters, start_date: e.target.value})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                    <input
                      type="date"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.end_date}
                      onChange={(e) => setQueryFilters({...queryFilters, end_date: e.target.value})}
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
                    <select 
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.status}
                      onChange={(e) => setQueryFilters({...queryFilters, status: e.target.value})}
                    >
                      <option value="">All Statuses</option>
                      <option value="verified">Verified</option>
                      <option value="under_verification">Under Verification</option>
                      <option value="rejected">Rejected</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Min Confidence</label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.min_confidence}
                      onChange={(e) => setQueryFilters({...queryFilters, min_confidence: parseInt(e.target.value)})}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Max Confidence</label>
                    <input
                      type="number"
                      min="0"
                      max="100"
                      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
                      value={queryFilters.max_confidence}
                      onChange={(e) => setQueryFilters({...queryFilters, max_confidence: parseInt(e.target.value)})}
                    />
                  </div>
                </div>
                
                <button
                  onClick={handleCustomQuery}
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Querying...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4 mr-2" />
                      Run Query
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Query Results */}
            {queryResults.length > 0 && (
              <div className="bg-white rounded-lg shadow">
                <div className="p-6 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">Query Results ({queryResults.length})</h3>
                </div>
                <div className="divide-y divide-gray-200">
                  {queryResults.map((result) => (
                    <div key={result.id} className="p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900">{result.hazard_type}</h4>
                          <p className="text-gray-600 mt-1">{result.description}</p>
                          <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                            <span>By: {result.user_name}</span>
                            <span>Confidence: {(result.confidence_score * 100).toFixed(0)}%</span>
                            <span>Status: {result.status}</span>
                            <span>{new Date(result.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Report-to-Warning Lag Analysis */}
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <Clock className="w-5 h-5 mr-2" />
                  Response Time Analysis
                </h3>
              </div>
              <div className="p-4 space-y-3">
                {lagAnalysis.map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{item.hazard_type}</p>
                      <p className="text-sm text-gray-500">{item.report_count} reports</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-gray-900">{item.avg_verification_time_minutes}m</p>
                      <p className="text-sm text-gray-500">avg time</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* NLP Trends */}
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <Activity className="w-5 h-5 mr-2" />
                  Trending Keywords
                </h3>
              </div>
              <div className="p-4 space-y-3">
                {nlpTrends.map((trend, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">#{trend.keyword}</p>
                      <p className="text-sm text-gray-500">{trend.frequency} mentions</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSentimentColor(trend.sentiment_score)}`}>
                        {trend.sentiment_score.toFixed(1)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Reliability Scores */}
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <Users className="w-5 h-5 mr-2" />
                  Top Contributors
                </h3>
              </div>
              <div className="p-4 space-y-3">
                {reliabilityScores.map((user, index) => (
                  <div key={user.user_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{user.user_name}</p>
                      <p className="text-sm text-gray-500">{user.total_reports} reports</p>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getReliabilityColor(user.reliability_percentage)}`}>
                        {user.reliability_percentage}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalystDashboard;
