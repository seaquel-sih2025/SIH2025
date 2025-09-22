#!/usr/bin/env python3
"""
Initialize Twitter Scraper Database
Creates the scraped_data table with proper schema for social media analysis.
"""

import sys
import os

# Add the twitter-scraper directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from db.models import create_table

def main():
    """Initialize the Twitter scraper database."""
    print("🔄 Initializing Twitter scraper database...")
    print("📊 Creating scraped_data table with source_date column...")
    
    try:
        create_table()
        print("✅ Twitter scraper database initialized successfully!")
        print("🎯 The scraped_data table is now ready with columns:")
        print("   - id, event_type, location, urgency, sentiment")
        print("   - source_url, source_created_at, source_date, source_time")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)