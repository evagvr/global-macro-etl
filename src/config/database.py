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
                    series_id TEXT,
                    country TEXT,
                    indicator_name TEXT,
                    value NUMERIC,
                    PRIMARY KEY (date, series_id)
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
                    currency TEXT,
                    PRIMARY KEY (date, symbol)
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS forex_rates (
                    date DATE,
                    base_currency TEXT,
                    quote_currency TEXT,
                    rate NUMERIC,
                    PRIMARY KEY (date, base_currency, quote_currency)
                );
                """
            )
            
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS dim_countries (
                    country TEXT PRIMARY KEY,
                    macro_region TEXT
                );
                """
            )
            
            cursor.execute("""
                CREATE OR REPLACE VIEW v_analytics AS
                WITH 
                monthly_stocks AS (
                    SELECT 
                        DATE_TRUNC('month', date) as month,
                        symbol,
                        country, 
                        currency,
                        AVG(close) as avg_price_native
                    FROM stock_prices
                    GROUP BY 1, 2, 3, 4
                ),
                monthly_forex AS (
                    SELECT 
                        DATE_TRUNC('month', date) as month,
                        quote_currency,
                        AVG(rate) as avg_rate
                    FROM forex_rates
                    GROUP BY 1, 2
                ),
                monthly_macro_raw AS (
                    SELECT 
                        DATE_TRUNC('month', date) as month,
                        country,
                        indicator_name,
                        AVG(value) as avg_value
                    FROM macro_data
                    GROUP BY 1, 2, 3
                )
                SELECT 
                    s.month,
                    s.symbol,
                    s.country,
                    s.avg_price_native,
                    s.currency,
                    f.avg_rate as exchange_rate_to_eur,
                    m_inf.avg_value AS inflation,
                    m_rate.avg_value AS policy_rate,
                    CASE 
                        WHEN s.currency = 'EUR' THEN s.avg_price_native
                        ELSE (s.avg_price_native / f.avg_rate) 
                    END as price_eur
                FROM monthly_stocks s
                JOIN dim_countries c ON s.country = c.country
                LEFT JOIN monthly_forex f ON s.month = f.month AND s.currency = f.quote_currency
                LEFT JOIN monthly_macro_raw m_inf 
                    ON s.month = m_inf.month 
                    AND (s.country = m_inf.country OR c.macro_region = m_inf.country)
                    AND m_inf.indicator_name LIKE '%inflation%'
                LEFT JOIN monthly_macro_raw m_rate 
                    ON s.month = m_rate.month 
                    AND c.macro_region = m_rate.country 
                    AND m_rate.indicator_name LIKE '%rate%';
            """)
        