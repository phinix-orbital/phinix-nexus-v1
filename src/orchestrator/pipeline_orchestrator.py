from mappers.pipeline_ops_mappers import PipelineMappersFactory

class PipelineOrchestrator:

    def __init__(
            self,
            config: dict,
    ) -> None:
        self.config = config
    
    def run_pipeline_steps(self):
        _step_outputs = dict()
        for _step, _op_cfg in self.config.items():
            for _op_name, _op_params in _op_cfg.items():
                _op_func = PipelineMappersFactory.get_mapper_classes().get(_op_name)
                for i in ["left_df", "right_df", "list_dfs"]:
                    if i in _op_params.keys():
                        if isinstance(_op_params[i], str) and _op_params[i].lower() in _step_outputs.keys():
                            _op_params[i] = _step_outputs[_op_params[i]]
                        elif isinstance(_op_params[i], list):
                            for s in _op_params[i]:
                                if s.lower() in _step_outputs.keys():
                                    s = _step_outputs[s]
                                else:
                                    raise ValueError(f"Target step {s} in {_step} has not been defined in a previous step!")
                        else:
                            raise ValueError(f"Target step {i} in {_step} has not been defined in a previous step!")
                _op_run = _op_func(**_op_params)
                _step_outputs[_step.lower()] = _op_run
                _result = _op_run
        return _result