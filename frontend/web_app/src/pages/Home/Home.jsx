import React, { useEffect, useState } from 'react';
import { MapPin, Waves, Shield, Phone, Navigation, AlertTriangle, CheckCircle, Users, Clock, Star, Anchor, Cross } from 'lucide-react';
import MapView from '../../components/MapView.jsx';
import { fetchHotspots, fetchRecentReports } from '../../services/hotspotService.js';

const Home = () => {
  const [hotspots, setHotspots] = useState([]);
  const [loadingHotspots, setLoadingHotspots] = useState(true);
  const [hotspotError, setHotspotError] = useState('');
  const [myLocation, setMyLocation] = useState(null); // { lat, lng }
  const [locationAllowed, setLocationAllowed] = useState(null); // null|true|false
  const [recentReports, setRecentReports] = useState([]);
  const [loadingReports, setLoadingReports] = useState(true);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const items = await fetchHotspots();
        if (mounted) setHotspots(items);
      } catch (e) {
        if (mounted) setHotspotError('Failed to load hotspots');
      } finally {
        if (mounted) setLoadingHotspots(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  // Load recent reports
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const items = await fetchRecentReports(10);
        if (mounted) setRecentReports(items);
      } catch (e) {
        // silent fail, we will show static fallback
      } finally {
        if (mounted) setLoadingReports(false);
      }
    })();
    return () => { mounted = false; };
  }, []);

  // Request location permission and current position
  useEffect(() => {
    let active = true;
    if (!navigator.geolocation) {
      setLocationAllowed(false);
      return () => {};
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        if (!active) return;
        setMyLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setLocationAllowed(true);
      },
      () => {
        if (!active) return;
        setLocationAllowed(false);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 300000 }
    );
    return () => { active = false; };
  }, []);

  return (
    <div className="min-h-screen bg-sky-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Main Title Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            {/* App Logo and Name */}
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900 text-left">Dashboard</h1>
            </div>
            {/* SOS Button */}
            <button className="bg-gradient-to-r from-red-600 to-red-500 text-white px-6 py-3 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-200 flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5" />
              <span>SOS</span>
            </button>
          </div>
          
          <p className="text-slate-600 text-lg text-left">
            Stay informed about current ocean conditions and safety alerts.
          </p>
        </div>

        {/* Content Cards */}
        <div className="space-y-8">
          {/* Current Location Card */}
          <div className="bg-slate-50 rounded-xl shadow-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center">
                <MapPin className="w-6 h-6 text-blue-800 mr-3" />
                <h2 className="text-xl font-semibold text-blue-800">Current Location</h2>
              </div>
              <div className="bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-full text-sm font-medium flex items-center">
                <MapPin className="w-4 h-4 mr-1" />
                GPS Active
              </div>
            </div>
            
            {/* Map Container */}
            <div className="h-64 rounded-lg border-2 border-slate-300 overflow-hidden">
              <div className="relative h-full">
                {hotspotError ? (
                  <div className="absolute inset-0 flex items-center justify-center text-sm text-red-600 bg-red-50">{hotspotError}</div>
                ) : null}
                <MapView
                  height="256px"
                  center={myLocation ? [myLocation.lat, myLocation.lng] : [12.9716, 77.5946]}
                  zoom={myLocation ? 13 : 11}
                  markers={locationAllowed && myLocation ? [{ position: [myLocation.lat, myLocation.lng], popup: 'My Location' }] : []}
                  hotspots={hotspots}
                />
                {loadingHotspots ? (
                  <div className="absolute bottom-2 left-2 bg-white/80 text-gray-700 text-xs px-2 py-1 rounded">Loading hotspots…</div>
                ) : null}
              </div>
            </div>
          </div>

          {/* Recent Reports Card */
          }
          <div className="bg-slate-50 rounded-xl shadow-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center">
                <Users className="w-6 h-6 text-blue-800 mr-3" />
                <h2 className="text-xl font-semibold text-blue-800">Recent Reports</h2>
              </div>
              <button className="text-blue-600 text-lg font-semibold hover:text-blue-700 transition-colors duration-200 px-4 py-2 rounded-lg hover:bg-blue-50">
                View More
              </button>
            </div>
            
            <div className="relative">
              <div className="flex gap-6 overflow-x-auto overflow-y-hidden pb-2 snap-x snap-mandatory scrollbar-thin scrollbar-thumb-slate-300">
                {(!loadingReports && recentReports && recentReports.length > 0) ? (
                  recentReports.map((r) => (
                    <div key={r.id} className="bg-white rounded-xl p-6 border border-gray-200 shadow-lg hover:shadow-xl transition-transform duration-200 hover:scale-[1.01] relative flex flex-col h-full min-w-[280px] max-w-[320px] snap-start">
                      <div className="mb-2">
                      <h3 className="font-bold text-gray-900 text-lg leading-tight">{r.title}</h3>
                    </div>
                      <div className="mb-4">
                        <div className={`inline-flex px-2.5 py-1 rounded-full text-xs font-medium items-center text-white ${r.status === 'verified' ? 'bg-green-600' : r.status === 'under_verification' ? 'bg-yellow-500' : 'bg-red-600'}` }>
                          <CheckCircle className="w-3.5 h-3.5 mr-1" />
                          {r.status?.replace('_', ' ') || 'status'}
                        </div>
                      </div>
                    {r.description ? (
                      <p className="text-gray-700 text-base mb-6 leading-relaxed line-clamp-4">{r.description}</p>
                    ) : null}
                    <div className="h-48 rounded-xl overflow-hidden mb-6 flex-grow bg-gray-100">
                      {r.thumbnailUrl ? (
                        <img src={r.thumbnailUrl} alt={r.title} className="w-full h-full object-cover" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-gray-400 text-sm">No media</div>
                      )}
                    </div>
                    <div className="flex items-center justify-between pt-4 border-t border-gray-100 mt-auto">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                          <Users className="w-4 h-4 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-semibold text-gray-900 text-sm">{r.city || 'Community'}</p>
                          <p className="text-xs text-gray-500">Reporter</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-medium text-gray-600">{r.createdAt ? new Date(r.createdAt).toLocaleString() : ''}</p>
                        <p className="text-xs text-gray-500">Created</p>
                      </div>
                    </div>
                    </div>
                  ))
                ) : (
                  !loadingReports && (
                    <div className="text-gray-600 text-sm px-2">No current reports</div>
                  )
                )}
              </div>
            </div>
          </div>

          {/* Risk Assessment Card */}
          <div className="bg-slate-50 rounded-xl shadow-lg p-8">
            <div className="flex items-center mb-6">
              <Shield className="w-6 h-6 text-blue-800 mr-3" />
              <h2 className="text-xl font-semibold text-blue-800">Risk Assessment</h2>
            </div>
            
            {/* High Risk Indicator */}
            <div className="bg-gradient-to-r from-red-600 to-red-700 rounded-xl p-6 mb-6 shadow-lg">
              <div className="flex items-center justify-between text-white">
                <div className="flex items-start">
                  <AlertTriangle className="w-8 h-8 mr-4 mt-1" />
                  <div>
                    <h3 className="text-2xl font-bold text-left">High Risk</h3>
                    <p className="text-base opacity-90 text-left">Current ocean hazard level for your location</p>
                  </div>
                </div>
                <div className="text-4xl font-bold">76%</div>
              </div>
            </div>
            
            {/* Risk Factors */}
            <div>
              <h3 className="text-lg font-bold text-gray-800 mb-4">Risk Factors</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-base mb-2">
                    <span className="text-gray-800 font-medium">Wave Height</span>
                    <span className="font-bold text-blue-800">75%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full shadow-sm" style={{width: '75%'}}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-base mb-2">
                    <span className="text-gray-800 font-medium">Current Strength</span>
                    <span className="font-bold text-blue-800">50%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full shadow-sm" style={{width: '50%'}}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex justify-between text-base mb-2">
                    <span className="text-gray-800 font-medium">Water Temperature</span>
                    <span className="font-bold text-blue-800">30%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full shadow-sm" style={{width: '30%'}}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Safety Recommendations Card */}
          <div className="bg-slate-50 rounded-xl shadow-lg p-8">
            <div className="flex items-center mb-6">
              <Shield className="w-6 h-6 text-blue-800 mr-3" />
              <h2 className="text-xl font-semibold text-blue-800">Safety Recommendations</h2>
            </div>
            
            <div className="space-y-3">
              {[
                'Avoid swimming alone',
                'Stay close to shore',
                'Check with lifeguards before entering',
                'Be aware of rip current warnings'
              ].map((recommendation, index) => (
                <div key={index} className="flex items-start">
                  <div className="w-2 h-2 bg-blue-800 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                  <p className="text-gray-700 text-base">{recommendation}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Safe Places Card (Indian locations; distance from Bengaluru) */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center mb-6">
              <Shield className="w-5 h-5 text-red-500 mr-3" />
              <h2 className="text-lg font-semibold text-gray-800">Safe Places</h2>
            </div>
            
            <div className="space-y-4">
              {(() => {
                const BLR = { lat: 12.9716, lng: 77.5946 };
                const toRad = (d) => (d * Math.PI) / 180;
                const haversineKm = (a, b) => {
                  const R = 6371;
                  const dLat = toRad(b.lat - a.lat);
                  const dLng = toRad(b.lng - a.lng);
                  const sa = Math.sin(dLat/2)**2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng/2)**2;
                  const c = 2 * Math.atan2(Math.sqrt(sa), Math.sqrt(1 - sa));
                  return R * c;
                };
                const places = [
                  { name: 'Bengaluru City Police HQ', type: 'Police Station', phone: '+91 80 2294 3333', coord: { lat: 12.9716, lng: 77.5946 }, icon: 'shield', rating: 4.7, hours: '24 hours' },
                  { name: 'NIMHANS Emergency', type: 'Medical Facility', phone: '+91 80 2699 5555', coord: { lat: 12.9426, lng: 77.5950 }, icon: 'cross', rating: 4.6, hours: '24 hours' },
                  { name: 'KSDMA Control Room', type: 'Emergency Shelter', phone: '+91 80 2225 5555', coord: { lat: 12.9784, lng: 77.5750 }, icon: 'shield', rating: 4.5, hours: '24 hours' },
                  { name: 'Ulsoor Lake Lifeguard Point', type: 'Lifeguard Station', phone: '+91 80 2294 0000', coord: { lat: 12.9833, lng: 77.6280 }, icon: 'anchor', rating: 4.4, hours: '6:00 AM - 8:00 PM' },
                ].map((p) => ({ ...p, distanceKm: haversineKm(BLR, p.coord) }));
                return places.map((p, idx) => (
                  <div key={idx} className="flex items-start justify-between py-4 border-b border-gray-100 last:border-b-0">
                    <div className="flex items-start space-x-3">
                      <div className={`w-8 h-8 ${p.icon==='anchor' ? 'bg-blue-100' : p.icon==='cross' ? 'bg-purple-100' : 'bg-orange-100'} rounded-lg flex items-center justify-center mt-1`}>
                        {p.icon==='anchor' ? <Anchor className="w-4 h-4 text-blue-600" /> : p.icon==='cross' ? <Cross className="w-4 h-4 text-purple-600" /> : <Shield className="w-4 h-4 text-orange-600" />}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 text-base mb-1">{p.name}</h3>
                        <p className="text-sm text-blue-600 mb-2 text-left">{p.type}</p>
                        <div className="flex items-center text-sm text-gray-600 mb-1">
                          <Phone className="w-4 h-4 mr-1" />
                          <span>{p.phone}</span>
                        </div>
                        <div className="flex items-center text-sm text-gray-600">
                          <Clock className="w-4 h-4 mr-1" />
                          <span>{p.hours}</span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600 mb-1">{p.distanceKm.toFixed(1)} km</p>
                      <div className="flex items-center">
                        <Star className="w-4 h-4 text-yellow-400 fill-current" />
                        <span className="text-sm font-medium text-gray-700 ml-1">{p.rating}</span>
                      </div>
                    </div>
                  </div>
                ));
              })()}
            </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
