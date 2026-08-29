from src.extractors.macro_extractor import MacroExtractor
from src.extractors.stock_extractor import StockExtractor
from src.extractors.forex_extractor import ForexExtractor
from src.validators.macro_validator import MacroValidator
from src.validators.stock_validator import StockValidator
from src.validators.forex_validator import ForexValidator
from src.transformers.macro_transformer import MacroTransformer
from src.transformers.stock_transformer import StockTransformer
from src.transformers.forex_transformer import ForexTransformer
from src.loaders.macro_loader import MacroLoader
from src.loaders.stock_loader import StockLoader
from src.loaders.forex_loader import ForexLoader
from src.config.settings import settings
from src.utils.logger import get_logger
import os
import yaml
import logging
from datetime import datetime
import pandas as pd

class ETLPipeline:
    def __init__(self, config_path: str="config.yaml"):
        self.logger = get_logger("ETLPipeline")
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.logger.info("Configuration and logger initialized")
        self.macro_extractor = MacroExtractor(
            base_url="https://api.stlouisfed.org/fred/series/observations",
            api_key=settings.fred_api_key,
            logger=self.logger
        )
        self.stock_extractor = StockExtractor(
            base_url="https://api.twelvedata.com/time_series",
            api_key=settings.twelve_data_api_key,
            logger=self.logger
        )
        self.forex_extractor = ForexExtractor(
            base_url="https://api.exchangerate.host/timeframe",
            api_key=settings.exchangerate_access_key,
            logger=self.logger
        )
        self.macro_validator = MacroValidator(
            logger=self.logger
        )
        self.stock_validator = StockValidator(
            logger=self.logger
        )
        self.forex_validator = ForexValidator(
            logger=self.logger
        )
    def run(self):
        self.logger.info(f"Processing forex.")
        try:
            raw_data = self.forex_extractor.get_series(start_date=self.config["settings"]["start_date"], end_date=datetime.now().strftime('%Y-%m-%d'), currencies=self.config["forex"]["symbols"])
            if len(raw_data["quotes"]) == 0:
                self.logger.error("Request for forex returned empty dataset.")
                return
            validations_results = self.forex_validator.validate(data=raw_data)
            if len(validations_results["clean_rows"]) * 0.1 > len(raw_data["quotes"]) - len(validations_results["clean_rows"]):
                cleaned_data = validations_results["clean_rows"]
                transformer = ForexTransformer(logger=self.logger)
                forex_df = transformer.transform(data=cleaned_data)
                forex_to_eur = forex_df[forex_df["quote_currency"] == "EUR"]
                forex_wide = forex_to_eur.pivot(index="date", columns="base_currency", values="rate").reset_index()
                loader = ForexLoader(logger=self.logger)
                loader.load(df_forex=forex_df)
            else:
                self.logger.error(f"The dataset obtained for forex had too many invalid/empty fields")
                return
        except Exception as e:
            self.logger.error("Request for forex returned empty dataset")
            return
        for indicator in self.config["macro_indicators"]:
            self.logger.info(f"Processing macro indicator: {indicator['name']}")
            try:
                raw_data = self.macro_extractor.get_series(series_id=indicator["series_id"], observation_start=self.config["settings"]["start_date"],**indicator["params"])
                if len(raw_data) == 0:
                    self.logger.warning(f"Request for macro indicator: {indicator['name']} returned empty dataset.")
                    continue
                validations_results = self.macro_validator.validate(data=raw_data)
                if len(validations_results["clean_rows"]) * 0.1 > len(raw_data["observations"]) - len(validations_results["clean_rows"]):
                    cleaned_data = validations_results["clean_rows"]
                    transformer = MacroTransformer(series_id=indicator["series_id"], logger=self.logger)
                    transformed_data = transformer.transform(data=cleaned_data)
                    loader = MacroLoader(country=indicator["country"], indicator_name=indicator["name"], series_id=indicator["series_id"], logger=self.logger)
                    loader.load(df_fred=transformed_data)
                else:
                    self.logger.warning(f"The dataset obtained for macro indicator: {indicator['name']} had too many invalid/empty rows.")
                    continue
            except Exception as e:
                self.logger.warning(f"Request for macro indicator: {indicator['name']} failed with error {e}")
                continue
        for equity in self.config["equities"]:
            self.logger.info(f"Processing equity: {equity['name']}")
            try:
                raw_data = self.stock_extractor.get_series(symbol=equity["symbol"], start_date=self.config["settings"]["start_date"])
                if len(raw_data["values"]) == 0:
                    self.logger.warning(f"Request for equity: {equity['name']} returned empty dataset.")
                    continue
                validations_results = self.stock_validator.validate(data=raw_data)
                if (len(validations_results["clean_rows"]) * 0.1 > len(raw_data["values"]) - len(validations_results["clean_rows"])):
                    cleaned_data = validations_results["clean_rows"]
                    transformer = StockTransformer(symbol=equity["symbol"], currency=equity["currency"], logger=self.logger)
                    transformed_data = transformer.transform(data=cleaned_data)
                    temp_df = pd.merge_asof(
                        transformed_data.sort_values("date"), 
                        forex_wide.sort_values("date"), 
                        on="date"
                    )
                    temp_df["price_eur"] = temp_df.apply(
                                self._calculate_price_eur,
                                axis=1
                            )
                    temp_df = temp_df.dropna()
                    loader = StockLoader(symbol=equity["symbol"], country=equity["country"], currency=equity["currency"], logger=self.logger)
                    loader.load(df_stock=temp_df)
                else:
                    self.logger.warning(f"The dataset obtained for equity: {equity['name']} had too many invalid/empty rows.")
                    continue
            except Exception as e:
                self.logger.warning(f"Request for equity: {equity['name']} failed with error {e}")
                continue
    @staticmethod
    def _calculate_price_eur(row: pd.DataFrame) -> float:
        if row["currency"].upper() != "EUR":
            currency = row["currency"]
            price = row["close"]
            if currency.upper() not in row.index:
                return None     
            if pd.isna(row[currency.upper()]):
                return None
            else:
                rate_to_eur = row[currency.upper()]
                price_eur = price * rate_to_eur
                return price_eur
        return row["close"]