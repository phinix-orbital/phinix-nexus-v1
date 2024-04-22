import pandas as pd

from pydantic import BaseModel, field_validator, model_validator

from stock.variables import COMPONENT_OPERATIONS

class ValidateRunGeValidation(BaseModel):
    ge_result: dict

    @field_validator("ge_result")
    def validate_success_key(
        cls,
        value: dict,
    ) -> None:
        if "success" not in value.keys():
            raise ValueError("'success' not in passed dictionary keys!")

class ValidateCalculateIndex(BaseModel):
    base: str | int | float
    value: str | int | float
    movement_base: str
    df: pd.DataFrame | None
    new_col_name: str | None

    class Config:
        arbitrary_types_allowed = True

    @field_validator("movement_base")
    def check_movement_base_value(cls, value: str):
        if value.lower() not in ["from", "to"]:
            raise ValueError("movement_base can only be set as 'from' or 'to'!")
    
    @model_validator(mode="after")
    def validate_non_zero_base(
        cls,
        field_values: dict,
    ) -> None:
        df: pd.DataFrame = field_values.get("df")
        _base: bool = field_values.get("base")
        if df is None and _base == 0.:
            raise ZeroDivisionError

class ValidateOrderConfigSteps(BaseModel):
    config: dict

    # @classmethod
    # def check_if_config_item_is_step(cls, config_item: str):
    #     config_item = config_item.lower()
    #     if config_item[0:4]!="step":
    #         raise ValueError("Passed config item is not a step!")
    #     if len(config_item.split("_"))!=2:
    #         raise ValueError("Config step can only be setup in the format 'STEP_N': N (int)!")
    #     _step_number: str = config_item.split("_")[1]
    #     if not _step_number.isdigit():
    #         raise TypeError("Step number has to be type int! 'STEP_N': N (int)")
    
    # @classmethod
    # def check_config_step_numbers(cls, step_numbers: list[int]):
    #     step_numbers = sorted(step_numbers)
    #     if step_numbers[0]!=1:
    #         raise ValueError(f"Config steps have to start from STEP_1. Passed config starts from STEP_{step_numbers[0]}")
    #     _step_diff_list = [t - s for s, t in zip(step_numbers, step_numbers[1:])]
    #     _unique_diff_list = list(set(_step_diff_list))
    #     if len(_unique_diff_list)!=1 or _unique_diff_list[0]!=1:
    #         raise ValueError(f"Steps have to increase by 1 starting from STEP_1! Passed config has step numbers: {', '.join([str(i) for i in step_numbers])}")
    
    # @classmethod
    # def check_step_setup(cls, step_config: dict):
    #     if not isinstance(step_config, dict):
    #         raise ValueError("Each step config must be a dictionary!")

    # @field_validator("config")
    # def validate_config(cls, value: dict):
    #     _step_numbers = []
    #     for k in value.keys():
    #         cls.check_if_config_item_is_step(config_item=k)
    #         _step_numbers.append(int(k.split("_")[1]))
    #     cls.check_config_step_numbers(step_numbers=_step_numbers)
