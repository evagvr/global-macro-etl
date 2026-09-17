import pytest
import logging
from src.preprocessors.forex_preprocessor import ForexPreprocessor
from src.preprocessors.macro_preprocessor import MacroPreprocessor
from src.preprocessors.stock_preprocessor import StockPreprocessor
import pandas as pd

def test_forex_preprocessor(logger: logging.Logger):
    preprocessor = ForexPreprocessor(logger=logger)
    
    fake_data = [
        {
            "date": "2023-01-01",
            "USDEUR": 0.92, 
            "USDPLN": 4.1
        }
    ]
    df = preprocessor.preprocess(data=fake_data)
    
    assert "base_currency" in df.columns
    assert "quote_currency" in df.columns
    
    assert df.iloc[0]["base_currency"] == "USD"
    assert df.iloc[0]["quote_currency"] == "EUR"
    
    assert len(df) == 2
    
def test_stock_preprocessor(logger: logging.Logger):
    preprocessor = StockPreprocessor(symbol="AAPL", currency="USD", logger=logger)
    
    fake_data = [
            {
                "datetime": "2023-01-01", 
                "close": "150.0"
            }
        ]
    df = preprocessor.preprocess(data=fake_data)
    
    assert "datetime" not in df.columns
    assert "date" in df.columns
    
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    
    assert df["currency"].iloc[0] == "usd"
    assert df["close"].iloc[0] == 150.0
    
def test_macro_preprocessor(logger: logging.Logger):
    preprocessor = MacroPreprocessor(series_id="GDP", logger=logger)
    
    fake_data = [
            {
                "realtime_start": "2023-01-01",
                "realtime_end": "2023-01-01",
                "date": "2023-01-01", 
                "value": "21000.5"
            }
        ]
    df = preprocessor.preprocess(data=fake_data)
    
    assert "realtime_start" not in df.columns
    assert "realtime_end" not in df.columns
    
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df["gdp"].iloc[0] == 21000.5
    
