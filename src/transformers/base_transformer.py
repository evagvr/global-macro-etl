import pandas as pd
import logging

class BaseTransformer:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def _apply_basic_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        df["date"] = pd.to_datetime(df["date"]).dt.normalize()
        return df.sort_values(by="date")

    def _convert_columns_to_float(self, df: pd.DataFrame)-> pd.DataFrame:
        numeric_cols = [col for col in df.columns if col not in ["currency", "date"]]
        df[numeric_cols] = df[numeric_cols].astype(float)
        return df