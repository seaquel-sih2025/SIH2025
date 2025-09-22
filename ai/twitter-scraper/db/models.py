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
    
    # Drop existing table to ensure clean creation with proper constraints
    cur.execute("DROP TABLE IF EXISTS scraped_data;")
    
    # Create table with proper SERIAL primary key
    cur.execute("""
    CREATE TABLE scraped_data (
        id SERIAL PRIMARY KEY,
        event_type TEXT,
        location TEXT,
        urgency TEXT,
        sentiment TEXT,
        source_url TEXT,
        source_created_at TIMESTAMP WITH TIME ZONE,
        source_date DATE,
        source_time TIME,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """)
    
    print("✅ Created scraped_data table with proper SERIAL ID column")
    conn.commit()
    cur.close()
    conn.close()
    
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