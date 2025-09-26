-- Migration to update user roles from 'official' to 'authority'
-- Run this script to update existing database

-- First, update the enum type to include 'authority' and remove 'official'
-- Note: PostgreSQL doesn't allow direct enum modification, so we need to:
-- 1. Add the new value
-- 2. Update existing records
-- 3. Remove the old value (if needed)

-- Add 'authority' to the user_role enum if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'authority' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'user_role')) THEN
        ALTER TYPE user_role ADD VALUE 'authority';
    END IF;
END$$;

-- Update any existing 'official' users to 'authority'
UPDATE users SET role = 'authority' WHERE role = 'official';

-- Add comments for documentation
COMMENT ON COLUMN users.role IS 'User role: citizen, authority, or analyst';

-- Create index on role for faster role-based queries
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
