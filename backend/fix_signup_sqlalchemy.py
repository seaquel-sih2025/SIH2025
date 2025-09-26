#!/usr/bin/env python3
import asyncio
import os
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def run_migration():
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:atharv@localhost/pravaah_db")
    
    # Create async engine
    engine = create_async_engine(database_url)
    
    try:
        async with engine.begin() as conn:
            print("🔄 Running signup fix migration...")
            
            # Add missing columns to users table
            migrations = [
                # Add reputation_score column if it doesn't exist
                text("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name = 'users' AND column_name = 'reputation_score'
                        ) THEN
                            ALTER TABLE users ADD COLUMN reputation_score INTEGER DEFAULT 100 NOT NULL;
                            RAISE NOTICE 'Added reputation_score column to users table';
                        ELSE
                            RAISE NOTICE 'reputation_score column already exists';
                        END IF;
                    END $$;
                """),
                
                # Add is_verified column if it doesn't exist
                text("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name = 'users' AND column_name = 'is_verified'
                        ) THEN
                            ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE NOT NULL;
                            RAISE NOTICE 'Added is_verified column to users table';
                        ELSE
                            RAISE NOTICE 'is_verified column already exists';
                        END IF;
                    END $$;
                """),
                
                # Add latitude column if it doesn't exist
                text("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name = 'users' AND column_name = 'latitude'
                        ) THEN
                            ALTER TABLE users ADD COLUMN latitude DECIMAL(10, 8);
                            RAISE NOTICE 'Added latitude column to users table';
                        ELSE
                            RAISE NOTICE 'latitude column already exists';
                        END IF;
                    END $$;
                """),
                
                # Add longitude column if it doesn't exist
                text("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name = 'users' AND column_name = 'longitude'
                        ) THEN
                            ALTER TABLE users ADD COLUMN longitude DECIMAL(11, 8);
                            RAISE NOTICE 'Added longitude column to users table';
                        ELSE
                            RAISE NOTICE 'longitude column already exists';
                        END IF;
                    END $$;
                """),
                
                # Add location_updated_at column if it doesn't exist
                text("""
                    DO $$ 
                    BEGIN 
                        IF NOT EXISTS (
                            SELECT 1 FROM information_schema.columns 
                            WHERE table_name = 'users' AND column_name = 'location_updated_at'
                        ) THEN
                            ALTER TABLE users ADD COLUMN location_updated_at TIMESTAMP WITH TIME ZONE;
                            RAISE NOTICE 'Added location_updated_at column to users table';
                        ELSE
                            RAISE NOTICE 'location_updated_at column already exists';
                        END IF;
                    END $$;
                """)
            ]
            
            for i, migration in enumerate(migrations, 1):
                try:
                    await conn.execute(migration)
                    print(f"✅ Migration {i} executed successfully")
                except Exception as e:
                    print(f"⚠️  Migration {i} warning: {e}")
                    
            print("✅ Signup fix migration completed!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run_migration())