import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from scraper import fetch_hazard_tweets
from classifier import classify_tweets
# Switch to PostgreSQL storage
from pg_db import init_db, upsert_hazardous_tweet

def run_pipeline(limit=20):
    tweets = fetch_hazard_tweets(limit=limit)
    results = classify_tweets(tweets)
    init_db()
    for r in results:
        if r.get('hazardous') == 1:
            hazards = (r.get('ner') or {}).get('hazards') or []
            hazard_type = ", ".join(hazards) if hazards else "unknown"
            locs = (r.get('ner') or {}).get('locations') or []
            if not locs and r.get('location'):
                locs = [r['location']]
            location = ", ".join(locs) if locs else "unknown"
            sentiment = r.get('sentiment') or {"label": "unknown", "score": 0.0}
            created_at = r.get('created_at') or ""
            tweet_date = ""
            tweet_time = ""
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
                    tweet_date = dt.date().isoformat()
                    tweet_time = dt.time().strftime('%H:%M:%S')
            upsert_hazardous_tweet(
                tweet_url=r.get('tweet_url') or "",
                hazard_type=hazard_type,
                location=location,
                sentiment_label=sentiment.get('label', 'unknown'),
                sentiment_score=float(sentiment.get('score', 0.0)),
                tweet_date=tweet_date,
                tweet_time=tweet_time,
            )
    return results

if __name__ == "__main__":
    output = run_pipeline(limit=20)
    print(json.dumps(output, indent=2, ensure_ascii=False))


