import argparse
import json
from pg_db import get_conn


def fetch_hazardous_tweets(limit: int = 50):
    query = (
        "SELECT tweet_url, hazard_type, location, sentiment_label, sentiment_score, "
        "tweet_date, tweet_time, inserted_at "
        "FROM hazardous_tweets ORDER BY inserted_at DESC LIMIT %s"
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            cols = [
                "tweet_url",
                "hazard_type",
                "location",
                "sentiment_label",
                "sentiment_score",
                "tweet_date",
                "tweet_time",
                "inserted_at",
            ]
            return [dict(zip(cols, row)) for row in rows]


def main():
    parser = argparse.ArgumentParser(description="View hazardous tweets from PostgreSQL")
    parser.add_argument("--limit", type=int, default=50, help="Max rows to display")
    args = parser.parse_args()

    records = fetch_hazardous_tweets(limit=args.limit)
    print(json.dumps(records, indent=2, default=str))


if __name__ == "__main__":
    main()


