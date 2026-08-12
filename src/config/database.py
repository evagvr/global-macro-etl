import psycopg2
from contextlib import contextmanager
from src.config.settings import settings

@contextmanager
def get_connection():
    connection = psycopg2.connect(host="db", user=settings.postgres_user, password=settings.postgres_password, dbname=settings.postgres_db, port=5432)
    try:
        yield connection
    finally:
        connection.close()

def create_tables():
    with get_connection() as connection:
        with connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS macro_data (
                    date DATE,
                    country TEXT,
                    indicator_name TEXT,
                    value NUMERIC,
                    PRIMARY KEY (date, country, indicator_name)
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS stock_prices (
                    date DATE,
                    symbol TEXT,
                    country TEXT,
                    open NUMERIC,
                    high NUMERIC,
                    low NUMERIC,
                    close NUMERIC,
                    volume NUMERIC,
                    PRIMARY KEY (date, symbol)
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS forex_rates (
                    date DATE,
                    currency_pair TEXT,
                    rate NUMERIC,
                    PRIMARY KEY (date, currency_pair)
                )
                """
            )
        