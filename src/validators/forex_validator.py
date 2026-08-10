from src.validators.base_validator import BaseValidator
from datetime import datetime

class ForexValidator(BaseValidator):
    def validate(self, data: dict):
        quotes = data["quotes"]
        empty_fields = self.check_nulls(list(quotes.values()))
        validation_results = dict()
        validation_results["empty_fields"] = empty_fields
        validation_results["invalid_value"] = []
        validation_results["negative_values"] = [] 
        validation_results["invalid_date"] = []
        for key, _ in quotes.items():
            try:
                date = datetime.strptime(key, "%Y-%m-%d")
            except ValueError:
                self.logger.error(f"Found invalid date field in quotes: {key}")
                validation_results["invalid_date"].append(key)
        for row in list(quotes.values()):
            for field in row.values():
                try:
                    value = float(field)
                    if value < 0:
                        self.logger.error(f"Found negative invalid field in quotes: {value}")
                        validation_results["negative_values"].append(value)
                except ValueError:
                    self.logger.error(f"Found invalid field in quotes: {field}")
                    validation_results["invalid_value"].append(field)
        return validation_results
        