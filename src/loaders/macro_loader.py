import pandas as pd
from src.config.database import get_connection
import logging

def load(df_fred: pd.DataFrame, country: str, indicator_name: str, logger: logging.Logger):
    with get_connection() as connection:
        with connection:
            cursor = connection.cursor()
            for index, row in df_fred.iterrows():
                cursor.execute(
                    """
                    INSERT INTO macro_data (date, country, indicator_name, value)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (date, country, indicator_name)
                    DO UPDATE SET value = EXCLUDED.value;
                    """,
                    (index, country, indicator_name, float(row["value"]))
                )
    logger.info(f"Loaded {len(df_fred)} macro data rows.")