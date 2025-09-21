#!/usr/bin/env python3
"""
Simple migration script to add user profile fields to the database.
Run this script to update your existing database with the new user profile fields.
"""

import asyncio
import asyncpg
import os
from pathlib import Path

async def run_migration():
    """Run the database migration to add user profile fields."""
    
    # Database connection parameters
    # Update these to match your database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    try:
        # Read the migration SQL file
        migration_file = Path(__file__).parent / "migrations" / "add_user_profile_fields.sql"
        
        if not migration_file.exists():
            print(f"❌ Migration file not found: {migration_file}")
            return False
            
        with open(migration_file, 'r') as f:
            migration_sql = f.read()
        
        print("🔄 Connecting to database...")
        
        # Connect to database
        conn = await asyncpg.connect(DATABASE_URL)
        
        print("🔄 Running migration...")
        
        # Execute the migration
        await conn.execute(migration_sql)
        
        print("✅ Migration completed successfully!")
        print("📋 Added the following fields to users table:")
        print("   - phone (VARCHAR(20))")
        print("   - bio (VARCHAR(500))")
        print("   - location (VARCHAR(255))")
        print("   - profile_picture (VARCHAR(500))")
        
        # Close connection
        await conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    success = asyncio.run(run_migration())
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("You can now use the new user profile features.")
    else:
        print("\n💥 Migration failed. Please check the error messages above.")
        exit(1)
