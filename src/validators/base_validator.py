import logging
class BaseValidator:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    def check_nulls(self, rows: list):
        empty_keys = []
        for row in rows:
            for key, element in row.items():
                if element is None:
                    self.logger.error(f"Found empty element at {key}")
                    empty_keys.append(key)
        return empty_keys
