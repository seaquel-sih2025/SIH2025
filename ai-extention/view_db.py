import argparse
import json
from pg_db import get_conn


def fetch_scraped_data(limit: int = 50):
    """Fetch AI-generated scraped data"""
    query = (
        "SELECT id, event_type, location, urgency, sentiment, source_url, "
        "source_created_at, source_date, source_time, created_at "
        "FROM scraped_data "
        "ORDER BY created_at DESC LIMIT %s"
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            cols = [
                "id",
                "event_type",
                "location",
                "urgency",
                "sentiment",
                "source_url",
                "source_created_at",
                "source_date",
                "source_time",
                "created_at",
            ]
            return [dict(zip(cols, row)) for row in rows]


def fetch_reports(limit: int = 50):
    """Fetch user-generated reports from reports table"""
    query = (
        "SELECT id, user_id, user_hazard_type, user_city, user_description, "
        "latitude, longitude, status, final_confidence_score, created_at "
        "FROM reports ORDER BY created_at DESC LIMIT %s"
    )
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            cols = [
                "id",
                "user_id",
                "user_hazard_type",
                "user_city",
                "user_description",
                "latitude",
                "longitude",
                "status",
                "final_confidence_score",
                "created_at",
            ]
            return [dict(zip(cols, row)) for row in rows]


def get_stats():
    """Get statistics about both reports and scraped_data tables"""
    reports_query = """
    SELECT 
        COUNT(*) as total_reports,
        COUNT(CASE WHEN status = 'under_verification' THEN 1 END) as under_verification,
        COUNT(CASE WHEN status = 'verified' THEN 1 END) as verified,
        COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected
    FROM reports
    """
    
    scraped_query = """
    SELECT 
        COUNT(*) as total_scraped_data,
        COUNT(CASE WHEN urgency = 'High' THEN 1 END) as high_urgency,
        COUNT(CASE WHEN urgency = 'Medium' THEN 1 END) as medium_urgency,
        COUNT(CASE WHEN urgency = 'Low' THEN 1 END) as low_urgency
    FROM scraped_data
    """
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Get reports stats
            cur.execute(reports_query)
            reports_row = cur.fetchone()
            reports_cols = ["total_reports", "under_verification", "verified", "rejected"]
            reports_stats = dict(zip(reports_cols, reports_row))
            
            # Get scraped data stats
            cur.execute(scraped_query)
            scraped_row = cur.fetchone()
            scraped_cols = ["total_scraped_data", "high_urgency", "medium_urgency", "low_urgency"]
            scraped_stats = dict(zip(scraped_cols, scraped_row))
            
            # Combine stats
            return {**reports_stats, **scraped_stats}


def main():
    parser = argparse.ArgumentParser(description="View data from PostgreSQL database")
    parser.add_argument("--limit", type=int, default=50, help="Max rows to display")
    parser.add_argument("--type", choices=["scraped", "reports", "stats"], default="scraped", 
                       help="Type of data to view: scraped (AI-generated scraped data), reports (user reports), stats (statistics)")
    args = parser.parse_args()

    if args.type == "scraped":
        records = fetch_scraped_data(limit=args.limit)
        print("🤖 AI-Generated Scraped Data:")
        print(json.dumps(records, indent=2, default=str))
    elif args.type == "reports":
        records = fetch_reports(limit=args.limit)
        print("📊 User-Generated Reports:")
        print(json.dumps(records, indent=2, default=str))
    elif args.type == "stats":
        stats = get_stats()
        print("📈 Database Statistics:")
        print(json.dumps(stats, indent=2, default=str))


if __name__ == "__main__":
    main()


