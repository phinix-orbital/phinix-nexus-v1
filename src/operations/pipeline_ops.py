import os
import pandas as pd
from typing import Any

from helpers.generic_helpers import GenericHelpers
from orchestrator.config_orchestrator import ConfigOrchestrator
from orchestrator.component_orchestrator import ComponentOrchestrator
from utils.file_loader import FileLoader
from validators.run_validator import RunValidator
from validators.data_validators.input_data_validator import ValidateInputData

class PipelineOperations:

    @classmethod
    @RunValidator.validate_class_method(check="run_component")
    def run_component(cls, comp_name: str) -> Any:
        _file_ext = os.path.splitext(comp_name)[1]
        _file_ext = _file_ext[1:]
        if len(_file_ext) == 0:
            comp_name += comp_name + ".yml"
            _file_ext = "yml"
        _cfg_fp = os.path.join(GenericHelpers.get_configs_path(), "components", f"{comp_name}")
        _cfg = FileLoader.read_local_file(file_path = _cfg_fp)
        _cfg_orc = ConfigOrchestrator(config=_cfg, config_type="component").orchestrate_config()
        return ComponentOrchestrator(config=_cfg_orc).run_component_steps()

    @classmethod
    @RunValidator.validate_class_method(check="run_component")
    def run_dataframes_interaction(
        cls,
        interaction_config: dict,
    ) -> pd.DataFrame:
        _int_type = interaction_config.get("type")
        _int_params: dict = interaction_config.get("parameters")
        if _int_type == "merge":
            _extra_args = dict()
            for k, v in _int_params.items():
                if k not in ["left_df", "right_df", "join_type", "join_cols"]:
                    _extra_args[k] = v
            df1: pd.DataFrame = _int_params.get("left_df")
            df2: pd.DataFrame = _int_params.get("right_df")
            df = df1.merge(df2, how=_int_params.get("join_type"), on=_int_params.get("join_cols"), **_extra_args)
        elif _int_type == "concat":
            _extra_args = dict()
            for k, v in _int_params.items():
                if k not in ["list_dfs"]:
                    _extra_args[k] = v
            df = pd.concat(_int_params.get("list_dfs"), **_extra_args)
        return df