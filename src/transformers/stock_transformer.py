from src.transformers.base_transformer import BaseTransformer
import pandas as pd
import logging

class StockTransformer(BaseTransformer):
    def __init__(self, symbol: str, currency: str, logger: logging.Logger):
        super().__init__(logger)
        self.symbol = symbol
        self.currency = currency
    def transform(self, data: dict) -> pd.DataFrame:
        self.logger.info(f"Started transformation for stock: {self.symbol} ({self.currency})")
        values = data["values"]
        df = pd.DataFrame(values)
        df = df.rename(columns={"datetime": "date"})
        df = self._apply_basic_cleaning(df=df)
        df["currency"] = self.currency.lower()
        df = self._convert_columns_to_float(df=df)
        df = df.drop_duplicates(subset=['date'], keep='last')
        self.logger.info(f"Succesfully transformed {len(df)} rows for {self.symbol} ({self.currency})")
        return df