#!/usr/bin/env python3
"""
Database fix script to resolve the user_role enum issue
This script will update the database to support the new 'authority' role
"""

import asyncio
import sys
from pathlib import Path
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Add the backend directory to the path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.core.config import settings

async def fix_user_role_enum():
    """Fix the user_role enum to support 'authority' instead of 'official'"""
    
    print("🔧 Fixing user_role enum in database...")
    
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    try:
        async with engine.begin() as conn:
            print("📋 Checking current enum values...")
            
            # Check current enum values
            result = await conn.execute(text("""
                SELECT enumlabel 
                FROM pg_enum 
                WHERE enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'user_role'
                )
                ORDER BY enumlabel;
            """))
            
            current_values = [row[0] for row in result.fetchall()]
            print(f"   Current enum values: {current_values}")
            
            # Check if 'authority' already exists
            if 'authority' in current_values:
                print("✅ 'authority' enum value already exists")
                
                # Check if there are any 'official' users to migrate
                result = await conn.execute(text("""
                    SELECT COUNT(*) FROM users WHERE role = 'official';
                """))
                official_count = result.scalar()
                
                if official_count > 0:
                    print(f"🔄 Migrating {official_count} users from 'official' to 'authority'...")
                    await conn.execute(text("""
                        UPDATE users SET role = 'authority' WHERE role = 'official';
                    """))
                    print("✅ User migration completed")
                else:
                    print("✅ No users need migration")
                    
            else:
                print("➕ Adding 'authority' to user_role enum...")
                
                # Add 'authority' to the enum
                await conn.execute(text("""
                    ALTER TYPE user_role ADD VALUE 'authority';
                """))
                print("✅ Added 'authority' to enum")
                
                # Migrate any existing 'official' users
                result = await conn.execute(text("""
                    SELECT COUNT(*) FROM users WHERE role = 'official';
                """))
                official_count = result.scalar()
                
                if official_count > 0:
                    print(f"🔄 Migrating {official_count} users from 'official' to 'authority'...")
                    await conn.execute(text("""
                        UPDATE users SET role = 'authority' WHERE role = 'official';
                    """))
                    print("✅ User migration completed")
            
            # Verify the fix
            print("🔍 Verifying enum values...")
            result = await conn.execute(text("""
                SELECT enumlabel 
                FROM pg_enum 
                WHERE enumtypid = (
                    SELECT oid FROM pg_type WHERE typname = 'user_role'
                )
                ORDER BY enumlabel;
            """))
            
            final_values = [row[0] for row in result.fetchall()]
            print(f"   Final enum values: {final_values}")
            
            # Test inserting a user with 'authority' role
            print("🧪 Testing authority role insertion...")
            test_result = await conn.execute(text("""
                SELECT 'authority'::user_role;
            """))
            print("✅ Authority role test successful")
            
            print("🎉 Database fix completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        return False
    finally:
        await engine.dispose()

async def create_test_authority_user():
    """Create a test authority user to verify the fix"""
    
    print("\n🧪 Creating test authority user...")
    
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    
    try:
        async with engine.begin() as conn:
            # Check if test user already exists
            result = await conn.execute(text("""
                SELECT id FROM users WHERE email = 'test-authority@example.com';
            """))
            
            if result.fetchone():
                print("✅ Test authority user already exists")
                return True
            
            # Create test user
            await conn.execute(text("""
                INSERT INTO users (id, email, full_name, phone, hashed_password, role, is_active)
                VALUES (
                    gen_random_uuid(),
                    'test-authority@example.com',
                    'Test Authority User',
                    '+1234567890',
                    '$2b$12$dummy.hash.for.testing.purposes.only',
                    'authority',
                    true
                );
            """))
            
            print("✅ Test authority user created successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False
    finally:
        await engine.dispose()

async def main():
    """Main function to run all fixes"""
    
    print("🚀 Starting database fix process...\n")
    
    # Fix the enum
    enum_fixed = await fix_user_role_enum()
    
    if enum_fixed:
        # Create test user
        test_created = await create_test_authority_user()
        
        if test_created:
            print("\n🎉 All fixes completed successfully!")
            print("\n📋 What was fixed:")
            print("   ✅ Added 'authority' to user_role enum")
            print("   ✅ Migrated any 'official' users to 'authority'")
            print("   ✅ Created test authority user")
            print("\n🚀 You can now restart your backend server and try registering authority users!")
            return True
    
    print("\n❌ Fix process failed. Please check the errors above.")
    return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
