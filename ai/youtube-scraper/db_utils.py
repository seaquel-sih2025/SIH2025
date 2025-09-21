import psycopg2
from psycopg2 import sql
from config import POSTGRES

def get_connection():
    return psycopg2.connect(
        host=POSTGRES["host"],
        port=POSTGRES["port"],
        database=POSTGRES["database"],
        user=POSTGRES["user"],
        password=POSTGRES["password"]
    )


def ensure_schema() -> None:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Create table if it doesn't exist (base columns)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts (
              event_type TEXT,
              location TEXT,
              urgency TEXT,
              sentiment TEXT,
              video_url TEXT,
              video_created_at TIMESTAMPTZ,
              video_date DATE,
              video_time TIME
            );
            """
        )
        # Add columns if missing
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS event_type TEXT;")
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS location TEXT;")
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS urgency TEXT;")
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS sentiment TEXT;")
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS video_url TEXT;")
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS video_created_at TIMESTAMPTZ;")
        # Rename legacy tweet_date/time to video_date/time if they exist
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='alerts' AND column_name='tweet_date';")
        if cur.fetchone():
            cur.execute("ALTER TABLE alerts RENAME COLUMN tweet_date TO video_date;")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='alerts' AND column_name='tweet_time';")
        if cur.fetchone():
            cur.execute("ALTER TABLE alerts RENAME COLUMN tweet_time TO video_time;")
        # Ensure new columns exist after potential rename
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS video_date DATE;")
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS video_time TIME;")

        # Legacy support for link as PK
        cur.execute("ALTER TABLE alerts ADD COLUMN IF NOT EXISTS link TEXT;")
        # Drop any existing PRIMARY KEY constraint
        cur.execute(
            """
            SELECT tc.constraint_name
            FROM information_schema.table_constraints tc
            WHERE tc.table_name = 'alerts' AND tc.constraint_type = 'PRIMARY KEY'
            """
        )
        pk_row = cur.fetchone()
        if pk_row and pk_row[0]:
            cur.execute(sql.SQL("ALTER TABLE alerts DROP CONSTRAINT {};").format(sql.Identifier(pk_row[0])))
        # Make link nullable
        cur.execute("ALTER TABLE alerts ALTER COLUMN link DROP NOT NULL;")
        # Backfill video_url from link
        cur.execute("UPDATE alerts SET video_url = COALESCE(video_url, link) WHERE video_url IS NULL AND link IS NOT NULL;")
        # Ensure unique PK on video_url
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS alerts_video_url_idx ON alerts (video_url);")
        cur.execute("ALTER TABLE alerts ADD CONSTRAINT alerts_pkey PRIMARY KEY (video_url);")

        conn.commit()
    finally:
        if conn:
            conn.close()


def store_alert(alert_data: dict) -> None:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        insert_query = sql.SQL(
            """
            INSERT INTO alerts (event_type, location, urgency, sentiment, video_url, video_created_at, video_date, video_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_url) DO NOTHING;
            """
        )
        cur.execute(
            insert_query,
            (
                alert_data.get('event_type'),
                alert_data.get('location'),
                alert_data.get('urgency'),
                alert_data.get('sentiment'),
                alert_data.get('video_url'),
                alert_data.get('video_created_at'),
                alert_data.get('video_date'),
                alert_data.get('video_time'),
            ),
        )
        conn.commit()
    finally:
        if conn:
            conn.close()
