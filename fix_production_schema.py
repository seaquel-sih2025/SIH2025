#!/usr/bin/env python3
"""
Emergency script to fix production database schema.
The tables exist but are missing columns.
"""
import asyncio
import os
from sqlalchemy import text
from app.db.session import engine
from app.db.models import Base

async def fix_production_schema():
    """Force recreation of all tables with proper schema."""
    print("🚨 EMERGENCY: Fixing production database schema...")
    print("⚠️  This will DROP and RECREATE all tables!")
    
    # Ensure we're using the production database
    db_url = os.getenv("DATABASE_URL")
    if not db_url or "render.com" not in db_url:
        print("❌ ERROR: Not connected to production database!")
        return
    
    print(f"🔗 Connected to: {db_url[:50]}...")
    
    try:
        async with engine.begin() as conn:
            print("🗑️  Dropping all existing tables...")
            
            # Drop all tables in correct order to handle foreign keys
            tables_to_drop = [
                "safety_circles",
                "verifications", 
                "media",
                "reports",
                "users"
            ]
            
            for table in tables_to_drop:
                await conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))
                print(f"   ✓ Dropped table: {table}")
            
            print("🔧 Creating tables with proper schema...")
            
            # Force create all tables
            await conn.run_sync(Base.metadata.create_all)
            print("✅ All tables recreated with complete schema!")
            
            # Verify the users table has all required columns
            result = await conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY ordinal_position;
            """))
            columns = [row[0] for row in result.fetchall()]
            print(f"📋 Users table columns: {columns}")
            
            # Check for critical columns
            required_columns = ['id', 'email', 'role', 'hashed_password', 'full_name']
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"❌ STILL MISSING: {missing_columns}")
                raise Exception(f"Critical columns still missing: {missing_columns}")
            else:
                print("✅ All critical columns present!")
                
    except Exception as e:
        print(f"❌ ERROR during schema fix: {e}")
        raise

if __name__ == "__main__":
    print("Starting emergency schema fix...")
    asyncio.run(fix_production_schema())
    print("🎉 Schema fix complete!")