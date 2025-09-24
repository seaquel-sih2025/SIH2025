# Hazardous Tweet Pipeline

Scrape tweets about ocean-related hazards, classify them, translate to English, analyze sentiment, extract hazard/location, and store hazardous items in PostgreSQL.

## Features
- Scraper builds a robust query and fetches tweets and metadata
- Classifier (zero-shot) flags hazardous tweets from tweet text
- Translator normalizes text to English (Helsinki-NLP opus-mt)
- Sentiment using GoEmotions mapped to: panic | calm | confusion | neutral | unknown
- NER for locations and hazard keywords with lightweight fallback
- PostgreSQL persistence and viewer tool

## Requirements
- Python 3.12 (virtualenv already present in `class/`)
- Internet access for first-time model downloads
- PostgreSQL 12+ reachable via env vars

## Setup
1) Activate venv (Windows PowerShell):
```powershell
cd "C:\Users\My PC\Desktop\Classifier"
./class/Scripts/Activate.ps1
```

2) Create `.env` in project root:
```
PGHOST=localhost
PGPORT=5432
PGDATABASE=postgres
PGUSER=postgres
PGPASSWORD=your_password
```

Optional (if you want to override the key in code):
```
TWITTER_API_KEY=your_twitterapi_io_key
```

## Run the pipeline
Runs: scrape → classify → (if hazardous) translate → sentiment → NER → store in Postgres.
```powershell
python main.py
```

Output: prints JSON list of processed tweets; hazardous ones are inserted into DB.

## View stored data
```powershell
python view_db.py --limit 100
```

Prints latest rows as JSON.

## Key files
- `scraper.py`: builds query, calls API, normalizes tweets
- `classifier.py`: classifies, translates, sentiment, NER
- `translate.py`: translation helpers
- `sentiment.py`: emotion classification helpers
- `ner.py`: NER + hazard keyword extraction with fallback
- `pg_db.py`: PostgreSQL connection, table creation, upsert
- `main.py`: orchestrates run and persistence
- `view_db.py`: simple DB viewer

## Database
Table: `hazardous_tweets`
- `tweet_url` (unique)
- `hazard_type` (comma-separated if multiple)
- `location` (comma-separated if multiple or author location fallback)
- `sentiment_label` (panic|calm|confusion|neutral|unknown)
- `sentiment_score` (0..1)
- `tweet_date` (DATE)
- `tweet_time` (TIME)
- `inserted_at` (TIMESTAMPTZ)

The table is created automatically on first run.

## Notes
- First run downloads models; allow time.
- If memory is limited, NER falls back to keyword-based location extraction.
- If you change API keys or DB creds, update `.env` and re-run.


