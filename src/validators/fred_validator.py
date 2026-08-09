from src.validators.base_validator import BaseValidator
class FredValidator(BaseValidator):
    def validate(self, data: dict):
        observations = data["observations"]
        empty_fields = self.check_nulls(observations)
        invalid_values = []
        for row in observations:
            try:
                value = float(row["value"])
            except ValueError:
                self.logger.error(f"Found invalid value in observationsL: {row['value']}.")
                invalid_values.append(row["value"])
        validation_results = dict()
        validation_results["empty_fields"] = empty_fields
        validation_results["invalid_values"] = invalid_values
        return validation_results
