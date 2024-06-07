import logging
import pandas as pd
import re

from mappers.component_ops_mappers import ComponentMappersFactory
from stock.variables import REPLACE_STEP_COMPONENTS
from validators.run_validator import RunValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComponentOrchestrator:

    @RunValidator.validate_instance_method(check="component_orchestrator")
    def __init__(
            self,
            config: dict,
    ) -> None:
        self.config = config
    
    def _replace_step_with_value(
            self,
            op_name: str,
            op_params: dict,
            step_values: dict,
    ) -> dict:
        
        if op_name == "data_validation":
            for k, v in op_params.items():
                if isinstance(v, str) and v.lower()[0:4] == "step":
                    if v.lower() in step_values.keys():
                        op_params[k] = step_values[v]
                    else:
                        raise ValueError(f"Target step {v} in {op_name} has not been defined in a previous step!")
        elif op_name == "filter_df":
            for _filter, _params in op_params.items():
                if not isinstance(_params, dict):
                    continue
                for _col, _values in _params.items():
                    for k, v in _values.items():
                        if isinstance(v, str) and v.lower()[0:4] == "step":
                            if v.lower() in step_values.keys():
                                op_params[_filter][_col][k] = step_values[v]
                            else:
                                raise ValueError(f"Target step {v} in {op_name} has not been defined in a previous step!")
        elif op_name == "fill_na":
            for _ftype, _params in op_params.items():
                if _ftype == "all_cols":
                    for k, v in _params.items():
                        if isinstance(v, str) and v.lower()[0:4] == "step":
                            if v.lower() in step_values.keys():
                                op_params[_ftype][k] = step_values[v]
                            else:
                                raise ValueError(f"Target step {v} in {op_name} has not been defined in a previous step!")
                elif _ftype == "subset":
                    for _fmethod, _fargs in _params.items():
                        if _fmethod == "set_value":
                            for k in _fargs.keys():
                                if isinstance(k, str) and k.lower()[0:4] == "step":
                                    if k.lower() in step_values.keys():
                                        op_params[_ftype][_fmethod][step_values[k]] = op_params[_ftype][_fmethod][k]
                                        del op_params[_ftype][_fmethod][k]
                                    else:
                                        raise ValueError(f"Target step {v} in {op_name} has not been defined in a previous step!")
        elif op_name == "arithmetic":
            if op_params.get("scope") == "basic":
                _exp: str = op_params.get("expression")
                _exp = _exp.lower()
                _step_idx = [i.start() for i in re.finditer("step", _exp)]
                for i in _step_idx:
                    _step = _exp[i:i+6]
                    if _step in step_values.keys():
                        _exp = re.sub(_step, str(step_values[_step]), _exp)
                    else:
                        raise ValueError(f"Target step {_step} in {op_name} has not been defined in a previous step!")
            elif op_params.get("scope") == "dataframe":
                _operators = [i for i in op_params.keys() if i!="scope"]
                for _op in _operators:
                    for _ix_calc, _calc in enumerate(op_params[_op]):
                        for _ix_elem, _elem in enumerate(_calc):
                            if isinstance(_elem, str) and _elem.lower()[0:4] == "step":
                                if _elem.lower() in step_values.keys():
                                    op_params[_op][_ix_calc][_ix_elem] = step_values[_elem]
                                else:
                                    raise ValueError(f"Target step {_elem} in {op_name} has not been defined in a previous step!")
        return op_params
    
    def _stage_component_op_params(
            self,
            op_name: str,
            op_params: dict,
    ) -> dict:
        
        if op_name in ["input", "data_validation", "select_cols"]:
            return op_params
        elif op_name == "groupby":
            if sorted(list(op_params.keys()))!=["agg_transform", "groupby_cols"]:
                _extra_args = dict()
                _new_keys = [i for i in op_params.keys() if i not in ["agg_transform", "groupby_cols"]]
                for k in _new_keys:
                    _extra_args[k] = op_params[k]
                    del op_params[k]
                op_params["extra_args"] = _extra_args
                return op_params
            else:
                return op_params
        elif op_name == "fill_na":
            return {
                "fill_na_params": op_params
            }
        elif op_name == "filter_df":
            return {
                "filter_params": op_params
            }
        elif op_name == "arithmetic":
            return {
                "arithmetic_params": op_params
            }
        elif op_name == "drop_columns":
            return {
                "list_cols": op_params
            }
        elif op_name == "set_column_type":
            return {
                "col_types": op_params
            }
        elif op_name == "rename_cols":
            return {
                "cols_to_rename": op_params
            }
        elif op_name in ["drop_duplicates", "reset_index"]:
            return {
                "extra_args": op_params
            }
        elif op_name == "pivot_df":
            return {
                "pivot_params": op_params
            }
    
    def run_component_steps(self):
        _step_outputs = dict()
        for _step, _op_cfg in self.config.items():
            logger.info(f"--- Running component {_step}... ---")
            for _op_name, _op_params in _op_cfg.items():
                _op_func = ComponentMappersFactory.get_mapper_classes().get(_op_name)
                if _op_name in REPLACE_STEP_COMPONENTS and _step_outputs:
                    _op_params = self._replace_step_with_value(op_name=_op_name, op_params=_op_params, step_values=_step_outputs)
                _op_params = self._stage_component_op_params(op_name=_op_name, op_params=_op_params)
                if "df" in _step_outputs.keys():
                    if _op_name not in ["input", "data_validation", "arithmetic"]:
                        _op_params["df"] = _step_outputs["df"]
                    if _op_name == "arithmetic" and _op_params["arithmetic_params"]["scope"] == "dataframe":
                        _op_params["df"] = _step_outputs["df"]
            _op_run = _op_func(**_op_params)
            if isinstance(_op_run, pd.DataFrame):
                _step_outputs["df"] = _op_run
            _step_outputs[_step.lower()] = _op_run
            _result = _op_run
        return _result
