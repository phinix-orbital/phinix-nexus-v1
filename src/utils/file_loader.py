import pandas as pd
import logging
import yaml

logger = logging.getLogger(__name__)

class FileLoader:

    @classmethod
    def load_yaml_to_dict(cls, file_path: str) -> dict:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

    @classmethod
    def load_df_from_csv(
        cls, 
        file_path: str,
        **kwargs
    ) -> dict:
        return pd.read_csv(file_path, **kwargs)
