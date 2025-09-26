-- Create safety_status table for tracking user safety responses
CREATE TABLE safety_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    is_safe BOOLEAN NOT NULL,
    user_location GEOGRAPHY(POINT, 4326) NOT NULL,
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', now()) NOT NULL
);

-- Create map_zones table for tracking safety/danger zones
CREATE TABLE map_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zone_type VARCHAR(20) NOT NULL CHECK (zone_type IN ('safe', 'danger', 'hazard')),
    center_location GEOGRAPHY(POINT, 4326) NOT NULL,
    radius_meters INTEGER NOT NULL DEFAULT 1000,
    color VARCHAR(7) NOT NULL, -- hex color
    opacity DECIMAL(3,2) NOT NULL DEFAULT 0.3,
    report_id UUID REFERENCES reports(id) ON DELETE SET NULL,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', now()) NOT NULL
);

-- Add location field to users table for proximity notifications
ALTER TABLE users ADD COLUMN IF NOT EXISTS last_known_location GEOGRAPHY(POINT, 4326);
ALTER TABLE users ADD COLUMN IF NOT EXISTS location_updated_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS reputation_score INTEGER DEFAULT 100;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;

-- Create indexes for performance
CREATE INDEX idx_safety_status_user_id ON safety_status(user_id);
CREATE INDEX idx_safety_status_report_id ON safety_status(report_id);
CREATE INDEX idx_safety_status_location ON safety_status USING GIST (user_location);

CREATE INDEX idx_map_zones_location ON map_zones USING GIST (center_location);
CREATE INDEX idx_map_zones_type ON map_zones(zone_type);
CREATE INDEX idx_map_zones_expires ON map_zones(expires_at);

CREATE INDEX idx_users_location ON users USING GIST (last_known_location);
CREATE INDEX idx_users_active_citizens ON users(is_active, role) WHERE role = 'citizen';