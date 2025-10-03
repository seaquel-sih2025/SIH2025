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
    Ensures the 'scraped_data' table exists with the expected columns.
    Idempotent and non-destructive: will not drop existing data.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scraped_data (
            id SERIAL PRIMARY KEY,
            event_type TEXT,
            location TEXT,
            urgency TEXT,
            sentiment TEXT,
            source_url TEXT,
            source_created_at TIMESTAMPTZ,
            source_date DATE,
            source_time TIME,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    )

    # Add missing columns if they were absent in older runs
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS event_type TEXT;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS location TEXT;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS urgency TEXT;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS sentiment TEXT;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS source_url TEXT;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS source_created_at TIMESTAMPTZ;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS source_date DATE;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS source_time TIME;")
    cur.execute("ALTER TABLE scraped_data ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();")

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