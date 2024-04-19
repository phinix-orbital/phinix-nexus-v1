import os
import pandas as pd
import logging
import yaml

from validators.run_validator import RunValidator

logger = logging.getLogger(__name__)

class FileLoader:

    @classmethod
    @RunValidator.validate_class_method(check="load_yaml_to_dict")
    def load_yaml_to_dict(cls, file_path: str) -> dict:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    @classmethod
    @RunValidator.validate_class_method(check="load_df_from_csv")
    def load_df_from_csv(
        cls, 
        file_path: str,
        **kwargs
    ) -> pd.DataFrame:
        return pd.read_csv(file_path, **kwargs)

    @classmethod
    @RunValidator.validate_class_method(check="load_df_from_excel")
    def load_df_from_excel(
        cls, 
        file_path: str,
        **kwargs
    ) -> pd.DataFrame:
        return pd.read_excel(file_path, **kwargs)
    
    @classmethod
    @RunValidator.validate_class_method(check="check_file_path_existence")
    def read_local_file(
        cls, 
        file_path: str,
        **kwargs
    ) -> dict | pd.DataFrame:
        _file_ext = os.path.splitext(file_path)[1]
        _file_ext = _file_ext[1:]
        if _file_ext in ["yml", "yaml"]:
            return cls.load_yaml_to_dict(file_path=file_path)
        elif _file_ext == "csv":
            return cls.load_df_from_csv(file_path=file_path, **kwargs)
        elif _file_ext == "xlsx":
            return cls.load_df_from_excel(file_path=file_path, **kwargs)
