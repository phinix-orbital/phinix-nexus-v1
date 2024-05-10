import great_expectations as ge
import os
import pandas as pd
from typing import List, Self
import warnings

from pydantic import BaseModel, field_validator, model_validator

from helpers.generic_helpers import GenericHelpers
from stock.variables import DATAFRAMES_INTERACTION_TYPES
from validators.extract_validator import ValidateLocalFilePath

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

class ValidateRunComponent(BaseModel):

    comp_name: str

    @field_validator("comp_name")
    def check_component_existence(cls, value: str) -> None:
        _file_ext = os.path.splitext(value)[1]
        _file_ext = _file_ext[1:]
        if len(_file_ext) == 0:
            value += ".yml"
        else:
            if _file_ext not in ["yml", "yaml"]:
                raise ValueError(f"Component file type must be Yaml!")
        _file_path = os.path.join(GenericHelpers.get_configs_path(), "components", f"{value}")
        _ = ValidateLocalFilePath(file_path=_file_path)

class ValidateRunDataframesInteraction(BaseModel):
    interaction_config: dict
    
    @field_validator("interaction_config")
    def validate_config(cls, value: dict):      
        if "type" not in value.keys() or "parameters" not in value.keys():
            raise ValueError("Dataframe interaction config must contain 'type' and 'parameters' in keys!")
        _int_type = value.get("type")
        if _int_type not in DATAFRAMES_INTERACTION_TYPES:
            raise ValueError(f"{_int_type} is not an accepted dataframe interaction type! Accepted types are {', '.join(DATAFRAMES_INTERACTION_TYPES)}")
        _int_params: dict = value.get("parameters")
        if not isinstance(_int_params, dict):
            raise ValueError("Dataframe interaction params must be a dictionary!")
        df1 = ge.from_pandas(_int_params.get("left_df"))
        df2 = ge.from_pandas(_int_params.get("right_df"))
        if _int_type == "merge":
            _params = ["left_df", "right_df", "join_type", "join_cols"]
            if not set(_params).issubset(set(list(_int_params.keys()))):
                raise ValueError(f" {_int_type} dataframe interaction params dict must contain keys: {', '.join(_params)}")
            if isinstance(_int_params.get("join_cols"), str):
                _join_cols = [_int_params.get("join_cols")]
            elif isinstance(_int_params.get("join_cols"), list):
                _join_cols = _int_params.get("join_cols")
            else:
                raise ValueError("Dataframe interaction parameter 'join_cols' must be of type str or list!")
            for _col in _join_cols:
                GenericHelpers.run_ge_validation(dict(**df1.expect_column_to_exist(_col)))
                GenericHelpers.run_ge_validation(dict(**df2.expect_column_to_exist(_col)))
        elif _int_type == "concat":
            _params = ["list_dfs"]
            if not set(_params).issubset(set(list(_int_params.keys()))):
                raise ValueError(f" {_int_type} dataframe interaction params dict must contain keys: {', '.join(_params)}")
            if not isinstance(_int_params.get("list_dfs"), list):
                raise ValueError("list_dfs parameter value must be of type list!")
            if len(_int_params.get("list_dfs"))<2:
                raise ValueError("list_dfs must contain at least 2 dataframes!")
            if "concat_axis" in _int_params.keys():
                if _int_params.get("concat_axis") not in [0,1]:
                    raise ValueError("concat_axis only accepts 0 or 1!")
                if _int_params.get("concat_axis") == 0:
                    _cols = []
                    for df in _int_params.get("list_dfs"):
                        _cols.append(list(df.columns))
                    if not GenericHelpers.check_if_all_list_elements_same(check_list=_cols):
                        raise ValueError("All dataframes must have the same columns and same column order for concat_axis = 0!")
                else:
                    _len_dfs = []
                    for df in _int_params.get("list_dfs"):
                        _len_dfs.append(len(df))
                        if not GenericHelpers.check_if_all_list_elements_same(check_list=_len_dfs):
                            raise ValueError("All dataframes must have the same length for concat_axis = 1!")
            else:
                _cols = []
                for df in _int_params.get("list_dfs"):
                    _cols.append(list(df.columns))
                if not GenericHelpers.check_if_all_list_elements_same(check_list=_cols):
                    raise ValueError("All dataframes must have the same columns and same column order if concat_axis is not set!")

class ValidateGenerateTemplate(BaseModel):
    template_name: str
    n_files: int | None
    extension: str | None
    list_filenames: List[str] | None

    @model_validator(mode="after")
    def validate_argparser_args(self) -> Self:
        n_files = self.n_files
        _ext = self.extension
        _fnames = self.list_filenames
        if n_files<1:
            raise ValueError("Number of files to generate cannot be less than 1!")
        if _fnames:
            if len(_fnames) != n_files:
                raise ValueError("Number of files arg must be equal to length of file names list!")
            if sum([len(i) for i in _fnames])<len(_fnames):
                raise ValueError("Each element of file names list must contain at least 1 character!")
            if sum([len(i) for i in [os.path.splitext(j)[1] for j in _fnames]]) not in [0, 2*len(_fnames)]:
                raise ValueError("Either all elements or none of file names list must contain extension!")
            if sum([len(i) for i in [os.path.splitext(j)[1] for j in _fnames]]) == 0 and _ext is None:
                raise ValueError("Either extension has to be set or must be specified in each element of file name list!")
            if _ext and sum([len(i) for i in [os.path.splitext(j)[1] for j in _fnames]]) == 2*len(_fnames):
                warnings.warn("Both extension and file names list are set; passed extension will overwrite any specified in list!")
        else:
            if not _ext:
                raise ValueError("Either extension has to be set or must be specified in each element of file name list!")