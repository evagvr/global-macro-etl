from src.loaders.base_loader import BaseLoader
import pandas as pd

class AnalyticsLoader(BaseLoader):
    def __init__(self, logger):
        super().__init__(logger)
    
    def load(self, df_final: pd.DataFrame):
        query = """
                    INSERT INTO --- (date, symbol, country, price, currency, price_eur, , , )
                    VALUES %s
                    ON CONFLICT (date, symbol)
                    DO UPDATE SET
                        - = EXCLUDED.
                """
        data_list = [
            (
                row.date,
                row.symbol,
                row.country,
                row.close,
                row.currency,
                row.price_eur,
                
                
            )
            for row in df_final.itertuples(index=False)
        ]