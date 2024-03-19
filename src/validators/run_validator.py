import logging
from functools import wraps
from typing import Callable

from mappers.validator_mappers import ValidatorsMapperFactory

class RunValidator:
    @staticmethod
    def validate_instance_method(check: str):
        def validate_decorator(func: Callable):
            wraps(func)

            def wrapper(self, *args, **kwargs):
                logging.basicConfig(level=logging.INFO)
                log = logging.getLogger(__name__)
                log.info(f"--- Running Validator for {check}... ---")
                _validator = ValidatorsMapperFactory.get_mapper_classes().get(check)
                _validator(*args, **kwargs)
                return func(self, *args, **kwargs)
            
            return wrapper
        
        return validate_decorator
    
    @staticmethod
    def validate_class_method(check: str):
        def validate_decorator(func: Callable):
            wraps(func)

            def wrapper(cls, *args, **kwargs):
                logging.basicConfig(level=logging.INFO)
                log = logging.getLogger(__name__)
                log.info(f"--- Running Validator for {check}... ---")
                _validator = ValidatorsMapperFactory.get_mapper_classes().get(check)
                _validator(*args, **kwargs)
                return func(cls, *args, **kwargs)
            
            return wrapper
        
        return validate_decorator
    
    @staticmethod
    def validate_method(check: str):
        def validate_decorator(func: Callable):
            wraps(func)

            def wrapper(*args, **kwargs):
                logging.basicConfig(level=logging.INFO)
                log = logging.getLogger(__name__)
                log.info(f"--- Running Validator for {check}... ---")
                _validator = ValidatorsMapperFactory.get_mapper_classes().get(check)
                _validator(*args, **kwargs)
                return func(*args, **kwargs)
            
            return wrapper
        
        return validate_decorator