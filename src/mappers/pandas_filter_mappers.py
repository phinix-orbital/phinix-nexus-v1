from mappers.abstract_mappers import AbstractMappersFactory


class PandasFiltersMapperFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "equals": "==",
            "greater than": ">",
            "less than": "<",
            "string contains": ".str.contains",
            "match in list": ".isin",
        }