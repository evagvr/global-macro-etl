from src.loaders.base_loader import BaseLoader
import pandas as pd
from src.config.database import get_connection
import logging

class ForexLoader(BaseLoader):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)

    def load(self, df_forex: pd.DataFrame):
        query = """
                    INSERT INTO forex_rates (date, base_currency, quote_currency, rate)
                    VALUES %s
                    On CONFLICT (date, base_currency, quote_currency)
                    DO UPDATE SET
                        rate = EXCLUDED.rate
                """
        data_list = [
                (
                    row.date,
                    row.base_currency,
                    row.quote_currency,
                    row.rate
                )
                for row in df_forex.itertuples(index=False)
            ]
        self._execute_bulk_insert(query=query, data_list=data_list)
        self.logger.info(f"Loaded {len(df_forex)} forex rate rows")