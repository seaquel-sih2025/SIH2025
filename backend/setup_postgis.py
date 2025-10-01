#!/usr/bin/env python3
"""
Manual PostGIS setup script for Render PostgreSQL database
Run this script once to enable PostGIS extension
"""
import asyncio
import os
from sqlalchemy import text
from app.db.session import engine

async def setup_postgis():
    """Enable PostGIS extension in the database"""
    try:
        async with engine.begin() as conn:
            print("🔄 Enabling PostGIS extension...")
            
            # Enable PostGIS extension
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            print("✅ PostGIS extension enabled successfully!")
            
            # Enable PostGIS topology (optional but recommended)
            try:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology;"))
                print("✅ PostGIS topology extension enabled!")
            except Exception as e:
                print(f"⚠️  PostGIS topology extension failed (non-critical): {e}")
            
            # Test PostGIS installation
            result = await conn.execute(text("SELECT PostGIS_version();"))
            version = result.scalar()
            print(f"✅ PostGIS version: {version}")
            
    except Exception as e:
        print(f"❌ Error setting up PostGIS: {e}")
        print("\n🔧 Manual setup required:")
        print("1. Go to Render Dashboard → Your PostgreSQL database")
        print("2. Click 'Connect' → 'External Connection' or 'psql'")
        print("3. Run these commands:")
        print("   CREATE EXTENSION IF NOT EXISTS postgis;")
        print("   CREATE EXTENSION IF NOT EXISTS postgis_topology;")
        raise e

async def main():
    if not os.getenv("DATABASE_URL"):
        print("❌ ERROR: DATABASE_URL environment variable is not set!")
        return
        
    print("🚀 Setting up PostGIS for Pravaah database...")
    await setup_postgis()
    print("🎉 PostGIS setup complete!")

if __name__ == "__main__":
    asyncio.run(main())