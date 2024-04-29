import logging

from helpers.orchestrator_helpers import OrchestratorHelpers
from mappers.pipeline_ops_mappers import PipelineMappersFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:

    def __init__(
            self,
            config: dict,
            pipeline_name: str,
    ) -> None:
        self.config = config
        self.pipeline_name = pipeline_name
    
    def run_pipeline_steps(self):
        _step_outputs = dict()
        for _step, _op_cfg in self.config.items():
            logger.info(f"--- Running pipeline {_step}... ---")
            for _op_name, _op_params in _op_cfg.items():
                logger.info(f"--- Running pipeline operation {_op_name}... ---")
                _op_func = PipelineMappersFactory.get_mapper_classes().get(_op_name)
                if _op_name not in ["dataframes_interaction"]:
                    _params = _op_params
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
                _op_params["parameters"] = _params
                _params = {"interaction_config": _op_params}
            _op_run = _op_func(**_params)
            _step_outputs[_step.lower()] = _op_run
            if "save_step" in _op_params.keys():
                if "save_name" not in _op_params.get("save_step"):
                    raise ValueError("'save_step' must contain 'save_name' as the key!")
                if not isinstance(_op_params["save_step"]["save_name"], str):
                    raise ValueError("'save_name' must be of type str!")
                OrchestratorHelpers.save_pipeline_step_output(pipeline_name=self.pipeline_name, op_name=_op_name, 
                                                              save_name=_op_params["save_step"]["save_name"], output=_op_run)       
        return {
            "pipeline_name" : self.pipeline_name,
            "op_name" : _op_name,
            "output" : _op_run
        }