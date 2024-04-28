import os
import pandas as pd
from pathlib import Path

from helpers.generic_helpers import GenericHelpers
from mappers.pipeline_ops_mappers import PipelineMappersFactory, PipelineSaveStepMappersFactory
from validators.run_validator import RunValidator

class PipelineOrchestrator:

    def __init__(
            self,
            config: dict,
            pipeline_name: str,
    ) -> None:
        self.config = config
        self.pipeline_name = pipeline_name
    
    @RunValidator.validate_instance_method(check="save_pipeline_step_output")
    def _save_pipeline_step_output(
            self, 
            op_name: str,
            save_name: str,
            output: pd.DataFrame | str,
    ):
        _write_class = PipelineSaveStepMappersFactory.get_mapper_classes().get(op_name)
        _fp = os.path.join(GenericHelpers.get_base_path(), "src", "artifacts", "pipeline_artifacts", self.pipeline_name)
        Path(_fp).mkdir(parents=True, exist_ok=True)
        _fp = os.path.join(_fp, save_name)
        _writer = _write_class(file_path = _fp)
        _writer.write_file(output = output)
    
    def run_pipeline_steps(self):
        _step_outputs = dict()
        for _step, _op_cfg in self.config.items():
            for _op_name, _op_params in _op_cfg.items():
                _op_func = PipelineMappersFactory.get_mapper_classes().get(_op_name)
                if _op_name not in ["dataframes_interaction"]:
                    continue
                _params: dict = _op_params.get("parameters")
                for i in ["left_df", "right_df", "list_dfs"]:
                    if i in _params.keys():
                        if isinstance(_params[i], str) and _params[i].lower() in _step_outputs.keys():
                            _params[i] = _step_outputs[_params[i]]
                        elif isinstance(_params[i], list):
                            for s in _params[i]:
                                if s.lower() in _step_outputs.keys():
                                    s = _step_outputs[s]
                                else:
                                    raise ValueError(f"Target step {s} in {_step} has not been defined in a previous step!")
                        else:
                            raise ValueError(f"Target step {i} in {_step} has not been defined in a previous step!")
            _op_run = _op_func(**_op_params)
            _step_outputs[_step.lower()] = _op_run
            _result = _op_run
            if "save_step" in _op_params.keys():
                if "save_name" not in _op_params.get("save_step"):
                    raise ValueError("'save_step' must contain 'save_name' as the key!")
                if not isinstance(_op_params["save_step"]["save_name"], str):
                    raise ValueError("'save_name' must be of type str!")
                self._save_pipeline_step_output(op_name=_op_name, save_name=_op_params["save_step"]["save_name"], output=_result)
        return _result