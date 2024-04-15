from pydantic import BaseModel, field_validator

class ValidateRunGeValidation(BaseModel):
    ge_result: dict

    @field_validator("ge_result")
    def validate_success_key(
        cls,
        value: dict,
    ) -> None:
        if "success" not in value.keys():
            raise ValueError("'success' not in passed dictionary keys!")
