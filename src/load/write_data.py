from abc import ABC, abstractmethod
from validators.run_validator import RunValidator

class WriteData(ABC):
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
    def write_file(self, **kwargs):
        """
        Write file from passed file path. File path must point to a file, not a directory.
        """
        # Abstract method