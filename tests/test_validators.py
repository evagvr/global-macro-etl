import pytest
import logging
from src.validators.stock_validator import StockValidator
from src.validators.forex_validator import ForexValidator
from src.validators.macro_validator import MacroValidator

def test_validator_detects_negative_price(logger: logging.Logger):
    validator = StockValidator(logger=logger)
    
    fake_api_data = {
        "values": [
            {
                "datetime": "2023-01-01", 
                "open": "-100", 
                "high": "110", 
                "low": "90", 
                "close": "105", 
                "volume": "1000"
            }
        ]
    }
    results = validator.validate(fake_api_data)
    
    assert len(results["clean_rows"]) == 0
    assert len(results["negative_values"]) == 1
    assert "-100" in results["negative_values"][0]
    
def test_stock_validator_detects_invalid_date(logger: logging.Logger):
    validator = StockValidator(logger=logger)
    
    fake_api_data = {
        "values": [
            {
                "datetime": "2023-13-01", 
                "open": "100", 
                "high": "110", 
                "low": "90", 
                "close": "105", 
                "volume": "1000"
            }
        ]
    }
    
    results = validator.validate(data=fake_api_data)
    
    assert len(results["clean_rows"]) == 0
    assert len(results["invalid_datetime"]) == 1

def test_stock_validator_accepts_clean_data(logger: logging.Logger):
    validator = StockValidator(logger=logger)
    
    fake_api_data = {
        "values": [
            {
                "datetime": "2023-12-01", 
                "open": "100", 
                "high": "110", 
                "low": "90", 
                "close": "105", 
                "volume": "1000"
            }
        ]
    }
    
    results = validator.validate(data=fake_api_data)
    assert len(results["clean_rows"]) == 1
    
def test_stock_validator_detects_nulls(logger):
    validator = StockValidator(logger)
    
    fake_api_data = {
        "values": [
            {
                "datetime": "2023-01-01", "open": 100, "high": 110, "low": 90, "close": 105, "volume": None
            }
            ]
        }
    
    results = validator.validate(data=fake_api_data)
    
    assert len(results["clean_rows"]) == 0
    assert len(results["empty_fields"]) == 1

def test_forex_validator_detects_negative_rate(logger: logging.Logger):
    validator = ForexValidator(logger=logger)
    
    fake_api_data = {
        "quotes": {
            "2025-01-01": {
                "USDEUR": -5.0
            }
        }
    }
    results = validator.validate(data=fake_api_data)
    
    assert len(results["clean_rows"]) == 0
    assert len(results["negative_values"]) == 1
    assert "-5.0" in results["negative_values"][0]
    
def test_forex_validator_detects_invalid_rate(logger: logging.Logger):
    validator = ForexValidator(logger=logger)
    
    fake_api_data = {
        "quotes": {
            "2025-01-01": {
                "USDEUR": "invalid"
            }
        }
    }
    results = validator.validate(data=fake_api_data)
    
    assert len(results["clean_rows"]) == 0
    assert len(results["invalid_value"]) == 1
    
def test_forex_validator_detects_invalid_date(logger: logging.Logger):
    validator = ForexValidator(logger=logger)
        
    fake_api_data = {
            "quotes": {
                "2025-13-01": {
                    "USDEUR": 1.3
                }
            }
        }
    results = validator.validate(data=fake_api_data)
        
    assert len(results["clean_rows"]) == 0
    assert len(results["invalid_date"]) == 1
    
def test_forex_validator_accepts_clean_data(logger: logging.Logger):
    validator = ForexValidator(logger=logger)
    fake_api_data = {
                "quotes": {
                    "2025-01-01": {
                        "USDEUR": 1.3
                    }
                }
            }
    results = validator.validate(data=fake_api_data)
            
    assert len(results["clean_rows"]) == 1
    
def test_macro_validator_detects_invalid_value(logger: logging.Logger):
    validator = MacroValidator(logger=logger)
    
    fake_api_data = {
        "observations": [
                {
                    "realtime_start": "2013-08-14",
                    "realtime_end": "2013-08-14",
                    "date": "1929-01-01",
                    "value": "."
                }
            ]
        }
    results = validator.validate(data=fake_api_data)
        
    assert len(results["clean_rows"]) == 0
    assert len(results["invalid_values"]) == 1
    assert "." in results["invalid_values"][0]
    
def test_macro_validator_detects_invalid_realtime_start(logger: logging.Logger):
    validator = MacroValidator(logger=logger)
    
    fake_api_data = {
        "observations": [
                {
                    "realtime_start": "2013-13-14",
                    "realtime_end": "2013-08-14",
                    "date": "1929-01-01",
                    "value": "1567.5"
                }
            ]
        }
    results = validator.validate(data=fake_api_data)
        
    assert len(results["clean_rows"]) == 0
    assert len(results["invalid_realtime_start"]) == 1

def test_macro_validator_mixed_batch(logger: logging.Logger):
    validator = MacroValidator(logger=logger)
        
    fake_api_data = {
            "observations": [
                    {
                        "realtime_start": "2013-12-14",
                        "realtime_end": "2013-08-14",
                        "date": "1929-01-01",
                        "value": "1567.5"
                    },
                    {
                        "realtime_start": "2013-12-14",
                        "realtime_end": "2013-13-14",
                        "date": "1929-01-01",
                        "value": "-14.0"
                    },
                ]
            }
    results = validator.validate(data=fake_api_data)
            
    assert len(results["clean_rows"]) == 1
    assert len(results["invalid_realtime_end"]) == 1

def test_stock_validator_empty_data(logger):
    validator = StockValidator(logger)
    fake_api_data = {"values": []}
    results = validator.validate(fake_api_data)
    
    assert len(results["clean_rows"]) == 0