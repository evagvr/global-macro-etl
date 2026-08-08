from src.extractors.base_extractor import BaseExtractor

class StockExtractor(BaseExtractor):
    def get_series(self, symbol: str):
        params = dict()
        params["symbol"] = symbol
        params["interval"] = "1day"
        params["apikey"] = self.api_key
        return self._make_request(params=params)