import pandas as pd

from pydantic import BaseModel, field_validator, model_validator, ValidationError

from stock.variables import COMPONENT_OPERATIONS

class ValidateRunGeValidation(BaseModel):
    ge_result: dict

    @field_validator("ge_result")
    def validate_success_key(
        cls,
        value: dict,
    ) -> None:
        if "success" not in value.keys():
            raise ValidationError("'success' not in passed dictionary keys!")

class ValidateCalculateIndex(BaseModel):
    base: str | int | float
    value: str | int | float
    movement_base: str
    df: pd.DataFrame | None
    new_col_name: str | None

    class Config:
        arbitrary_types_allowed = True

    @field_validator("movement_base")
    def check_movement_base_value(cls, value: str):
        if value.lower() not in ["from", "to"]:
            raise ValidationError("movement_base can only be set as 'from' or 'to'!")
    
    @model_validator(mode="after")
    def validate_non_zero_base(
        cls,
        field_values: dict,
    ) -> None:
        df: pd.DataFrame = field_values.get("df")
        _base: bool = field_values.get("base")
        if df is None and _base == 0.:
            raise ZeroDivisionError

class ValidateOrderConfigSteps(BaseModel):
    config: dict

class ValidateCheckIfAllListElementsSame(BaseModel):
    check_list: list

    @field_validator("check_list")
    def check_list_length(cls, value: list):
        if len(value)<2:
            raise ValidationError("Length of passed list to check has to be greater or equal to 2!")
