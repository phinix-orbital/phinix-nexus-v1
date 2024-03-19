from validators import extract_validator

class ValidatorsMapperFactory:
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "check_file_path_existence": extract_validator.ValidateLocalFilePath,
        }