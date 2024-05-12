import os
from datetime import datetime, UTC
import random
import string

from pydantic import ValidationError

from validators.helpers_validator import (
    ValidateRunGeValidation, 
    ValidateCheckIfAllListElementsSame,
    ValidateGenerateRandomString,
    ValidateGenerateRandomNumber,
    ValidateGenerateRandomName,
)

class GenericHelpers:

    @classmethod
    def get_base_path(cls) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    @classmethod
    def get_configs_path(cls) -> str:
        return os.path.join(cls.get_base_path(), 'src', 'stock', 'configs')
    
    @classmethod
    def get_time_stamp(cls) -> str:
        _ts = datetime.now(UTC)
        return f"{_ts.date()}_{int(_ts.timestamp())}"
    
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
    
    @classmethod
    def generate_random_string(
        cls, 
        size:int = 5, 
        seed:int | None = None
    ) -> str:
        try:
            _ = ValidateGenerateRandomString(size=size, seed=seed)
        except ValidationError as e:
            raise e
        if seed:
            random.seed(seed)
        return ("".join(random.choice(string.ascii_lowercase) for i in range(size)))
    
    @classmethod
    def generate_random_number(
        cls, 
        lower_bound: int = 0, 
        upper_bound: int = 99999,
        seed:int | None = None
    ) -> int:
        try:
            _ = ValidateGenerateRandomNumber(lower_bound=lower_bound, upper_bound=upper_bound, seed=seed)
        except ValidationError as e:
            raise e
        if seed:
            random.seed(seed)
        return random.randint(lower_bound, upper_bound)
    
    @classmethod
    def generate_random_name(
        cls, 
        output_dir: str, 
        str_length: int | None = 5, 
        int_length: int | None = 5,
        seed:int | None = None
    ) -> str:
        try:
            _ = ValidateGenerateRandomName(output_dir=output_dir, str_length=str_length, int_length=int_length, seed=seed)
        except ValidationError as e:
            raise e
        _files = [i.split(".")[0] for i in os.listdir(output_dir)]
        if len(_files) == 0:
            _files = ["dEcLaN_RiCe_41_BS7_MO8"]
            _f = "dEcLaN_RiCe_41_BS7_MO8"
        else:
            _f = _files[0]        
        while _f in _files:
            if not seed:
                seed = 41
            if str_length:
                _name_part_1 = f"{cls.generate_random_string(size=str_length, seed=seed)}_"
            else: 
                _name_part_1 = ""
            if int_length:
                _name_part_2 = f"{cls.generate_random_number(lower_bound=10**int_length, upper_bound=10**(int_length+1)-1, seed=seed)}"
            else: 
                _name_part_2 = ""
            seed += 1
            _f = _name_part_1 + _name_part_2
        return _f
