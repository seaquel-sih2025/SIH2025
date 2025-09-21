-- Migration to add profile fields to users table
-- Run this script to update existing database

-- Add new columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone VARCHAR(20),
ADD COLUMN IF NOT EXISTS bio VARCHAR(500),
ADD COLUMN IF NOT EXISTS location VARCHAR(255),
ADD COLUMN IF NOT EXISTS profile_picture VARCHAR(500);

-- Add comments for documentation
COMMENT ON COLUMN users.phone IS 'User phone number for contact';
COMMENT ON COLUMN users.bio IS 'User biography/description';
COMMENT ON COLUMN users.location IS 'User location/city';
COMMENT ON COLUMN users.profile_picture IS 'URL to user profile picture';

-- Create index on phone for faster lookups (optional)
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
