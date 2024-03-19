import logging
from pydantic import BaseModel, field_validator
from stock.variables import LOCAL_FILE_PATH_SUFFFIX_LIST

logger = logging.getLogger(__name__)

class ValidateLocalFilePath(BaseModel):
    file_path: str

    @field_validator("file_path")
    def validate_path_existence(
        cls,
        value: str,
    ) -> None:
        if value.split(".")[1] not in LOCAL_FILE_PATH_SUFFFIX_LIST:
            raise ValueError(f"Local file to be read must end with one of {', '.join(LOCAL_FILE_PATH_SUFFFIX_LIST)}!")
        _file_read_indicator = False
        try:
            f = open(value, "rb")
            _file_read_indicator = True
        except FileNotFoundError as e:
            logger.error(f"File not found at path {value}")
            raise e
        else:
            if _file_read_indicator:
                f.close()
