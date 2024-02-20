import psycopg2
import os
import time

# Database connection parameters
db_name = os.getenv("POSTGRES_DB", "analys")
db_user = os.getenv("POSTGRES_USER", "futures_user")
db_password = os.getenv("POSTGRES_PASSWORD", "aaa")
db_host = "postgres-db"  # Service name in docker-compose

# SQL for creating tables
create_tables_sql = """
BEGIN;

CREATE TABLE IF NOT EXISTS btc_data (
    timestamp TIMESTAMP NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS eth_data (
    timestamp TIMESTAMP NOT NULL,
    open NUMERIC NOT NULL,
    high NUMERIC NOT NULL,
    low NUMERIC NOT NULL,
    close NUMERIC NOT NULL,
    volume NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS eth_data_filtered (
    timestamp TIMESTAMP NOT NULL,
    eth_close NUMERIC NOT NULL,
    eth_close_filtered NUMERIC NOT NULL
);

COMMIT;
"""


def wait_for_db_to_be_ready(max_attempts=5, delay=5):
    """Checks if the database is ready for connections."""
    for attempt in range(max_attempts):
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
            )
            print("Database is ready!")
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            print(
                f"Database not ready, waiting... Attempt {attempt + 1}/{max_attempts}"
            )
            time.sleep(delay)
    return False


def create_tables():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host
        )
        cursor = conn.cursor()
        cursor.execute(create_tables_sql)
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    if wait_for_db_to_be_ready():
        create_tables()
    else:
        print("Database did not become ready in time. Exiting.")
        exit(1)
