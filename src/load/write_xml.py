import logging
from xml.etree.ElementTree import ElementTree, tostring

from load.write_data import WriteData
from validators.run_validator import RunValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WriteXml(WriteData):
    """
    Write XML class using abstract write data class.
    """

    def __init__(
            self,
            file_path: str,
    ) -> None:
        super().__init__(file_path=file_path)
    
    @RunValidator.validate_instance_method(check="write_xml")
    def write_file(
            self,
            output: ElementTree,
    ) -> None:
        output.write(self.file_path)
        logger.info(f"File saved successfully at path: {self.file_path}")