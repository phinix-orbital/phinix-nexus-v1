import logging

from mappers.component_ops_mappers import ComponentMappersFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComponentOrchestrator:

    def __init__(
            self,
            config: dict,
    ) -> None:
        self.config = config
    
    def run_component_steps(self):
        _step_outputs = dict()
        for _step, _op_cfg in self.config.items():
            logger.info(f"--- Running component {_step}... ---")
            for _op_name, _op_params in _op_cfg.items():
                _op_func = ComponentMappersFactory.get_mapper_classes().get(_op_name)
                for i in ["calibrate", "schema", "in_feed"]:
                    if i in _op_params.keys():
                        if isinstance(_op_params[i], str) and _op_params[i].lower() in _step_outputs.keys():
                            _op_params[i] = _step_outputs[_op_params[i]]
                            if i == "in_feed":
                                del _op_params["in_feed"]
                        else:
                            raise ValueError(f"Target step {i} in {_step} has not been defined in a previous step!")
            _op_run = _op_func(**_op_params)
            _step_outputs[_step.lower()] = _op_run
            _result = _op_run
        return _result
