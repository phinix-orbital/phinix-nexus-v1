import great_expectations as ge
import pandas as pd
from typing import Self

from pydantic import BaseModel, field_validator, model_validator

class ValidateRunGeValidation(BaseModel):
    ge_result: dict

    @field_validator("ge_result")
    def validate_success_key(
        cls,
        value: dict,
    ) -> None:
        if "success" not in value.keys():
            raise ValueError("'success' not in passed dictionary keys!")

class ValidateCalculateIndex(BaseModel):
    base: str | int | float
    value: str | int | float
    df: pd.DataFrame | None
    new_col_name: str | None

    class Config:
        arbitrary_types_allowed = True
    
    @model_validator(mode="after")
    def validate_non_zero_base(self) -> Self:
        df = self.df
        _base = self.base
        _value = self.value
        _new_col_name = self.new_col_name
        if df is None and _base == 0.:
            raise ZeroDivisionError
        if df is not None:
            if isinstance(_base, str) is False or isinstance(_value, str) is False:
                raise ValueError("args 'base' and 'value' must be column names (type: str) when df is passed!")
            if _new_col_name is None:
                raise ValueError("new_col_name arg must be passed when dataframe is passed!")
            df_ge = ge.from_pandas(df)
            for _col in [_base, _value]:
                _ = df_ge.expect_column_to_exist(_col)
        if isinstance(_base, int | float) is True and isinstance(_value, int | float) is False:
            raise ValueError("args 'base' and 'value' must be simultaenously numeric or string!")

class ValidateOrderConfigSteps(BaseModel):
    config: dict

class ValidateCheckIfAllListElementsSame(BaseModel):
    check_list: list

    @field_validator("check_list")
    def check_list_length(cls, value: list):
        if len(value)<2:
            raise ValueError("Length of passed list to check has to be greater or equal to 2!")
