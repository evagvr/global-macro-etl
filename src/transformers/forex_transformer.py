from src.transformers.base_transformer import BaseTransformer
import pandas as pd
import logging

class ForexTransformer(BaseTransformer):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
    def transform(self, data: dict) -> pd.DataFrame:
        self.logger.info(f"Started Forex transformation.")
        quotes = data["quotes"]
        df = pd.DataFrame.from_dict(data=quotes, orient="index").reset_index().rename(columns={"index": "date"})
        df = self._apply_basic_cleaning(df=df)
        df = self._convert_columns_to_float(df=df)
        self.logger.info(f"Succesfully transformed {len(df)} forex rows.")
        return df