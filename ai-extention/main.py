import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from scraper import fetch_hazard_tweets
from classifier import classify_tweets
# Switch to PostgreSQL storage
from pg_db import init_db, store_scraped_data, get_recent_reports
# Default values (can be overridden by external calls)
DEFAULT_HAZARD_TYPE = "storm"
DEFAULT_LOCATION = "Mumbai"

def run_pipeline(limit=20):
    """
    Main pipeline that reads from reports table and stores output in scraped_data table.
    """
    print("🤖 AI Extension: Starting pipeline...")
    
    # Initialize database
    init_db()
    
    # Get recent reports from the reports table
    reports = get_recent_reports(limit=limit)
    print(f"📊 Found {len(reports)} reports to process")
    
    total_processed = 0
    
    for report in reports:
        print(f"\n🔄 Processing report {report['id']}: {report['user_hazard_type']} in {report['user_city']}")
        
        # Extract parameters from the report
        hazard_type = report['user_hazard_type']
        location = report['user_city']
        latitude = report.get('latitude')
        longitude = report.get('longitude')
        
        try:
            # Fetch and analyze tweets based on the report
            tweets = fetch_hazard_tweets(limit=10, hazard_keywords=hazard_type, location=location)
            results = classify_tweets(tweets)
            
            # Process each tweet result
            for r in results:
                if r.get('hazardous') == 1:
                    # Extract hazard information
                    hazards = (r.get('ner') or {}).get('hazards') or []
                    detected_hazard_type = ", ".join(hazards) if hazards else hazard_type
                    
                    # Extract location information
                    locs = (r.get('ner') or {}).get('locations') or []
                    if not locs and r.get('location'):
                        locs = [r['location']]
                    detected_location = ", ".join(locs) if locs else location
                    
                    # Extract sentiment
                    sentiment = r.get('sentiment') or {"label": "unknown", "score": 0.0}
                    
                    # Process timestamps
                    created_at = r.get('created_at') or ""
                    source_created_at = None
                    source_date = None
                    source_time = None
                    
                    if created_at:
                        dt = None
                        try:
                            dt = parsedate_to_datetime(created_at)
                        except Exception:
                            dt = None
                        if dt is None and 'T' in created_at:
                            try:
                                iso = created_at.replace('Z', '+00:00')
                                dt = datetime.fromisoformat(iso)
                            except Exception:
                                dt = None
                        if dt is not None:
                            source_created_at = dt.isoformat()
                            source_date = dt.date().isoformat()
                            source_time = dt.time().strftime('%H:%M:%S')
                    
                    # Determine urgency based on sentiment and hazard type
                    urgency = determine_urgency(sentiment.get('label', 'unknown'), detected_hazard_type)
                    
                    # Store in scraped_data table
                    store_scraped_data(
                        event_type=detected_hazard_type,
                        location=detected_location,
                        urgency=urgency,
                        sentiment=sentiment.get('label', 'unknown'),
                        source_url=r.get('tweet_url', ''),
                        source_created_at=source_created_at,
                        source_date=source_date,
                        source_time=source_time
                    )
                    
                    total_processed += 1
                    print(f"  ✅ Stored: {detected_hazard_type} in {detected_location}")
            
        except Exception as e:
            print(f"  ❌ Error processing report {report['id']}: {e}")
    
    print(f"\n🎉 Pipeline completed: Processed {total_processed} hazardous tweets")
    return total_processed

def determine_urgency(sentiment, hazard_type):
    """
    Determine urgency level based on sentiment and hazard type.
    """
    # High urgency indicators
    high_urgency_keywords = ['panic', 'emergency', 'urgent', 'critical', 'dangerous']
    high_urgency_hazards = ['tsunami', 'storm_surge', 'coastal_flooding']
    
    sentiment_lower = sentiment.lower()
    hazard_lower = hazard_type.lower()
    
    if any(keyword in sentiment_lower for keyword in high_urgency_keywords):
        return 'High'
    elif any(hazard in hazard_lower for hazard in high_urgency_hazards):
        return 'High'
    elif 'calm' in sentiment_lower or 'normal' in sentiment_lower:
        return 'Low'
    else:
        return 'Medium'

def run_pipeline_with_params(hazard_type=None, location=None, latitude=None, longitude=None, limit=20):
    """
    Wrapper function for run_pipeline that can be called from external sources.
    Now reads from reports table instead of using parameters.
    """
    print(f"🤖 AI Extension: Processing reports from database")
    return run_pipeline(limit=limit)

if __name__ == "__main__":
    output = run_pipeline(limit=20)
    print(f"Processed {output} hazardous tweets from reports")


