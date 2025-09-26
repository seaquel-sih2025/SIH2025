#!/usr/bin/env python3
import asyncio
import asyncpg
import os
from urllib.parse import urlparse

async def run_migration():
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pravaah_db")
    
    # Parse the URL to extract connection parameters
    parsed = urlparse(database_url)
    
    # Connect to PostgreSQL
    conn = await asyncpg.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:]  # Remove leading slash
    )
    
    try:
        print("🔄 Running signup fix migration...")
        
        # Add missing columns to users table
        migrations = [
            # Add reputation_score and is_verified columns if they don't exist
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'reputation_score'
                ) THEN
                    ALTER TABLE users ADD COLUMN reputation_score INTEGER DEFAULT 100 NOT NULL;
                    PRINT 'Added reputation_score column to users table';
                END IF;
            END $$;
            """,
            
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'is_verified'
                ) THEN
                    ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE NOT NULL;
                    PRINT 'Added is_verified column to users table';
                END IF;
            END $$;
            """,
            
            # Add other missing columns if they don't exist
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'latitude'
                ) THEN
                    ALTER TABLE users ADD COLUMN latitude DECIMAL(10, 8);
                    PRINT 'Added latitude column to users table';
                END IF;
            END $$;
            """,
            
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'longitude'
                ) THEN
                    ALTER TABLE users ADD COLUMN longitude DECIMAL(11, 8);
                    PRINT 'Added longitude column to users table';
                END IF;
            END $$;
            """,
            
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'location_updated_at'
                ) THEN
                    ALTER TABLE users ADD COLUMN location_updated_at TIMESTAMP WITH TIME ZONE;
                    PRINT 'Added location_updated_at column to users table';
                END IF;
            END $$;
            """
        ]
        
        for migration in migrations:
            try:
                await conn.execute(migration)
                print("✅ Executed migration successfully")
            except Exception as e:
                print(f"⚠️  Migration warning: {e}")
                
        print("✅ Signup fix migration completed!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_migration())