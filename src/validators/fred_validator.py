from src.validators.base_validator import BaseValidator
from datetime import datetime

class FredValidator(BaseValidator):
    def validate(self, data: dict):
        observations = data["observations"]
        elements_list = ["realtime_start", "realtime_end", "date"]
        validation_results = dict()
        validation_results["empty_fields"] = []
        for element_name in elements_list:
            validation_results["invalid_"+ element_name] = []
        validation_results["invalid_values"] = []
        validation_results["clean_rows"] = []
        for row in observations:
            clean = True
            row_empty_fields = self.check_nulls([row])
            if row_empty_fields:
                clean = False
                validation_results["empty_fields"].append(row)
            for element_name in elements_list:
                if not self.is_valid_date(info="observations", date_str=row[element_name]):
                    clean = False
                    validation_results["invalid_"+ element_name].append(row[element_name])
            if not self.is_numeric(info="observations", value=row["value"]):
                clean = False
                validation_results["invalid_values"].append(row["value"])
            if clean:
                validation_results["clean_rows"].append(row)
        return validation_results
