from mappers.abstract_mappers import AbstractMappersFactory
from validators import extract_validator, pipeline_validator

class ValidatorsMapperFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "check_file_path_existence": extract_validator.ValidateLocalFilePath,
            "convert_key_to_pandas_filter": pipeline_validator.ValidateConvertKeyToPandasFilter,
        }