import api from '../utils/api';

export const fetchHotspots = async () => {
  const { data } = await api.get('/reports/hotspots');
  // Normalize items
  return (data.items || []).map((h) => ({
    id: h.report_id,
    lat: h.latitude,
    lng: h.longitude,
    // normalize confidence to 0..1; backend may return 0..1 or 0..100
    confidence: (() => {
      const raw = Number(h.confidence);
      if (!isFinite(raw)) return 0;
      const val = raw > 1 ? raw / 100 : raw;
      return Math.max(0, Math.min(1, val));
    })(),
    hazardType: h.hazard_type,
    status: h.status,
    createdAt: h.created_at,
  }));
};

export const fetchRecentReports = async (limit = 10) => {
  const { data } = await api.get('/reports/recent', { params: { limit } });
  return (data.items || []).map((r) => ({
    id: r.id,
    title: r.hazard_type || 'Hazard Report',
    description: r.user_description || '',
    status: r.status,
    createdAt: r.created_at,
    city: r.user_city || '',
    thumbnailUrl: r.thumbnail_url || null,
  }));
};