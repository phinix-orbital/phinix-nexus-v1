from utils.file_loader import FileLoader
from extract.local.read_data import ReadData

class ReadYml(ReadData):
    """
    Read yaml files using abstract read data class.
    """
    def __init__(
            self,
            file_path: str,
    ) -> None:
        super().__init__(file_path=file_path)
    
    def read_file(self):
        return FileLoader.load_yaml_to_dict(file_path=self.file_path)