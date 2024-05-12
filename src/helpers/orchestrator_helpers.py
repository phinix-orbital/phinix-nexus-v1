import os
import pandas as pd
from pathlib import Path

from helpers.generic_helpers import GenericHelpers
from mappers.loader_mappers import PipelineSaveStepMappersFactory 
from validators.run_validator import RunValidator

class OrchestratorHelpers:
    
    @classmethod
    @RunValidator.validate_class_method(check="order_config_steps")
    def order_config_steps(cls, config: dict):
        _dict_steps = dict()
        _dict_ordered_steps = dict()
        _new_config = dict()
        for _step in config.keys():
            _step_num = int(_step.split("_")[1])
            _dict_steps[_step_num] = _step
        _ord_steps = sorted(list(_dict_steps.keys()))
        for s in _ord_steps:
            _dict_ordered_steps[s] = _dict_steps[s]
        for _step in _dict_ordered_steps.values():
            _new_config[_step] = config[_step]
        return _new_config
    
    @classmethod
    @RunValidator.validate_class_method(check="save_pipeline_step_output")
    def save_pipeline_step_output(
            cls,
            pipeline_name: str, 
            op_name: str,
            save_name: str,
            output: pd.DataFrame | str,
            save_file_path: str | None = None,
    ) -> None:
        _write_class = PipelineSaveStepMappersFactory.get_mapper_classes().get(op_name)
        if save_file_path is None:
            _fp = os.path.join(GenericHelpers.get_base_path(), "src", "artifacts", "pipeline_artifacts", pipeline_name)
        else:
            _fp = save_file_path
        Path(_fp).mkdir(parents=True, exist_ok=True)
        _fp = os.path.join(_fp, save_name)
        _writer = _write_class(file_path = _fp)
        _writer.write_file(output = output)