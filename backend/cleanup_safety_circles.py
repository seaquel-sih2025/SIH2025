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

            # Find expired safety circles
            result = await db.execute(
                select(SafetyCircle).where(SafetyCircle.created_at < expiration_cutoff)
            )
            expired_circles = result.scalars().all()

            if not expired_circles:
                print("No expired safety circles found.")
                return

            print(f"Found {len(expired_circles)} expired circles to delete.")

            for circle in expired_circles:
                try:
                    # Attempt to delete each circle individually for better error isolation
                    await db.delete(circle)
                    print(f"Deleted expired safety circle ID: {circle.id}")
                except Exception as e:
                    # If an error occurs for one circle, log it and continue
                    print(f"--- FAILED TO DELETE CIRCLE ID: {circle.id} ---")
                    print(f"Error: {e}")
                    # This will help us debug if the data in a specific row is corrupt
                    print(f"Circle Data: {circle.__dict__}")
                    print("-------------------------------------------------")
                    # Rollback this specific failed transaction but continue the loop
                    await db.rollback()


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
