from mappers.abstract_mappers import AbstractMappersFactory
from operations.pipeline_ops import PipelineOperations

class PipelineMappersFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "component": PipelineOperations.run_component,
            "dataframes_interaction": PipelineOperations.run_dataframes_interaction,
        }
