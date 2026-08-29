from src.pipeline import ETLPipeline
import pandas as pd
    
def test_conversion_ron_to_eur():
    test_row = pd.Series({
        "close": 100,
        "currency": "RON",
        "RON": 0.20
    })
    result = ETLPipeline._calculate_price_eur(row=test_row)
    assert result == 20.0
def test_conversion_already_eur():
    test_row = pd.Series({
        "close": 100,
        "currency": "EUR",
        "RON": 0.20
    })
    result = ETLPipeline._calculate_price_eur(row=test_row)
    assert result == 100.0
def test_conversion_missing_currency():
    test_row = pd.Series({
        "close": 100,
        "currency": "GBP",
        "RON": 0.20
    })
    result = ETLPipeline._calculate_price_eur(row=test_row)
    assert result is None
