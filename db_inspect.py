"""Minimal PostgreSQL inspection starter."""

import psycopg
from config import DB_CONFIG

def main():
    # TODO: add schema-inspection and profiling queries.
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM support_tickets;")
            print("support_tickets rows:", cur.fetchone()[0])

if __name__ == "__main__":
    main()
