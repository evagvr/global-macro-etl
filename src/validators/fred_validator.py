from src.validators.base_validator import BaseValidator
from datetime import datetime
class FredValidator(BaseValidator):
    def validate(self, data: dict):
        observations = data["observations"]
        empty_fields = self.check_nulls(observations)
        elements_list = ["realtime_start", "realtime_end", "date"]
        validation_results = dict()
        validation_results["empty_fields"] = empty_fields
        for element_name in elements_list:
            validation_results["invalid_"+ element_name] = []
        validation_results["invalid_values"] = []
        for row in observations:
            for element_name in elements_list:
                try:
                    element = datetime.strptime(row[element_name], "%Y-%m-%d")
                except ValueError:
                    self.logger.error(f"Found invalid datetime field in observations: {row[element_name]}")
                    validation_results["invalid_"+ element_name].append(row[element_name])
            try:
                value = float(row["value"])
            except ValueError:
                self.logger.error(f"Found invalid value in observations: {row['value']}.")
                validation_results["invalid_values"].append(row["value"])
        return validation_results
