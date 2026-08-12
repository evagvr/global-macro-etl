import pandas as pd
from src.config.database import get_connection
import logging

def load(df_stock: pd.DataFrame, symbol: str, country: str, logger: logging.Logger):
    with get_connection() as connection:
        with connection:
            cursor = connection.cursor()
            for index, row in df_stock.iterrows():
                cursor.execute(
                    """
                    INSERT INTO stock_prices (date, symbol, country, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (date, symbol)
                    DO UPDATE SET country = EXCLUDED.country, open = EXCLUDED.open, high = EXCLUDED.high, low = EXCLUDED.low, close = EXCLUDED.close, volume = EXCLUDED.volume
                    """,
                    (index, symbol, country, float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]), float(row["volume"]))
                )
    logger.info(f"Loaded {len(df_stock)} stock price rows")
                