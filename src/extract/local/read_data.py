import logging
from abc import ABC, abstractmethod
from validators.run_validator import RunValidator

logger = logging.getLogger(__name__)

class ReadData(ABC):
    """
    Abstract class for local data reads.
    """

    @RunValidator.validate_instance_method(check="check_file_path_existence")
    def __init__(
            self,
            file_path: str,
    ) -> None:
        self.file_path = file_path
    
    @abstractmethod
    def read_file(self, **kwargs):
        """
        Read input file from passed file path. File path must point to a file, not a directory.
        """
        # Abstract method