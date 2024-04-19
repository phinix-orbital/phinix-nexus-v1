from mappers.abstract_mappers import AbstractMappersFactory
from operations.component_ops import ComponentOperations

class ComponentMappersFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "input": ComponentOperations.run_input,
            "data_validation": ComponentOperations.run_data_validation,
        }