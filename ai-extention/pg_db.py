import os
from contextlib import contextmanager
from datetime import datetime

import psycopg2


def _load_env_file(path: str = ".env"):
    if not os.path.isfile(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
    except Exception:
        pass


def _conn_params():
    # Load .env into environment if present
    _load_env_file()
    return dict(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "postgres"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
    )


@contextmanager
def get_conn():
    conn = psycopg2.connect(**_conn_params())
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    # Create the scraped_data table for AI extension output
    create_sql = """
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
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)


def store_scraped_data(
    *,
    event_type: str,
    location: str,
    urgency: str,
    sentiment: str,
    source_url: str,
    source_created_at: str = None,
    source_date: str = None,
    source_time: str = None,
):
    """
    Store AI-generated scraped data in scraped_data table.
    """
    insert_sql = """
    INSERT INTO scraped_data (
        event_type, location, urgency, sentiment, source_url,
        source_created_at, source_date, source_time
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    # Convert date/time strings to PostgreSQL-friendly formats
    created_at_val = source_created_at if source_created_at else None
    date_val = source_date if source_date else None
    time_val = source_time if source_time else None
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                insert_sql,
                (
                    event_type,
                    location,
                    urgency,
                    sentiment,
                    source_url,
                    created_at_val,
                    date_val,
                    time_val,
                ),
            )

def get_recent_reports(limit: int = 10):
    """
    Get recent reports from the reports table for AI processing.
    """
    query = """
    SELECT id, user_hazard_type, user_city, user_description, 
           latitude, longitude, created_at
    FROM reports 
    WHERE status = 'under_verification' 
    ORDER BY created_at DESC 
    LIMIT %s
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            cols = [
                "id",
                "user_hazard_type", 
                "user_city",
                "user_description",
                "latitude",
                "longitude",
                "created_at"
            ]
            return [dict(zip(cols, row)) for row in rows]


