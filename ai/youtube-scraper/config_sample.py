# YouTube Scraper Configuration Sample
# Copy this file to config.py and fill in your actual API keys

# API Keys - Get these from the respective services
YOUTUBE_API_KEY = "your_youtube_api_key_here"  # Get from Google Cloud Console
GOOGLE_API_KEY = "your_gemini_api_key_here"    # Get from Google AI Studio

# Database Configuration - Using same database as Twitter scraper and backend
POSTGRES = {
    "host": "localhost",
    "port": 5432,
    "database": "pravaah_db",  # Same as Twitter scraper and backend
    "user": "postgres",
    "password": "your_db_password_here"  # Update this
}

# Analysis Configuration
ALERT_THRESHOLD = 2
SEARCH_TIMEFRAME_HOURS = 48
SEARCH_KEYWORDS = "tsunami | storm surge | coastal flood | cyclone | rogue wave"

