import os
import logging
from pydantic import BaseModel, field_validator
from stock.variables import LOCAL_FILE_PATH_SUFFFIX_LIST

logger = logging.getLogger(__name__)

class ValidateLocalFilePath(BaseModel):
    file_path: str

    @field_validator("file_path")
    def validate_extension(
        cls,
        value: str,
    ) -> None:
        _file_ext = os.path.splitext(value)[1]
        _file_ext = _file_ext[1:]
        if len(_file_ext) == 0:
            raise ValueError(f"File path passed does not have an extension!")
        else:
            if _file_ext not in LOCAL_FILE_PATH_SUFFFIX_LIST:
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

class ValidateLoadYamlToDict(BaseModel):
    file_path: str

    @field_validator("file_path")
    def validate_extension(
        cls,
        value: str,
    ) -> None:
        _file_ext = os.path.splitext(value)[1]
        _file_ext = _file_ext[1:]
        if _file_ext not in ["yml", "yaml"]:
            raise ValueError(f"Local file to be read must have extension .yml or .yaml!")

class ValidateLoadDfFromCsv(BaseModel):
    file_path: str

    @field_validator("file_path")
    def validate_extension(
        cls,
        value: str,
    ) -> None:
        _file_ext = os.path.splitext(value)[1]
        _file_ext = _file_ext[1:]
        if _file_ext != "csv":
            raise ValueError(f"Local file to be read must have extension .yml or .yaml!")

class ValidateLoadDfFromExcel(BaseModel):
    file_path: str

    @field_validator("file_path")
    def validate_extension(
        cls,
        value: str,
    ) -> None:
        _file_ext = os.path.splitext(value)[1]
        _file_ext = _file_ext[1:]
        if _file_ext != "xlsx":
            raise ValueError(f"Local file to be read must have extension .yml or .yaml!")
