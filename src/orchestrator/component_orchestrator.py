import pandas as pd

from mappers.component_ops_mappers import ComponentMappersFactory

class ComponentOrchestrator:

    def __init__(
            self,
            config: dict,
    ) -> None:
        self.config = config
    
    def run_component_steps(self):
        for _step, _op_cfg in self.config.items():
            for _op_name, _op_params in _op_cfg.items():
                _op_func = ComponentMappersFactory.get_mapper_classes().get(_op_name)
                _op_run = _op_func(**_op_params)
                if _op_run is not None:
                    _step = _op_run # will be saved for future ops
