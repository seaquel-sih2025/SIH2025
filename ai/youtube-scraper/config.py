# YouTube Scraper Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# Database Configuration - Using same database as Twitter scraper and backend
POSTGRES = {
    "host": "localhost",
    "port": 5432,
    "database": "pravaah_db",  # Same as Twitter scraper and backend
    "user": "postgres",
    "password": "atharv"  # Same as Twitter scraper
}

# Analysis Configuration
ALERT_THRESHOLD = 2
SEARCH_TIMEFRAME_HOURS = 48
SEARCH_KEYWORDS = "tsunami | storm surge | coastal flood | cyclone | rogue wave"

