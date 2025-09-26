#!/usr/bin/env python3
"""
Database migration runner for Pravaah backend.
This script runs SQL migration files against the PostgreSQL database.
"""

import asyncio
import asyncpg
import os
from pathlib import Path
from app.core.config import settings

async def run_migration_file(pool, migration_file: Path):
    """Run a single migration file."""
    print(f"Running migration: {migration_file.name}")
    
    # Read the migration file
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Execute the migration
    async with pool.acquire() as connection:
        try:
            # Execute the SQL migration
            await connection.execute(sql_content)
            print(f"✅ Successfully executed {migration_file.name}")
        except Exception as e:
            print(f"❌ Error executing {migration_file.name}: {str(e)}")
            raise

async def run_migrations():
    """Run all pending migrations."""
    # Parse the DATABASE_URL to get connection parameters
    DATABASE_URL = settings.DATABASE_URL
    
    # Convert SQLAlchemy URL to asyncpg format
    if DATABASE_URL.startswith('postgresql+asyncpg://'):
        DATABASE_URL = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
    
    print(f"Connecting to database...")
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(DATABASE_URL)
        
        # Define migration files in order
        migrations_dir = Path(__file__).parent / "migrations"
        migration_files = [
            migrations_dir / "add_user_location_columns.sql",
            migrations_dir / "add_peer_verification_tables.sql"
        ]
        
        print(f"Found {len(migration_files)} migration files to run")
        
        # Run each migration
        for migration_file in migration_files:
            if migration_file.exists():
                await run_migration_file(pool, migration_file)
            else:
                print(f"⚠️  Migration file not found: {migration_file}")
        
        # Close the pool
        await pool.close()
        print("🎉 All migrations completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(run_migrations())