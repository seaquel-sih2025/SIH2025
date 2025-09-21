import asyncio
import os
from pathlib import Path
from app.db.session import engine
from app.db.models import Base

async def create_all_tables():
    """Connects to the database and creates all tables."""
    async with engine.begin() as conn:
        print("Dropping all existing tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully.")

async def run_migrations():
    """Run database migrations to add new fields."""
    migration_file = Path(__file__).parent / "migrations" / "add_user_profile_fields.sql"
    
    if not migration_file.exists():
        print(f"❌ Migration file not found: {migration_file}")
        return False
        
    with open(migration_file, 'r') as f:
        migration_sql = f.read()
    
    async with engine.begin() as conn:
        print("🔄 Running migrations...")
        await conn.execute(migration_sql)
        print("✅ Migrations completed successfully!")
        return True

async def main():
    """Main function with options for different operations."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "fresh":
            # Create fresh database (destroys existing data)
            print("🚀 Creating fresh database...")
            await create_all_tables()
            
        elif command == "migrate":
            # Run migrations only (preserves existing data)
            print("🔄 Running database migrations...")
            await run_migrations()
            
        elif command == "reset":
            # Drop, recreate, and migrate (fresh start with latest schema)
            print("🔄 Resetting database with latest schema...")
            await create_all_tables()
            await run_migrations()
            
        else:
            print("❌ Unknown command. Available commands:")
            print("  python create_tables_enhanced.py fresh   - Create fresh database (destroys data)")
            print("  python create_tables_enhanced.py migrate - Run migrations only (preserves data)")
            print("  python create_tables_enhanced.py reset   - Reset with latest schema (destroys data)")
    else:
        # Default behavior - ask user what they want to do
        print("🔧 Database Management Tool")
        print("Choose an option:")
        print("1. Create fresh database (⚠️  DESTROYS existing data)")
        print("2. Run migrations only (✅ Preserves existing data)")
        print("3. Reset with latest schema (⚠️  DESTROYS existing data)")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            await create_all_tables()
        elif choice == "2":
            await run_migrations()
        elif choice == "3":
            await create_all_tables()
            await run_migrations()
        else:
            print("❌ Invalid choice. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
