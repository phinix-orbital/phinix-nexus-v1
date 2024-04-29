from helpers.orchestrator_helpers import OrchestratorHelpers
from validators.run_validator import RunValidator

class ConfigOrchestrator:
    
    @RunValidator.validate_instance_method(check="config_orchestrator")
    def __init__(
            self,
            config: dict,
            config_type: str
    ) -> None:
        self.config = config
        self.config_type = config_type

    def orchestrate_config(self) -> dict:
        return OrchestratorHelpers.order_config_steps(config=self.config)