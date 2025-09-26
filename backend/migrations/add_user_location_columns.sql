-- Add location tracking columns to users table
-- This migration adds latitude, longitude, and location_updated_at columns to support user location features

-- Add columns if they don't exist
DO $$ 
BEGIN
    -- Add latitude column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='latitude') THEN
        ALTER TABLE users ADD COLUMN latitude DECIMAL(10, 8);
    END IF;
    
    -- Add longitude column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='longitude') THEN
        ALTER TABLE users ADD COLUMN longitude DECIMAL(11, 8);
    END IF;
    
    -- Add location_updated_at column
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='users' AND column_name='location_updated_at') THEN
        ALTER TABLE users ADD COLUMN location_updated_at TIMESTAMP WITH TIME ZONE;
    END IF;
END $$;

-- Add index for location-based queries if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_users_location') THEN
        CREATE INDEX idx_users_location ON users (latitude, longitude) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
    END IF;
END $$;

-- Add comments to document the coordinate system
COMMENT ON COLUMN users.latitude IS 'User latitude coordinate in WGS84 (SRID=4326)';
COMMENT ON COLUMN users.longitude IS 'User longitude coordinate in WGS84 (SRID=4326)';
COMMENT ON COLUMN users.location_updated_at IS 'Timestamp when user location was last updated';