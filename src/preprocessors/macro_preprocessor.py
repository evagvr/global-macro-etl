from src.preprocessors.base_preprocessor import BasePreprocessor
import pandas as pd
import logging

class MacroPreprocessor(BasePreprocessor):
    def __init__(self, series_id: str, logger: logging.Logger):
        super().__init__(logger)
        self.series_id = series_id
        
    def preprocess(self, data: list) -> pd.DataFrame:
        self.logger.info(f"Started preprocessation for FRED series: {self.series_id}")
        df = pd.DataFrame(data)
        df = df.drop(columns=["realtime_start", "realtime_end"])
        df = self._apply_basic_cleaning(df=df)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.rename(columns={"value": self.series_id.lower()})
        self.logger.info(f"Succesfully preprocessed {len(df)} rows for {self.series_id}")
        return df