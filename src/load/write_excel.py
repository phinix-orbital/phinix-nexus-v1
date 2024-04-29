import logging
import pandas as pd

from load.write_data import WriteData
from validators.run_validator import RunValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WriteExcel(WriteData):
    """
    Write Excel class using abstract write data class.
    """

    def __init__(
            self,
            file_path: str,
    ) -> None:
        super().__init__(file_path=file_path)
    
    @RunValidator.validate_instance_method(check="write_dataframe")
    def write_file(
            self,
            output: pd.DataFrame,
            **kwargs
    ) -> None:
        output.to_excel(self.file_path, index=False, **kwargs)
        logger.info(f"File saved successfully at path: {self.file_path}")