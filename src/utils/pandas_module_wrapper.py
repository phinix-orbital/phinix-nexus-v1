import re
from mappers.pandas_filter_mappers import PandasFiltersMapperFactory
from validators.run_validator import RunValidator

class PandasModuleWrapper:

    @RunValidator.validate_class_method(check="convert_key_to_pandas_filter")
    @classmethod
    def convert_key_to_pandas_filter(
        cls,
        filter_name: str,
        include: bool = True,
    ) -> str:
        filter_name = filter_name.lower()
        _dict_mappers = PandasFiltersMapperFactory.get_mapper_classes()
        _filter = _dict_mappers.get(filter_name)
        if include:
            _filter += "="
        return _filter