import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from app.db.models import SafetyCircle
from datetime import datetime, timedelta
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def cleanup_expired_safety_circles():
    if not DATABASE_URL:
        print("DATABASE_URL not set, skipping cleanup.")
        return

    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

    async with AsyncSessionLocal() as db:
        try:
            # By default, circles expire after 24 hours.
            expiration_cutoff = datetime.now() - timedelta(days=1)
            
            print(f"Starting cleanup for safety circles created before {expiration_cutoff.isoformat()}")

            # Find expired safety circles with safer query
            try:
                result = await db.execute(
                    select(SafetyCircle).where(SafetyCircle.created_at < expiration_cutoff)
                )
                expired_circles = result.scalars().all()
            except Exception as query_error:
                print(f"Error querying expired circles: {query_error}")
                # Try alternative approach - get all circles and filter manually
                print("Attempting to get all circles and filter manually...")
                result = await db.execute(select(SafetyCircle))
                all_circles = result.scalars().all()
                expired_circles = []
                
                for circle in all_circles:
                    try:
                        if circle.created_at and circle.created_at < expiration_cutoff:
                            expired_circles.append(circle)
                    except Exception as filter_error:
                        print(f"Error checking expiration for circle {circle.id}: {filter_error}")
                        # Add this circle to deletion list since it has invalid dates
                        expired_circles.append(circle)

            if not expired_circles:
                print("No expired safety circles found.")
                return

            print(f"Found {len(expired_circles)} expired circles to delete.")

            for circle in expired_circles:
                try:
                    # Debug: Check if the date values are valid before processing
                    try:
                        created_str = str(circle.created_at) if circle.created_at else "None"
                        expires_str = str(circle.expires_at) if circle.expires_at else "None"
                        print(f"Processing circle ID: {circle.id}, created_at: {created_str}, expires_at: {expires_str}")
                    except Exception as date_error:
                        print(f"Error accessing dates for circle ID: {circle.id}: {date_error}")
                        # Skip this circle if we can't even access its dates
                        continue
                    
                    # Attempt to delete each circle individually for better error isolation
                    await db.delete(circle)
                    print(f"Deleted expired safety circle ID: {circle.id}")
                except Exception as e:
                    # If an error occurs for one circle, log it and continue
                    print(f"--- FAILED TO DELETE CIRCLE ID: {circle.id} ---")
                    print(f"Error: {e}")
                    # This will help us debug if the data in a specific row is corrupt
                    try:
                        circle_data = {k: v for k, v in circle.__dict__.items() if not k.startswith('_')}
                        print(f"Circle Data: {circle_data}")
                    except Exception as dict_error:
                        print(f"Could not access circle data: {dict_error}")
                    print("-------------------------------------------------")
                    # Continue processing other circles


            await db.commit()
            print("Safety circle cleanup complete.")
        except Exception as e:
            # This will catch broader errors, e.g., connection issues
            print(f"A critical error occurred during the cleanup process: {e}")
            await db.rollback()
        finally:
            await engine.dispose()

if __name__ == "__main__":
    print("Running manual cleanup of expired safety circles...")
    asyncio.run(cleanup_expired_safety_circles())

