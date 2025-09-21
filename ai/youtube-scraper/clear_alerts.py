import argparse
import psycopg2
from config import POSTGRES


def get_conn():
    return psycopg2.connect(
        host=POSTGRES["host"],
        port=POSTGRES["port"],
        database=POSTGRES["database"],
        user=POSTGRES["user"],
        password=POSTGRES["password"]
    )


def clear_rows() -> None:
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM alerts;")
        conn.commit()
        print("alerts table cleared (all rows deleted).")
    finally:
        if conn:
            conn.close()


def drop_table() -> None:
    conn = None
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS alerts;")
        conn.commit()
        print("alerts table dropped.")
    finally:
        if conn:
            conn.close()


def main():
    parser = argparse.ArgumentParser(description="Clear or drop alerts table")
    parser.add_argument("--drop", action="store_true", help="Drop the alerts table instead of deleting rows")
    args = parser.parse_args()

    if args.drop:
        drop_table()
    else:
        clear_rows()


if __name__ == "__main__":
    main()
