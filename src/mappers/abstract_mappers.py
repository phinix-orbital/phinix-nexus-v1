from abc import ABC, abstractmethod

class AbstractMappersFactory(ABC):
    """
    Abstract class for mappers.
    """
    @abstractmethod
    def get_mapper_classes(cls):
        """
        Return mappers dictionary.
        """
        # Abstract method