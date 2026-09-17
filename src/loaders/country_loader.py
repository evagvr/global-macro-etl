from src.loaders.base_loader import BaseLoader
import pandas as pd

class CountryLoader(BaseLoader):
    def __init__(self, logger):
        super().__init__(logger)
    
    def load(self, df_final: pd.DataFrame):
        query = """
            INSERT INTO dim_countries (country, macro_region)
            VALUES %s
            ON CONFLICT (country)
            DO UPDATE SET
                macro_region = EXCLUDED.macro_region
        """
        data_list = [
            (
                row.country,
                row.macro_region
            )
            for row in df_final.itertuples(index=False)
        ]
        self._execute_bulk_insert(query=query, data_list=data_list)
        self.logger.info(f"Loaded {len(data_list)} countries into dim_countries.")