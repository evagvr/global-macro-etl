import pandas as pd
from src.config.database import get_connection
import logging
def load(df_forex: pd.DataFrame, logger: logging.Logger):
    with get_connection() as connection:
        with connection:
            cursor = connection.cursor()
            for index, row in df_forex.iterrows():
                for key, value in row.items():
                    cursor.execute(
                        """
                        INSERT INTO forex_rates (date, currency_pair, rate)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (date, currency_pair)
                        DO UPDATE SET rate = EXCLUDED.rate;
                        """,
                        (index, key, value)
                        )
    logger.info(f"Loaded {len(df_forex)} forex rate rows")