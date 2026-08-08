from src.extractors.base_extractor import BaseExtractor

class ForexExtractor(BaseExtractor):
    def get_series(self, start_date: str, end_date: str, currencies: str):
        params = dict()
        params["access_key"] = self.api_key
        params["start_date"] = start_date
        params["end_date"] = end_date
        params["currencies"] = currencies
        return self._make_request(params=params)