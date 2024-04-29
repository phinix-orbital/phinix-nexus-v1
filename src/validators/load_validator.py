import pandas as pd
from pydantic import BaseModel, field_validator, ValidationError

class ValidateWriteDataframe(BaseModel):

    output: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ValidateWriteString(BaseModel):

    output: str

class ValidateSavePipelineStepOutput(BaseModel):
    pipeline_name: str
    op_name: str
    save_name: str
    output: pd.DataFrame | str
    save_file_path: str | None = None

    class Config:
        arbitrary_types_allowed = True