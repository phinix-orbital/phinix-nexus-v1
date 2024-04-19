import pandas as pd
import re
from mappers.pandas_filter_mappers import PandasFiltersMapperFactory
from validators.run_validator import RunValidator

class PandasModuleWrapper:

    @RunValidator.validate_class_method(check="convert_key_to_pandas_filter")
    @classmethod
    def convert_key_to_pandas_filter(
        cls,
        filter_name: str,
        include: bool = True,
    ) -> str:
        filter_name = filter_name.lower()
        _dict_mappers = PandasFiltersMapperFactory.get_mapper_classes()
        _filter = _dict_mappers.get(filter_name)
        if include:
            _filter += "="
        return _filter
    
    @RunValidator.validate_class_method(check="create_filter_condition")
    @classmethod
    def create_filter_condition(
        cls,
        dict_filter_params: dict,
        df_name: str = "df",
    ) -> str:
        _dict_filters_to_apply = dict()
        for _fname, _fparams in dict_filter_params.keys():
            if _fparams is not None:
                for _col_name, _params in _fparams.items():
                    _fvalues = _params.get("VALUE")
                    _fid = _params.get("ID")
                    if _fname in ["GREATER THAN", "LESS THAN"]:
                        _dict_filter_conversion = {
                            "filter_name" : _fname,
                            "include" : _fparams[_col_name]["INCLUDE"]
                        }
                    else:
                        _dict_filter_conversion = {
                            "filter_name" : _fname,
                        }
                    if _fname in ["STRING CONTAINS", "MATCH IN LIST"]:
                        _filter_string = f"{df_name}['{_col_name}']{cls.convert_key_to_pandas_filter(**_dict_filter_conversion)}({str(_fvalues)})"
                    else:
                        _filter_string = f"{df_name}['{_col_name}']{cls.convert_key_to_pandas_filter(**_dict_filter_conversion)}{_fvalues}"
                    _dict_filters_to_apply[_fid] = _filter_string
        _filter_combo_string = dict_filter_params.get("FILTER_COMBINATION")
        _filter_combo_string = re.sub(fr"\band\b", "&", _filter_combo_string)
        _filter_combo_string = re.sub(fr"\bor\b", "|", _filter_combo_string)
        for _id, _cond in _dict_filters_to_apply.items():
            _filter_combo_string = re.sub(fr"\b{_id}\b", "(" + _cond + ")", _filter_combo_string)
        return f"{df_name}[{_filter_combo_string}]"
    
    @RunValidator.validate_class_method(check="rename_columns")
    @classmethod
    def rename_columns(
        df: pd.DataFrame,
        cols_to_rename: dict,
    ) -> pd.DataFrame:
        df.rename(columns=cols_to_rename, inplace=True)
        return df
    
    @RunValidator.validate_class_method(check="groupby_and_agg")
    @classmethod
    def groupby_and_agg(
        df: pd.DataFrame,
        cols: list,
        agg_dict: dict,
    ) -> pd.DataFrame:
        _col_list = cols + list(agg_dict.keys())
        df = df[_col_list]
        df = df.groupby(by=cols).agg(agg_dict)
        return df
    
    @classmethod
    def fill_na(
        df: pd.DataFrame,
        filla_na_config: dict,
    ) -> pd.DataFrame:
        for _fna_type, _fna_vals in filla_na_config.items():
            _fval: str = list(_fna_vals.keys())[0]
            if _fna_type == "all_cols":
                if _fval == "set_value":
                    df = df.fillna(_fna_vals.get("set_value")) #add pipeline step to transform config to lowercase
                elif _fval == "apply_func":
                    df = pd.eval(f"df.fillna(df.{_fna_vals.get('apply_func')}())", target=df)
            elif _fna_type == "subset":
                if _fval == "set_value":
                    for _val, _col_list in _fna_vals["set_value"].items():
                        df[_col_list] = df[_col_list].fillna(_val)
                elif _fval == "apply_func":
                    for _func, _col_list in _fna_vals["apply_func"].items():
                        df[_col_list] = pd.eval(f"df[_col_list].fillna(df[_col_list].{_func}())", target=df[_col_list])
            elif _fna_type == "other_col":
                for _col_fill, _col_val in _fna_vals.items():
                    df[_col_fill] = df[_col_fill].fillna(df[_col_val])
        return df