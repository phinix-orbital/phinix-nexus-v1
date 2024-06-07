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
        type: str,
        target: str | int | float | dict | list | tuple | set | pd.DataFrame,
    ) -> str | int | float | dict | list | tuple | set | pd.DataFrame:
        if type == "read_local":
            _local_files = FileLoader.read_local_file(file_path=os.path.join(GenericHelpers.get_configs_path(), 'extract', 'config_local.yml'))
            _data_fp = _local_files.get(target)
            _data_fp = os.path.join(GenericHelpers.get_base_path(), _data_fp)
            return FileLoader.read_local_file(file_path=_data_fp)
        elif type == "basic":
            return target
    
    @classmethod
    @RunValidator.validate_class_method(check="run_data_validation")
    def run_data_validation(
        cls,
        calibrate: pd.DataFrame,
        schema: dict | pd.DataFrame,
    ) -> None:
        _ = ValidateInputData(calibrate=calibrate, schema=schema).validate_data()
        return calibrate
    
    @classmethod
    @RunValidator.validate_class_method(check="run_fill_na")
    def run_fill_na(
        cls,
        df: pd.DataFrame,
        fill_na_params: dict,
    ) -> pd.DataFrame:
        for _fna_scope, _fna_args in fill_na_params.items():
            for _ftype, _fval in _fna_args.items():
                if _fna_scope == "all_cols":
                    if _ftype == "set_value":
                        df = df.fillna(_fval)
                    else:
                        df = pd.eval(f"df.fillna(df.{_fval}())")
                elif _fna_scope == "subset":
                    if _ftype == "set_value":
                        for _val, _cols in _fval.items():
                            df[_cols] = df[_cols].fillna(_val)
                        else:
                            for _func, _cols in _fval.items():
                                df[_cols] = pd.eval(f"df[_cols].fillna(df[_cols].{_func}())")
                else:
                    for _col_fill, _col_val in _fval.items():
                        df[_col_fill] = df[_col_fill].fillna(df[_col_val])
        return df
