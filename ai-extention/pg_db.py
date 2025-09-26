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
    create_sql = """
    CREATE TABLE IF NOT EXISTS hazardous_tweets (
        id SERIAL PRIMARY KEY,
        tweet_url TEXT UNIQUE,
        hazard_type TEXT,
        location TEXT,
        sentiment_label TEXT,
        sentiment_score DOUBLE PRECISION,
        tweet_date DATE,
        tweet_time TIME,
        inserted_at TIMESTAMPTZ
    );
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)


def upsert_hazardous_tweet(
    *,
    tweet_url: str,
    hazard_type: str,
    location: str,
    sentiment_label: str,
    sentiment_score: float,
    tweet_date: str,
    tweet_time: str,
):
    """
    Insert if new; ignore duplicates based on tweet_url.
    """
    insert_sql = """
    INSERT INTO hazardous_tweets (
        tweet_url, hazard_type, location, sentiment_label, sentiment_score,
        tweet_date, tweet_time, inserted_at
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (tweet_url) DO NOTHING;
    """
    # Convert date/time strings to PostgreSQL-friendly formats
    date_val = tweet_date if tweet_date else None
    time_val = tweet_time if tweet_time else None
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                insert_sql,
                (
                    tweet_url,
                    hazard_type,
                    location,
                    sentiment_label,
                    float(sentiment_score),
                    date_val,
                    time_val,
                    datetime.utcnow().isoformat(timespec="seconds") + "Z",
                ),
            )


