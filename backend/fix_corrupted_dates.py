"""
Script to fix corrupted date records in the database.
This addresses the "day is out of range for month" error.
"""
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select, text
from app.db.models import SafetyCircle
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def fix_corrupted_dates():
    """Fix corrupted date records that cause 'day is out of range for month' errors."""
    if not DATABASE_URL:
        print("DATABASE_URL not set, skipping fix.")
        return

    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

    async with AsyncSessionLocal() as db:
        try:
            print("🔍 Checking for corrupted date records...")
            
            # Method 1: Try to identify records with invalid dates using raw SQL
            try:
                # Check for obviously invalid dates
                result = await db.execute(text("""
                    SELECT id, created_at, expires_at 
                    FROM safety_circles 
                    WHERE created_at IS NULL 
                       OR expires_at IS NULL
                       OR created_at > NOW() + INTERVAL '1 year'
                       OR expires_at > NOW() + INTERVAL '1 year'
                       OR created_at < '1900-01-01'
                       OR expires_at < '1900-01-01'
                """))
                
                invalid_records = result.fetchall()
                
                if invalid_records:
                    print(f"Found {len(invalid_records)} records with obviously invalid dates:")
                    for record in invalid_records:
                        print(f"  ID: {record.id}, created_at: {record.created_at}, expires_at: {record.expires_at}")
                else:
                    print("No obviously invalid date records found.")
                    
            except Exception as e:
                print(f"Error checking for invalid dates: {e}")
            
            # Method 2: Try to access all records and identify problematic ones
            print("\n🔍 Scanning all safety circle records...")
            
            try:
                # Get all records in small batches
                offset = 0
                batch_size = 100
                total_processed = 0
                corrupted_ids = []
                
                while True:
                    result = await db.execute(
                        text("SELECT id FROM safety_circles LIMIT :limit OFFSET :offset")
                        .bindparam(limit=batch_size, offset=offset)
                    )
                    batch_ids = [row.id for row in result.fetchall()]
                    
                    if not batch_ids:
                        break
                    
                    print(f"Processing batch {offset//batch_size + 1} ({len(batch_ids)} records)...")
                    
                    for circle_id in batch_ids:
                        try:
                            # Try to fetch and access the record
                            circle_result = await db.execute(
                                select(SafetyCircle).where(SafetyCircle.id == circle_id)
                            )
                            circle = circle_result.scalar_one_or_none()
                            
                            if circle:
                                # Try to access the datetime fields
                                _ = str(circle.created_at)
                                _ = str(circle.expires_at)
                                # Try datetime operations that might trigger the error
                                if circle.created_at:
                                    _ = circle.created_at.year
                                    _ = circle.created_at.month  
                                    _ = circle.created_at.day
                                if circle.expires_at:
                                    _ = circle.expires_at.year
                                    _ = circle.expires_at.month
                                    _ = circle.expires_at.day
                                    
                        except Exception as e:
                            if "day is out of range for month" in str(e):
                                print(f"❌ Found corrupted date record: {circle_id} - {e}")
                                corrupted_ids.append(circle_id)
                            else:
                                print(f"⚠️  Other error for record {circle_id}: {e}")
                    
                    total_processed += len(batch_ids)
                    offset += batch_size
                
                print(f"\n📊 Processed {total_processed} total records")
                print(f"🔍 Found {len(corrupted_ids)} records with corrupted dates")
                
                # Delete corrupted records
                if corrupted_ids:
                    print(f"\n🗑️  Deleting {len(corrupted_ids)} corrupted records...")
                    for corrupted_id in corrupted_ids:
                        try:
                            await db.execute(
                                text("DELETE FROM safety_circles WHERE id = :id")
                                .bindparam(id=corrupted_id)
                            )
                            print(f"✅ Deleted corrupted record: {corrupted_id}")
                        except Exception as e:
                            print(f"❌ Failed to delete {corrupted_id}: {e}")
                    
                    await db.commit()
                    print(f"✅ Successfully deleted {len(corrupted_ids)} corrupted records")
                else:
                    print("✅ No corrupted date records found to delete")
                    
            except Exception as e:
                print(f"❌ Error during record scanning: {e}")
                await db.rollback()
                
        except Exception as e:
            print(f"❌ Critical error during date fix: {e}")
            await db.rollback()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    print("🔧 Running corrupted date fix...")
    asyncio.run(fix_corrupted_dates())
    print("🔧 Corrupted date fix complete.")