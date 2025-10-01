import asyncio
from sqlalchemy import text
from app.db.session import engine
from app.db.models import Base

async def create_all_tables():
    """Connects to the database and creates all tables from SQLAlchemy models."""
    try:
        async with engine.begin() as conn:
            print("🔄 Creating all tables from models...")
            
            # Create all tables defined in models
            await conn.run_sync(Base.metadata.create_all)
            print("✅ All tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise e

async def drop_all_tables():
    """Drops all existing tables and their associated types (for fresh database creation)."""
    async with engine.begin() as conn:
        print("🗑️  Dropping all existing tables (with CASCADE)...")
        
        # Drop tables in correct order to handle foreign key constraints
        await conn.execute(text("DROP TABLE IF EXISTS safety_circles CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS verifications CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS media CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS reports CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        
        print("🧹 Cleaning up composite types...")
        # Drop composite types that PostgreSQL creates automatically for tables
        # This prevents "type already exists" errors when recreating tables
        await conn.execute(text("DROP TYPE IF EXISTS safety_circles CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS verifications CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS media CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS reports CASCADE;"))
        await conn.execute(text("DROP TYPE IF EXISTS users CASCADE;"))
        
        print("✅ All tables and types dropped successfully!")

async def create_fresh_database():
    """Creates a fresh database by dropping and recreating all tables."""
    await drop_all_tables()
    await create_all_tables()
    print("🎉 Fresh database created with latest schema!")

async def main():
    """Main function with options for different operations."""
    import sys
    import os
    
    # Verify DATABASE_URL is available
    if not os.getenv("DATABASE_URL"):
        print("❌ ERROR: DATABASE_URL environment variable is not set!")
        print("Make sure your database is properly configured in Render.")
        sys.exit(1)
    
    print(f"🔗 Using database: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "fresh":
            # Create fresh database (destroys existing data)
            print("🚀 Creating fresh database...")
            await create_fresh_database()
            
        elif command == "create":
            # Create tables only (preserves existing data)
            print("🔄 Creating tables...")
            await create_all_tables()
            
        elif command == "drop":
            # Drop all tables (be careful!)
            print("�️  Dropping all tables...")
            await drop_all_tables()
            
        else:
            print("❌ Unknown command. Available commands:")
            print("  python create_tables.py fresh  - Create fresh database (destroys all data)")
            print("  python create_tables.py create - Create tables only (preserves existing data)")
            print("  python create_tables.py drop   - Drop all tables (destroys all data)")
    else:
        # Default behavior - create tables (safer default)
        print("🔄 Creating database tables (default behavior)...")
        print("💡 Use 'python create_tables.py fresh' to create fresh database")
        await create_all_tables()

if __name__ == "__main__":
    asyncio.run(main())
