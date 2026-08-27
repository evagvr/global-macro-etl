from src.transformers.base_transformer import BaseTransformer
import pandas as pd

class FredTransformer(BaseTransformer):
    def __init__(self, series_id: str):
        self.series_id = series_id
        
    def transform(self, data: dict) -> pd.DataFrame:
        self.logger.info(f"Started transformation for FRED series: {self.series_id}")
        observations = data["observations"]
        df = pd.DataFrame(observations)
        df = df.drop(columns=["realtime_start", "realtime_end"])
        df = self._apply_basic_cleaning(df=df)
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.rename(columns={"value": self.series_id.lower()})
        self.logger.info(f"Succesfully transformed {len(df)} rows for {self.series_id}")
        return df