from src.validators.base_validator import BaseValidator
from datetime import datetime

class StockValidator(BaseValidator):
    def validate(self, data: dict):
        validation_results = dict()
        validation_results["empty_fields"] = self.check_nulls(data["values"])
        validation_results["invalid_datetime"] = []
        elements_list = ["open", "high", "low", "close", "volume"]
        negative_values = []
        for element_name in elements_list:
            validation_results["invalid_" + element_name] = []
        for row in data["values"]:
            try:
                datetime_value = datetime.strptime(row["datetime"], "%Y-%m-%d")
            except ValueError:
                self.logger.error(f"Found invalid value: {row['datetime']}.")
                validation_results["invalid_datetime"].append(row['datetime'])
            for element_name in elements_list:
                try:
                    element = float(row[element_name])
                    if element < 0:
                        self.logger.error(f"Found negative invalid value: {element}")
                        negative_values.append(element)
                except ValueError:
                    self.logger.error(f"Found invalid value: {row[element_name]}.")
                    validation_results["invalid_" + element_name].append(row[element_name])
        validation_results["negative_values"] = negative_values
        return validation_results