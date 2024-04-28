from mappers.abstract_mappers import AbstractMappersFactory
from operations.pipeline_ops import PipelineOperations
from load.write_csv import WriteCsv

class PipelineMappersFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "component": PipelineOperations.run_component,
            "dataframes_interaction": PipelineOperations.run_dataframes_interaction,
        }

class PipelineSaveStepMappersFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "component": WriteCsv,
            "dataframes_interaction": WriteCsv,
        }