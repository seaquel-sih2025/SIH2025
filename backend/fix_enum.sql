-- Quick fix for user_role enum issue
-- Run this SQL script to fix the "authority" role problem

-- Check current enum values
SELECT enumlabel 
FROM pg_enum 
WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'user_role')
ORDER BY enumlabel;

-- Add 'authority' to the enum if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_enum 
        WHERE enumlabel = 'authority' 
        AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'user_role')
    ) THEN
        ALTER TYPE user_role ADD VALUE 'authority';
        RAISE NOTICE 'Added authority to user_role enum';
    ELSE
        RAISE NOTICE 'Authority already exists in user_role enum';
    END IF;
END$$;

-- Migrate any existing 'official' users to 'authority'
UPDATE users SET role = 'authority' WHERE role = 'official';

-- Verify the fix
SELECT enumlabel 
FROM pg_enum 
WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'user_role')
ORDER BY enumlabel;

-- Test that authority role works
SELECT 'authority'::user_role as test_authority_role;

-- Show current user roles
SELECT role, COUNT(*) as count 
FROM users 
GROUP BY role 
ORDER BY role;
