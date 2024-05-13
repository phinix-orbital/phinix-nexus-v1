from abc import ABC, abstractmethod

class WriteData(ABC):
    """
    Abstract class for local data reads.
    """

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