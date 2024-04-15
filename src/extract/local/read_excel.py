from utils.file_loader import FileLoader
from extract.local.read_data import ReadData

class ReadExcel(ReadData):
    """
    Read Excel class using abstract read data class.
    """

    def __init__(
            self,
            file_path: str,
    ) -> None:
        super().__init__(file_path=file_path)
    
    def read_file(self, **kwargs):
        return FileLoader.load_df_from_excel(file_path=self.file_path, **kwargs)