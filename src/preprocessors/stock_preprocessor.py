from src.preprocessors.base_preprocessor import BasePreprocessor
import pandas as pd
import logging

class StockPreprocessor(BasePreprocessor):
    def __init__(self, symbol: str, currency: str, logger: logging.Logger):
        super().__init__(logger)
        self.symbol = symbol
        self.currency = currency
    def preprocess(self, data: list) -> pd.DataFrame:
        self.logger.info(f"Started preprocessation for stock: {self.symbol} ({self.currency})")
        df = pd.DataFrame(data=data)
        df = df.rename(columns={"datetime": "date"})
        df = self._apply_basic_cleaning(df=df)
        df["currency"] = self.currency.lower()
        df = self._convert_columns_to_float(df=df)
        df = df.drop_duplicates(subset=['date'], keep='last')
        self.logger.info(f"Succesfully preprocessed {len(df)} rows for {self.symbol} ({self.currency})")
        return df