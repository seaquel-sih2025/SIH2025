import psycopg2
from config import POSTGRES

def get_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=POSTGRES["host"],
        port=POSTGRES["port"],
        database=POSTGRES["database"],
        user=POSTGRES["user"],
        password=POSTGRES["password"]
    )

def create_table():
    """
    Creates the 'scraped_data' table if it doesn't exist and runs
    idempotent migrations to rename old columns and add new ones.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Base table creation
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scraped_data (
        id SERIAL PRIMARY KEY,
        event_type TEXT,
        location TEXT,
        urgency TEXT,
        sentiment TEXT
    );
    """)

    # Idempotent migration to rename old 'tweet_*' columns to 'source_*' if they exist
    cur.execute("""
    DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='scraped_data' AND column_name='tweet_url') THEN
            ALTER TABLE scraped_data RENAME COLUMN tweet_url TO source_url;
        END IF;
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='scraped_data' AND column_name='tweet_created_at') THEN
            ALTER TABLE scraped_data RENAME COLUMN tweet_created_at TO source_created_at;
        END IF;
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='scraped_data' AND column_name='tweet_date') THEN
            ALTER TABLE scraped_data RENAME COLUMN tweet_date TO source_date;
        END IF;
        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='scraped_data' AND column_name='tweet_time') THEN
            ALTER TABLE scraped_data RENAME COLUMN tweet_time TO source_time;
        END IF;
    END;
    $$;
    """)

    # Idempotent migration to add new columns if they don't exist
    cur.execute("""
    ALTER TABLE scraped_data
        ADD COLUMN IF NOT EXISTS source_url TEXT,
        ADD COLUMN IF NOT EXISTS source_created_at TIMESTAMP WITH TIME ZONE,
        ADD COLUMN IF NOT EXISTS source_date DATE,
        ADD COLUMN IF NOT EXISTS source_time TIME;
    """)
    
    conn.commit()
    cur.close()
    conn.close()

def store_scraped_data(payload):
    """
    Inserts a new record into the scraped_data table.
    The function now expects 'source_*' keys in the payload dictionary.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    source_created_at = payload.get("source_created_at")

    cur.execute("""
    INSERT INTO scraped_data (
        event_type, location, urgency, sentiment, source_url, source_created_at, source_date, source_time
    ) VALUES (
        %s, %s, %s, %s, %s, %s,
        (CASE WHEN %s IS NULL THEN NULL ELSE (%s::timestamptz)::date END),
        (CASE WHEN %s IS NULL THEN NULL ELSE (%s::timestamptz)::time END)
    );
    """, (
        payload.get("event_type"),
        payload.get("location"),
        payload.get("urgency"),
        payload.get("sentiment"),
        payload.get("source_url"),
        source_created_at,
        source_created_at, # For casting to date
        source_created_at, # For casting to date
        source_created_at, # For casting to time
        source_created_at  # For casting to time
    ))
    conn.commit()
    cur.close()
    conn.close()