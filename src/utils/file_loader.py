import pandas as pd
import logging
import yaml

from validators.run_validator import RunValidator

logger = logging.getLogger(__name__)

class FileLoader:

    @classmethod
    @RunValidator.validate_class_method(check="check_file_path_existence")
    def load_yaml_to_dict(cls, file_path: str) -> dict:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    @classmethod
    @RunValidator.validate_class_method(check="check_file_path_existence")
    def load_df_from_csv(
        cls, 
        file_path: str,
        **kwargs
    ) -> dict:
        return pd.read_csv(file_path, **kwargs)

    @classmethod
    @RunValidator.validate_class_method(check="check_file_path_existence")
    def load_df_from_excel(
        cls, 
        file_path: str,
        **kwargs
    ) -> dict:
        return pd.read_excel(file_path, **kwargs)
