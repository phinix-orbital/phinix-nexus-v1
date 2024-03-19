import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class ReadData(ABC):
    """
    Abstract class for local data reads.
    """

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