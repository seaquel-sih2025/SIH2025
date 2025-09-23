import asyncio
import os
from pathlib import Path
from sqlalchemy import text
from app.db.session import engine
from app.db.models import Base

from sqlalchemy import text

async def create_all_tables():
    """Connects to the database and creates all tables."""
    async with engine.begin() as conn:
        print("Dropping all existing tables (with CASCADE)...")
        
        # Use text() to wrap the SQL statements
        await conn.execute(text("DROP TABLE IF EXISTS reports CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS media CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS verifications CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS notifications CASCADE;"))
        
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
    
    # Split the SQL into individual statements
    # Remove comments and empty lines, then split by semicolon
    statements = []
    for line in migration_sql.split('\n'):
        line = line.strip()
        if line and not line.startswith('--'):
            statements.append(line)
    
    # Join lines and split by semicolon to get individual commands
    full_sql = ' '.join(statements)
    individual_statements = [stmt.strip() for stmt in full_sql.split(';') if stmt.strip()]
    
    async with engine.begin() as conn:
        print("🔄 Running migrations...")
        for i, statement in enumerate(individual_statements, 1):
            print(f"   Executing statement {i}/{len(individual_statements)}")
            await conn.execute(text(statement))
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
            print("  python create_tables.py fresh   - Create fresh database (destroys data)")
            print("  python create_tables.py migrate - Run migrations only (preserves data)")
            print("  python create_tables.py reset   - Reset with latest schema (destroys data)")
    else:
        # Default behavior - run migrations (safer default)
        print("🔄 Running database migrations (default behavior)...")
        print("💡 Use 'python create_tables.py fresh' to create fresh database")
        await run_migrations()

if __name__ == "__main__":
    asyncio.run(main())
