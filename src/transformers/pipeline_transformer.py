from src.transformers.base_transformer import BaseTransformer
import pandas as pd
import numpy as np

class PipelineTransformer(BaseTransformer):
    def __init__(self, df_fred: pd.DataFrame, df_stocks: pd.DataFrame, df_forex: pd.DataFrame):
        self.df_fred = df_fred
        self.df_stocks = df_stocks
        self.df_forex = df_forex

    def _calculate_price_eur(self, row) -> float:
        currency = row["currency"]
        price = row["close"]
        rate_to_eur = row["usdeur"]
        try:
            if currency == "usd":
                return price * rate_to_eur
            else:
                forex_col = f"usd{currency}"
                
                if forex_col not in row  or pd.isna(row[forex_col]):
                    return None
                
                rate_to_usd = row[forex_col]
                return price / rate_to_usd * rate_to_eur
        except Exception:
            self.logger.error(f"Failed conversion for currency {currency} at close {row['close']} on {row['date']}")
            return None

    def merge_all(self) -> pd.DataFrame:
        self.logger.info("Started merge of Stocks, Forex and Macro data.")
        df_merged = pd.merge_asof(left=self.df_stocks, right=self.df_forex, on="date", direction="backward")
        df_merged = pd.merge_asof(left=self.df_merged, right=self.df_fred, on="date", direction="backward")
        df_merged["price_eur"] = df_merged.apply(
            self._calculate_price_eur,
            axis=1
        )
        init_rowcount = len(df_merged)
        df_merged = df_merged.dropna(subset=["price_eur"])
        if init_rowcount > len(df_merged):
            self.logger.warning(f"Dropped {init_rowcount - len(df_merged)} rows due to failed EUR conversion.")
        self.logger.info(f"Merge transformation is completed. Final dataset has {len(df_merged)} rows")
        return df_merged