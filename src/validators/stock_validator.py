from src.validators.base_validator import BaseValidator
from datetime import datetime

class StockValidator(BaseValidator):
    def validate(self, data: dict):
        validation_results = dict()
        validation_results["empty_fields"] = []
        validation_results["invalid_datetime"] = []
        validation_results["clean_rows"] = []
        validation_results["negative_values"] = []
        elements_list = ["open", "high", "low", "close", "volume"]
        for element_name in elements_list:
            validation_results["invalid_" + element_name] = []
        for row in data["values"]:
            clean = True
            row_empty_fields = self.check_nulls([row])
            if row_empty_fields:
                clean = False
                validation_results["empty_fields"].append(row)
            if not self.is_valid_date(info="values", date_str=row["datetime"]):
                clean = False
                validation_results["invalid_datetime"].append(row["datetime"])
            for element_name in elements_list:
                if not self.is_numeric(info="values", value=row[element_name]):
                    clean = False
                    validation_results["invalid_" + element_name].append(row[element_name])
                elif not self.is_positive(info="values", value=row[element_name]):
                    clean = False
                    validation_results["negative_values"].append(f"{row[element_name]}({element_name})")
            if clean:
                validation_results["clean_rows"].append(row)
        return validation_results