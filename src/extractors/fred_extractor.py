from src.extractors.base_extractor import BaseExtractor
class FredExtractor(BaseExtractor): 
    def get_series(self, series_id: str):
        params = dict()
        params["series_id"] = series_id
        params["api_key"] = self.api_key
        params["file_type"] = "json"
        return self._make_request(params=params)