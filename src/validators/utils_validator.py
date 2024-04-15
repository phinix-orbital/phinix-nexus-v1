import logging
import pandas as pd

from pydantic import BaseModel, field_validator, model_validator
from stock.variables import PANDAS_FILTERS

logger = logging.getLogger(__name__)

class ValidateConvertKeyToPandasFilter(BaseModel):
    filter_name: str
    include: bool

    @field_validator("filter_name")
    def validate_filter_key_existence(
        cls,
        value: str,
    ) -> None:
        if value.lower() not in [i.lower() for i in PANDAS_FILTERS]:
            raise ValueError(f"{value} not in implemented list of pandas filters!")
    
    @model_validator(mode="after")
    def validate_fields_combination(
        cls,
        field_values: dict,
    ) -> None:
        _fname: str = field_values.get("filter_name")
        _inc: bool = field_values.get("include")
        if _inc and _fname.lower() not in ["greater than", "less than"]:
            raise ValueError(f"{_fname} is not valid for include = True!")

class ValidateCreateFilterCondition(BaseModel):
    dict_filter_params: dict
    df_name: str

    @field_validator("dict_filter_params")
    def validate_dict_keys_in_pandas_filters(
        cls,
        value: dict,
    ) -> None:
        if not set(value.keys()).issubset(set(PANDAS_FILTERS)):
            raise ValueError("All filters in passed dict must be in PANDAS_FILTERS!")

class ValidateRenameColumns(BaseModel):
    df: pd.DataFrame
    cols_to_rename: dict

    class Config:
        arbitrary_types_allowed = True
    
    @model_validator(mode="after")
    def validate_rename_dict_keys_in_df_columns(
        cls,
        field_values: dict,
    ) -> None:
        df: pd.DataFrame = field_values.get("df")
        _rename_dict: dict = field_values.get("cols_to_rename")
        if not set(_rename_dict.keys()).issubset(set(df.columns)):
            raise ValueError("Not all columns to be renamed are in passed dataframe!")

class ValidateGroupbyAndAgg(BaseModel):
    df: pd.DataFrame
    cols: list
    agg_dict: dict

    class Config:
        arbitrary_types_allowed = True
    
    @model_validator(mode="after")
    def validate_groupby_agg_columns_in_df_columns(
        cls,
        field_values: dict,
    ) -> None:
        
        df: pd.DataFrame = field_values.get("df")
        _cols: list = field_values.get("cols")
        _dict_agg: dict = field_values.get("agg_dict")
        _col_list = _cols + list(_dict_agg.keys())
        if not set(_col_list).issubset(set(df.columns)):
            raise ValueError("Not all columns in groupby and agg are in passed dataframe!")
        if len(_col_list)<len(df.columns):
            logger.warning("Groupby agg columns are a subset of dataframe columns. Some columns will be dropped!")
    
    @model_validator(mode="after")
    def validate_agg_cols_are_numeric(
        cls,
        field_values: dict,
    ) -> None:
        pass