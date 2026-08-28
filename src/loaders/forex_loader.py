from src.loaders.base_loader import BaseLoader
import pandas as pd
from src.config.database import get_connection
import logging

class ForexLoader(BaseLoader):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)

    def load(self, df_forex: pd.DataFrame):
        query = """
                    INSERT INTO forex_rates (date, currency_pair, rate)
                    VALUES %s
                    On CONFLICT (date, currency_pair)
                    DO UPDATE SET
                        rate = EXCLUDED.rate
                """
        df_melted = df_forex.melt(
            id_vars=['date'],
            var_name="currency_pair",
            value_name="rate"
        )
        data_list = list(df_melted.itertuples(index=False, name=None))
        self._execute_bulk_insert(query=query, data_list=data_list)
        self.logger.info(f"Loaded {len(df_forex)} forex rate rows")