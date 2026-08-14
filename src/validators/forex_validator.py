from src.validators.base_validator import BaseValidator
from datetime import datetime

class ForexValidator(BaseValidator):
    def convert(self, data: dict):
        return [{"date": date, **rate} for date, rate in data.items()]
    def validate(self, data: dict):
        quotes = self.convert(data["quotes"])
        validation_results = dict()
        validation_results["empty_fields"] = []
        validation_results["invalid_value"] = []
        validation_results["negative_values"] = [] 
        validation_results["invalid_date"] = []
        validation_results["clean_rows"] = []
        for row in quotes:
            clean = True
            row_empty_fields = self.check_nulls([row])
            if row_empty_fields:
                clean = False
                validation_results["empty_fields"].append(row)
            for key, field in row.items():
                if key == "date":
                    if not self.is_valid_date(info="quotes", date_str=field):
                        clean = False
                        validation_results["invalid_date"].append(field)
                else:
                    if not self.is_numeric(info="quotes", value=field):
                        clean = False
                        validation_results["invalid_value"].append(f"{field}({key})")
                    elif not self.is_positive(info="quotes", value=field):
                        clean = False
                        validation_results["negative_values"].append(f"{field}({key})")
            if clean:
                validation_results["clean_rows"].append(row)
        return validation_results
        