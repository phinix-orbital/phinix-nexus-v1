from mappers.abstract_mappers import AbstractMappersFactory
from load.write_csv import WriteCsv

class PipelineSaveStepMappersFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "component": WriteCsv,
            "dataframes_interaction": WriteCsv,
        }