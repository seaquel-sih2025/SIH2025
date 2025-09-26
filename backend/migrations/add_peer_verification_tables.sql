-- Create tables for peer verification and safety zone features
-- This migration creates PeerVerification, SafetyZone, SafetyStatus, and MapZone tables

-- Create enum types first (if they don't exist)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'safety_status_enum') THEN
        CREATE TYPE safety_status_enum AS ENUM ('safe', 'warning', 'danger');
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'zone_type_enum') THEN
        CREATE TYPE zone_type_enum AS ENUM ('safe_zone', 'evacuation_zone', 'restricted_zone', 'monitoring_zone');
    END IF;
END $$;

-- Create PeerVerification table
CREATE TABLE IF NOT EXISTS peer_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    verification_type VARCHAR(20) NOT NULL CHECK (verification_type IN ('verify', 'deny')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure a user can only verify/deny a report once
    UNIQUE(report_id, user_id)
);

-- Create SafetyZone table
CREATE TABLE IF NOT EXISTS safety_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    zone_name VARCHAR(255) NOT NULL,
    center_latitude DECIMAL(10, 8) NOT NULL,
    center_longitude DECIMAL(11, 8) NOT NULL,
    radius_meters INTEGER NOT NULL,
    zone_type zone_type_enum NOT NULL DEFAULT 'monitoring_zone',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create SafetyStatus table
CREATE TABLE IF NOT EXISTS safety_statuses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    safety_zone_id UUID NOT NULL REFERENCES safety_zones(id) ON DELETE CASCADE,
    status safety_status_enum NOT NULL DEFAULT 'safe',
    last_checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure a user has only one status per safety zone
    UNIQUE(user_id, safety_zone_id)
);

-- Create MapZone table
CREATE TABLE IF NOT EXISTS map_zones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    zone_name VARCHAR(255) NOT NULL,
    center_latitude DECIMAL(10, 8) NOT NULL,
    center_longitude DECIMAL(11, 8) NOT NULL,
    radius_meters INTEGER NOT NULL,
    zone_type zone_type_enum NOT NULL DEFAULT 'monitoring_zone',
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance (if they don't exist)
DO $$ 
BEGIN
    -- PeerVerification indexes
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_peer_verifications_report_id') THEN
        CREATE INDEX idx_peer_verifications_report_id ON peer_verifications(report_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_peer_verifications_user_id') THEN
        CREATE INDEX idx_peer_verifications_user_id ON peer_verifications(user_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_peer_verifications_type') THEN
        CREATE INDEX idx_peer_verifications_type ON peer_verifications(verification_type);
    END IF;

    -- SafetyZone indexes
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_safety_zones_report_id') THEN
        CREATE INDEX idx_safety_zones_report_id ON safety_zones(report_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_safety_zones_location') THEN
        CREATE INDEX idx_safety_zones_location ON safety_zones(center_latitude, center_longitude);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_safety_zones_active') THEN
        CREATE INDEX idx_safety_zones_active ON safety_zones(is_active);
    END IF;

    -- SafetyStatus indexes
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_safety_statuses_user_id') THEN
        CREATE INDEX idx_safety_statuses_user_id ON safety_statuses(user_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_safety_statuses_zone_id') THEN
        CREATE INDEX idx_safety_statuses_zone_id ON safety_statuses(safety_zone_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_safety_statuses_status') THEN
        CREATE INDEX idx_safety_statuses_status ON safety_statuses(status);
    END IF;

    -- MapZone indexes
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_map_zones_location') THEN
        CREATE INDEX idx_map_zones_location ON map_zones(center_latitude, center_longitude);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_map_zones_active') THEN
        CREATE INDEX idx_map_zones_active ON map_zones(is_active);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_map_zones_type') THEN
        CREATE INDEX idx_map_zones_type ON map_zones(zone_type);
    END IF;
END $$;

-- Add comments for documentation
COMMENT ON TABLE peer_verifications IS 'Tracks user verifications/denials for reports to prevent duplicate voting';
COMMENT ON TABLE safety_zones IS 'Defines geographic safety zones associated with reports';
COMMENT ON TABLE safety_statuses IS 'Tracks user safety status within specific safety zones';
COMMENT ON TABLE map_zones IS 'General-purpose geographic zones for mapping and monitoring';

COMMENT ON COLUMN peer_verifications.verification_type IS 'Type of verification: verify or deny';
COMMENT ON COLUMN safety_zones.radius_meters IS 'Zone radius in meters from center point';
COMMENT ON COLUMN safety_zones.zone_type IS 'Type of safety zone: safe_zone, evacuation_zone, restricted_zone, or monitoring_zone';
COMMENT ON COLUMN map_zones.radius_meters IS 'Zone radius in meters from center point';