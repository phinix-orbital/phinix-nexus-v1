from validators.run_validator import RunValidator

class OrchestratorHelpers:
    
    @classmethod
    @RunValidator.validate_class_method(check="order_config_steps")
    def order_config_steps(cls, config: dict):
        _steps = sorted(list(config.keys()))
        _new_config = dict()
        for _step in _steps:
            _new_config[_step] = config[_step]
        return _new_config