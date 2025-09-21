import psycopg2
from psycopg2 import sql
from config import POSTGRES

DEFAULT_LIMIT = 20


def main() -> None:

    limit_env = os.getenv('VIEW_ALERTS_LIMIT')
    try:
        limit = int(limit_env) if limit_env else DEFAULT_LIMIT
    except ValueError:
        limit = DEFAULT_LIMIT

    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES["host"],
            port=POSTGRES["port"],
            database=POSTGRES["database"],
            user=POSTGRES["user"],
            password=POSTGRES["password"]
        )
        with conn.cursor() as cur:
            # Count total rows
            cur.execute("SELECT COUNT(*) FROM alerts")
            (count_all,) = cur.fetchone()
            print(f"alerts: {count_all} row(s) total")

            # Fetch sample rows using new schema
            cur.execute(
                sql.SQL(
                    """
                    SELECT event_type, location, urgency, sentiment, video_url, video_created_at, video_date, video_time
                    FROM alerts
                    ORDER BY COALESCE(video_created_at, '1970-01-01'::timestamptz) DESC, video_url DESC
                    LIMIT %s
                    """
                ),
                (limit,)
            )
            rows = cur.fetchall()

            if not rows:
                print("No rows to display.")
                return

            print(f"\nShowing up to {limit} row(s):\n")
            for idx, (event_type, location, urgency, sentiment, video_url, video_created_at, video_date, video_time) in enumerate(rows, start=1):
                print(f"[{idx}] Event: {event_type}")
                print(f"     Location: {location}")
                print(f"     Urgency: {urgency}")
                print(f"     Sentiment: {sentiment}")
                print(f"     Video URL: {video_url}")
                print(f"     Video Created At: {video_created_at}")
                print(f"     Video Date: {video_date}")
                print(f"     Video Time: {video_time}\n")

    except Exception as e:
        print(f"Failed to read alerts: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
