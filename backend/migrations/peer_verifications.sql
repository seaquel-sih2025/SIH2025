-- backend/migrations/add_peer_verifications.sql
-- Migration to add peer verification and safety zone tables

-- Create peer_verifications table
CREATE TABLE IF NOT EXISTS peer_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    verifier_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    verification_type VARCHAR(20) NOT NULL CHECK (verification_type IN ('verify', 'reject', 'safe', 'not_safe')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', now()) NOT NULL,
    
    -- Ensure user can only verify each report once
    UNIQUE(report_id, verifier_user_id)
);

-- Create safety_zones table
CREATE TABLE IF NOT EXISTS safety_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    zone_type VARCHAR(20) NOT NULL CHECK (zone_type IN ('safe_green', 'unsafe_purple')),
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    radius_meters INTEGER DEFAULT 1000 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', now()) NOT NULL
);

-- Add user location columns to users table (if not already exists)
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS latitude DECIMAL(10, 8),
ADD COLUMN IF NOT EXISTS longitude DECIMAL(11, 8),
ADD COLUMN IF NOT EXISTS location_updated_at TIMESTAMP WITH TIME ZONE;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_peer_verifications_report_id ON peer_verifications(report_id);
CREATE INDEX IF NOT EXISTS idx_peer_verifications_verifier ON peer_verifications(verifier_user_id);
CREATE INDEX IF NOT EXISTS idx_safety_zones_report_id ON safety_zones(report_id);
CREATE INDEX IF NOT EXISTS idx_safety_zones_location ON safety_zones USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_users_location ON users(latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;

-- Add comments for documentation
COMMENT ON TABLE peer_verifications IS 'Stores peer verification responses for reports';
COMMENT ON TABLE safety_zones IS 'Stores safety zones created by user responses';
COMMENT ON COLUMN users.latitude IS 'User current latitude for location-based notifications';
COMMENT ON COLUMN users.longitude IS 'User current longitude for location-based notifications';
COMMENT ON COLUMN users.location_updated_at IS 'Timestamp when user location was last updated';