import os
import pandas as pd
from typing import Any

from helpers.generic_helpers import GenericHelpers
from utils.file_loader import FileLoader
from validators.run_validator import RunValidator
from validators.data_validators.input_data_validator import ValidateInputData

class PipelineOperations:

    @classmethod
    def run_component(cls, comp_name: str) -> Any:
        pass

    @classmethod
    def run_dataframes_interaction(
        cls,
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        interaction_params: dict,
    ) -> pd.DataFrame:
        pass