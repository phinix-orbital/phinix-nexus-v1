import os
import pandas as pd

from helpers.generic_helpers import GenericHelpers
from utils.file_loader import FileLoader
from validators.run_validator import RunValidator
from validators.data_validators.input_data_validator import ValidateInputData

class ComponentOperations:

    @classmethod
    @RunValidator.validate_class_method(check="run_input")
    def run_input(
        cls,
        input_type: str,
        input_target: str | int | float | dict | list | tuple | set | pd.DataFrame,
    ) -> str | int | float | dict | list | tuple | set | pd.DataFrame:
        if input_type == "read_local":
            _local_files = FileLoader.read_local_file(file_path=os.path.join(GenericHelpers.get_configs_path(), 'extract', 'config_local.yml'))
            _data_fp = _local_files.get(input_target)
            _data_fp = os.path.join(GenericHelpers.get_base_path(), _data_fp)
            return FileLoader.read_local_file(file_path=_data_fp)
        elif input_type == "basic":
            return input_target
    
    @classmethod
    @RunValidator.validate_class_method(check="run_data_validation")
    def run_data_validation(
        cls,
        df_calibrate: pd.DataFrame,
        schema: dict | pd.DataFrame,
    ) -> None:
        _ = ValidateInputData(df_calibrate=df_calibrate, schema=schema).validate_data()