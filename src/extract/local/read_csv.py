from utils.file_loader import FileLoader
from extract.local.read_data import ReadData

class ReadCsv(ReadData):
    """
    Read CSV class using abstract read data class.
    """

    def __init__(
            self,
            file_path: str,
    ) -> None:
        super().__init__(file_path)
    
    def read_file(self, **kwargs):
        return FileLoader.load_df_from_csv(self.file_path, **kwargs)