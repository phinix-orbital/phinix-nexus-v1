from mappers.abstract_mappers import AbstractMappersFactory
from validators import extract_validator, utils_validator

class ValidatorsMapperFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "check_file_path_existence": extract_validator.ValidateLocalFilePath,
            "convert_key_to_pandas_filter": utils_validator.ValidateConvertKeyToPandasFilter,
            "create_filter_condition": utils_validator.ValidateCreateFilterCondition,
            "rename_columns": utils_validator.ValidateRenameColumns,
            "groupby_and_agg": utils_validator.ValidateGroupbyAndAgg,
        }