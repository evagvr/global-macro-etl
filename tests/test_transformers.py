import pytest
import logging
from src.transformers.forex_transformer import ForexTransformer
from src.transformers.macro_transformer import MacroTransformer
from src.transformers.stock_transformer import StockTransformer
import pandas as pd

def test_forex_transformer(logger: logging.Logger):
    transformer = ForexTransformer(logger=logger)
    
    fake_data = {
        "quotes": {
            "2023-01-01": {
                "USDEUR": 0.92, 
                "USDPLN": 4.1
                }
            }
        }
    df = transformer.transform(data=fake_data)
    
    assert "base_currency" in df.columns
    assert "quote_currency" in df.columns
    
    assert df.iloc[0]["base_currency"] == "USD"
    assert df.iloc[0]["quote_currency"] == "EUR"
    
    assert len(df) == 2
    
def test_stock_transformer(logger: logging.Logger):
    transformer = StockTransformer(symbol="AAPL", currency="USD", logger=logger)
    
    fake_data = {
        "values": [
            {
                "datetime": "2023-01-01", 
                "close": "150.0"
            }
        ]
    }
    df = transformer.transform(data=fake_data)
    
    assert "datetime" not in df.columns
    assert "date" in df.columns
    
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    
    assert df["currency"].iloc[0] == "usd"
    assert df["close"].iloc[0] == 150.0
    
def test_macro_transformer(logger: logging.Logger):
    transformer = MacroTransformer(series_id="GDP", logger=logger)
    
    fake_data = {
        "observations": [
            {
                "realtime_start": "2023-01-01",
                "realtime_end": "2023-01-01",
                "date": "2023-01-01", 
                "value": "21000.5"
            }
        ]
    }
    df = transformer.transform(data=fake_data)
    
    assert "realtime_start" not in df.columns
    assert "realtime_end" not in df.columns
    
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df["gdp"].iloc[0] == 21000.5
    
