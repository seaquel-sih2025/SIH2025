-- Migration to update user roles from 'authority' to 'official'
-- Run this script to update existing database

-- First, update the enum type to include 'official' and remove 'authority'
-- Note: PostgreSQL doesn't allow direct enum modification, so we need to:
-- 1. Add the new value
-- 2. Update existing records
-- 3. Remove the old value (if needed)

-- Add 'official' to the user_role enum if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'official' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'user_role')) THEN
        ALTER TYPE user_role ADD VALUE 'official';
    END IF;
END$$;

-- Update any existing 'authority' users to 'official'
UPDATE users SET role = 'official' WHERE role = 'authority';

-- Add comments for documentation
COMMENT ON COLUMN users.role IS 'User role: citizen, official, or analyst';

-- Create index on role for faster role-based queries
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
