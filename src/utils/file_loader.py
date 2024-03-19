import pandas as pd
import logging
import yaml

logger = logging.getLogger(__name__)

class FileLoader:

    @classmethod
    def load_yaml_to_dict(cls, file_path: str) -> dict:
        if file_path[-3:]!="yml" or file_path[-4:]!="yaml":
            file_path += "yml"
        try:
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error("Error reading file!")
            raise e

    @classmethod
    def load_df_from_csv(
        cls, 
        file_path: str,
        **kwargs
    ) -> dict:
        if file_path[-3:]!="csv":
            file_path += ".csv"
        try:
            return pd.read_csv(file_path, **kwargs)
        except FileNotFoundError as e:
            logger.error("Error reading file!")
            raise e