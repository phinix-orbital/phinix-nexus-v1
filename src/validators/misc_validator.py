import great_expectations as ge
import pandas as pd

from pydantic import BaseModel, field_validator, ValidationError

from helpers.generic_helpers import GenericHelpers

class ValidateInputDataValidator(BaseModel):
    df_calibrate: pd.DataFrame
    schema: pd.DataFrame | dict

    class Config:
        arbitrary_types_allowed = True
    
    @field_validator("schema")
    def validate_schema_setup(
        cls,
        value: pd.DataFrame | dict,
    ) -> None:
        if isinstance(value, dict):
            if sorted(list(value.keys()))!=["column_name", "column_type"]:
                raise ValidationError("Schema dict must contain keys exclusively from ['column_name', 'column_type']")
        else:
            _schema_data = ge.from_pandas(value)
            for _col in ["column_name", "column_type"]:
                GenericHelpers.run_ge_validation(dict(**_schema_data.expect_column_to_exist(_col)))