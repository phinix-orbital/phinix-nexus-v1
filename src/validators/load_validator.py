import great_expectations as ge
import pandas as pd
from pydantic import BaseModel, field_validator, model_validator
from xml.etree.ElementTree import ElementTree

from helpers.generic_helpers import GenericHelpers
from stock.variables import VISUALIZER_PARAMETERS_COLUMNS

class ValidateWriteDataframe(BaseModel):

    output: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

class ValidateWriteString(BaseModel):

    output: str

class ValidateWriteXml(BaseModel):

    output: ElementTree

    class Config:
        arbitrary_types_allowed = True

class ValidateSavePipelineStepOutput(BaseModel):
    pipeline_name: str
    op_name: str
    save_name: str
    output: pd.DataFrame | str | ElementTree
    save_file_path: str | None = None

    class Config:
        arbitrary_types_allowed = True

class ValidateVisualizerParameters(BaseModel):
    params: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True
    
    @field_validator("params")
    def validate_data(
        cls,
        value: pd.DataFrame
    ) -> None:
        data = ge.from_pandas(value)
        for _col in VISUALIZER_PARAMETERS_COLUMNS:
            GenericHelpers.run_ge_validation(dict(**data.expect_column_to_exist(_col)))