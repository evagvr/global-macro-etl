from src.loaders.base_loader import BaseLoader
import pandas as pd
from src.config.database import get_connection
import logging

class MacroLoader(BaseLoader):
    def __init__(self, country: str, indicator_name: str, series_id: str, logger: logging.Logger):
        super().__init__(logger)
        self.country = country
        self.indicator_name = indicator_name
        self.series_id = series_id

    def load(self, df_fred: pd.DataFrame):
        query = """
                    INSERT INTO macro_data (date, series_id, country, indicator_name, value)
                    VALUES %s
                    ON CONFLICT (date, series_id)
                    DO UPDATE SET
                        value = EXCLUDED.value,
                        country = EXCLUDED.country,
                        indicator_name = EXCLUDED.indicator_name
                """
        
        data_list = [
            (
                row.date,
                self.series_id,
                self.country,
                self.indicator_name,
                getattr(row, self.series_id.lower())
            )
            for row in df_fred.itertuples(index=False)
        ]
        self._execute_bulk_insert(query=query, data_list=data_list)
        self.logger.info(f"Loaded {len(df_fred)} macro data rows.")