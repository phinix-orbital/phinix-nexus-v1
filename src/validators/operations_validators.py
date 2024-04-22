import pandas as pd

from pydantic import BaseModel, field_validator, model_validator

class ValidateRunInput(BaseModel):

    type: str
    target: str | int | float | dict | list | tuple | set | pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ValidateRunDataValidation(BaseModel):

    calibrate: pd.DataFrame
    schema: dict | pd.DataFrame

    class Config:
        arbitrary_types_allowed = True