import pandas as pd
import yaml

class FileLoader:
    
    @classmethod
    def load_yaml_to_dict(cls, file_path: str) -> dict:
        if file_path[-3:]!="yml":
            file_path += "yml"
        with open(file_path, "r") as f:
            return yaml.safe_load(f)