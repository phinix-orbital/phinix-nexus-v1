import great_expectations as ge
import pandas as pd
from typing import Self

from pydantic import BaseModel, field_validator, model_validator

from helpers.generic_helpers import GenericHelpers
from stock.variables import CONFIG_TYPES, COMPONENT_OPERATIONS, PIPELINE_OPERATIONS

class ValidateConfigOrchestrator(BaseModel):
    config: dict
    config_type: str
    
    def check_if_config_item_is_step(self, config_item: str):
        config_item = config_item.lower()
        if config_item[0:4]!="step":
            raise ValueError("Passed config item is not a step!")
        if len(config_item.split("_"))!=2:
            raise ValueError("Config step can only be setup in the format 'STEP_N': N (int)!")
        _step_number: str = config_item.split("_")[1]
        if not _step_number.isdigit():
            raise TypeError("Step number has to be type int! 'STEP_N': N (int)")

    def check_config_step_numbers(self, step_numbers: list[int]):
        step_numbers = sorted(step_numbers)
        if step_numbers[0]!=1:
            raise ValueError(f"Config steps have to start from STEP_1. Passed config starts from STEP_{step_numbers[0]}")
        _step_diff_list = [t - s for s, t in zip(step_numbers, step_numbers[1:])]
        _unique_diff_list = list(set(_step_diff_list))
        if len(_unique_diff_list)!=1 or _unique_diff_list[0]!=1:
            raise ValueError(f"Steps have to increase by 1 starting from STEP_1! Passed config has step numbers: {', '.join([str(i) for i in step_numbers])}")

    def check_step_setup(self, step_config: dict):
        if not isinstance(step_config, dict):
            raise ValueError("Each step config must be a dictionary!")
        for k, v in step_config.items():
            if self.config_type == "component":
                if k.lower() not in COMPONENT_OPERATIONS:
                    raise ValueError(f"Component operation {k} not in registered list! Accepted operations are: {', '.join(COMPONENT_OPERATIONS)}")
                if not isinstance(v, dict):
                    raise ValueError("Component operation must be defined as a dict!")
            elif self.config_type == "pipeline":
                if k.lower() not in PIPELINE_OPERATIONS:
                    raise ValueError(f"Pipeline operation {k} not in registered list! Accepted operations are: {', '.join(PIPELINE_OPERATIONS)}")
                if not isinstance(v, dict):
                    raise ValueError("Pipeline operation must be defined as a dict!")
 
    @model_validator(mode="after")
    def validate_config(self) -> Self:
        _cfg: dict = self.config
        _cfg_type: str = self.config_type
        if _cfg_type not in CONFIG_TYPES:
            raise ValueError(f"config_type has to be one of {', '.join(CONFIG_TYPES)}")
        _step_numbers = []
        for k in _cfg.keys():
            self.check_if_config_item_is_step(config_item=k)
            _step_numbers.append(int(k.split("_")[1]))
        self.check_config_step_numbers(step_numbers=_step_numbers)
        for _step_cfg in _cfg.values():
            self.check_step_setup(step_config=_step_cfg)
        return self

class ValidateComponentOrchestrator(BaseModel):
    config: dict

class ValidatePipelineOrchestrator(BaseModel):
    config: dict
    pipeline_name: str