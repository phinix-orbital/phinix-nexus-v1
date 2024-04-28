import os

from pydantic import ValidationError

from validators.helpers_validator import ValidateRunGeValidation, ValidateCheckIfAllListElementsSame

class GenericHelpers:

    @classmethod
    def get_base_path(cls) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    @classmethod
    def get_configs_path(cls) -> str:
        return os.path.join(cls.get_base_path(), 'src', 'stock', 'configs')
    
    @classmethod
    def run_ge_validation(cls, ge_result: dict) -> None:
        try:
            _ = ValidateRunGeValidation(ge_result=ge_result)
        except ValidationError as e:
            raise e
        if not ge_result.get("success"):
            raise ValueError(f"Data expectation check failed! Check result: {ge_result.get('result')}")
    
    @classmethod
    def check_if_all_list_elements_same(cls, check_list: list) -> bool:
        try:
            _ = ValidateCheckIfAllListElementsSame(check_list=check_list)
        except ValidationError as e:
            raise e
        if len(list(set(check_list))) == 1:
            return True
        else:
            return False      
