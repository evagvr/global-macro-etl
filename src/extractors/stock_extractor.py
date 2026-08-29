from src.extractors.base_extractor import BaseExtractor

class StockExtractor(BaseExtractor):
    def get_series(self, symbol: str, **kwargs):
        params = dict()
        params["symbol"] = symbol
        params["interval"] = "1day"
        params["apikey"] = self.api_key
        params.update(kwargs=kwargs)
        return self._make_request(params=params)