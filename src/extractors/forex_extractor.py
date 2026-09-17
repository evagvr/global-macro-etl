from src.extractors.base_extractor import BaseExtractor
from datetime import datetime, timedelta
import time

class ForexExtractor(BaseExtractor):
    def get_series(self, start_date: str, end_date: str, currencies: str, base_currency: str):
        curr_start = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        all_quotes = {}
        params = dict()
        params["access_key"] = self.api_key
        params["currencies"] = currencies
        params["source"] = base_currency
        while curr_start <= end_dt:
            curr_end = min(curr_start + timedelta(days=364), end_dt)
            params["start_date"] = curr_start.strftime("%Y-%m-%d")
            params["end_date"] = curr_end.strftime("%Y-%m-%d")
            response = self._make_request(params=params)
            all_quotes.update(response.get("quotes", {}))
            time.sleep(0.5)
            curr_start = curr_end + timedelta(days=1)
        return {"success": True,"quotes": all_quotes}