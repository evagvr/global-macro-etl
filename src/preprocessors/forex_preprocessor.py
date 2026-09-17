from src.preprocessors.base_preprocessor import BasePreprocessor
import pandas as pd
import logging

class ForexPreprocessor(BasePreprocessor):
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
    def preprocess(self, data: list) -> pd.DataFrame:
        self.logger.info(f"Started Forex preprocessation.")
        df = pd.DataFrame(data=data)
        df = self._apply_basic_cleaning(df=df)
        df = self._convert_columns_to_float(df=df)
        df = df.melt(
                    id_vars=['date'],
                    var_name="currency_pair",
                    value_name="rate"
                )
        df["base_currency"] = df["currency_pair"].str[:3].str.upper()
        df["quote_currency"] = df["currency_pair"].str[3:].str.upper()
        df = df.drop(columns=["currency_pair"])
        self.logger.info(f"Succesfully preprocessed {len(df)} forex rows.")
        return df