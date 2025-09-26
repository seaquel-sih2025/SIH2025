#!/usr/bin/env python3
"""
Safety Circles Cleanup Script

This script should be run periodically (e.g., via cron job) to clean up
expired safety circles from the database.

Usage:
    python cleanup_safety_circles.py

Cron job example (run every hour):
    0 * * * * cd /path/to/backend && python cleanup_safety_circles.py
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.db.session import async_session
from app.db.models import SafetyCircle
from sqlalchemy.future import select


async def cleanup_expired_safety_circles():
    """Remove safety circles that have expired (older than 48 hours)."""
    try:
        async with async_session() as db:
            current_time = datetime.utcnow()
            
            # Find expired circles
            result = await db.execute(
                select(SafetyCircle)
                .where(SafetyCircle.expires_at <= current_time)
            )
            expired_circles = result.scalars().all()
            
            count = len(expired_circles)
            
            if count > 0:
                # Delete expired circles
                for circle in expired_circles:
                    await db.delete(circle)
                
                await db.commit()
                print(f"[{datetime.now()}] Cleaned up {count} expired safety circles")
            else:
                print(f"[{datetime.now()}] No expired safety circles found")
                
    except Exception as e:
        print(f"[{datetime.now()}] Error during cleanup: {e}")
        return False
    
    return True


async def main():
    """Main function to run the cleanup."""
    print(f"[{datetime.now()}] Starting safety circles cleanup...")
    success = await cleanup_expired_safety_circles()
    
    if success:
        print(f"[{datetime.now()}] Cleanup completed successfully")
        sys.exit(0)
    else:
        print(f"[{datetime.now()}] Cleanup failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())