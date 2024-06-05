from abc import ABC, abstractmethod
import pandas as pd

class XmlGenerator(ABC):
    """
    Abstract class to generate XML docs.
    """

    def __init__(
            self,
            params: pd.DataFrame,
    ) -> None:
        self.params = params
    
    @abstractmethod
    def generate_xml(self) -> None:
        """
        Generate XML using passed params.
        """
        # Abstract method