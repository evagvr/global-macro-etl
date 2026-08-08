from src.utils.logger import get_logger
import logging
import requests
import time
class BaseExtractor:
    def __init__(self, base_url: str, api_key: str, logger: logging.Logger):
        self.base_url = base_url
        self.api_key = api_key
        self.logger = logger
    def _make_request(self, params: dict):
        max_attempts = 3
        for attempt in range(max_attempts):
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                self.logger.info(f"Succesfully fetched data from {self.base_url}")
                return response.json()
            else:
                self.logger.error(f"While trying to fetch data from {self.base_url} obtained status code: {response.status_code}")
                if attempt < max_attempts - 1:
                    time.sleep(2 ** attempt)
        raise Exception(f"Failed to fetch data from {self.base_url} after {max_attempts} attempts")
