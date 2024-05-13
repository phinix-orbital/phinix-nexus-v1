from abc import ABC, abstractmethod

from validators.run_validator import RunValidator

class XmlGenerator(ABC):
    """
    Abstract class to generate XML docs.
    """

    @RunValidator.validate_instance_method(check="generate_xml")
    def __init__(
            self,
            params: dict,
    ) -> None:
        self.params = params
    
    @abstractmethod
    def generate_xml(self) -> None:
        """
        Generate XML using passed params.
        """
        # Abstract method