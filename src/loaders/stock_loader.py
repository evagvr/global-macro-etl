from src.loaders.base_loader import BaseLoader
import pandas as pd
from src.config.database import get_connection
import logging

class StockLoader(BaseLoader):
    def __init__(self, symbol: str, country: str, currency: str, logger: logging.Logger):
        super().__init__(logger)
        self.symbol = symbol
        self.country = country
        self.currency = currency
    def load(self, df_stock: pd.DataFrame):
        data_list = data_list = [
            (
                row.date, 
                self.symbol, 
                self.country, 
                row.open, 
                row.high, 
                row.low, 
                row.close, 
                row.volume,
                self.currency,
                row.price_eur
            ) 
            for row in df_stock.itertuples(index=False)
        ]
        query = """
                    INSERT INTO stock_prices (date, symbol, country, open, high, low, close, volume, currency, price_eur)
                    VALUES %s
                    ON CONFLICT (date, symbol)
                    DO UPDATE SET 
                        country = EXCLUDED.country,
                        open = EXCLUDED.open, 
                        high = EXCLUDED.high, 
                        low = EXCLUDED.low, 
                        close = EXCLUDED.close, 
                        volume = EXCLUDED.volume,
                        currency = EXCLUDED.currency,
                        price_eur = EXCLUDED.price_eur
                """
        self._execute_bulk_insert(query=query, data_list=data_list)
        self.logger.info(f"Loaded {len(df_stock)} stock price rows")