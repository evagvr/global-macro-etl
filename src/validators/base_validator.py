import logging
from datetime import datetime

class BaseValidator:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    def check_nulls(self, rows: list) -> list:
        empty_keys = []
        for row in rows:
            for key, element in row.items():
                if element is None:
                    self.logger.error(f"Found empty element at {key}")
                    empty_keys.append(key)
        return empty_keys
    def is_valid_date(self,info: str, date_str, format="%Y-%m-%d") -> bool:
        try:
            date = datetime.strptime(date_str, format)
        except ValueError:
            self.logger.error(f"Found invalid date field in {info}: {date_str}")
            return False
        return True
    def is_numeric(self, info, value) -> bool:
        try:
            val = float(value)
        except ValueError:
            self.logger.error(f"Found invalid field in {info}: {value}")
            return False
        return True
    def is_positive(self, info, value) -> bool:
        if not self.is_numeric(info, value):
            return False
        val = float(value)
        if val < 0:
            self.logger.error(f"Found negative value in {info}: {value}")
            return False
        return True
