from mappers.abstract_mappers import AbstractMappersFactory
from validators import (
    extract_validator, 
    helpers_validator, 
    utils_validator, 
    operations_validators, 
    misc_validator, 
    load_validator,
)

class ValidatorsMapperFactory(AbstractMappersFactory):
    @classmethod
    def get_mapper_classes(cls) -> dict:
        return {
            "check_file_path_existence": extract_validator.ValidateLocalFilePath,
            "load_yaml_to_dict": extract_validator.ValidateLoadYamlToDict,
            "load_df_from_csv": extract_validator.ValidateLoadDfFromCsv,
            "load_df_from_excel": extract_validator.ValidateLoadDfFromExcel,
            "write_dataframe": load_validator.ValidateWriteDataframe,
            "write_string": load_validator.ValidateWriteString,
            "write_xml": load_validator.ValidateWriteXml,
            "save_pipeline_step_output": load_validator.ValidateSavePipelineStepOutput,
            "visualizer_parameters": load_validator.ValidateVisualizerParameters,
            "run_ge_validation": helpers_validator.ValidateRunGeValidation,
            "calculate_index": helpers_validator.ValidateCalculateIndex,
            "order_config_steps": helpers_validator.ValidateOrderConfigSteps,
            "convert_key_to_pandas_filter": utils_validator.ValidateConvertKeyToPandasFilter,
            "create_filter_condition": utils_validator.ValidateCreateFilterCondition,
            "rename_columns": utils_validator.ValidateRenameColumns,
            "groupby_and_agg": utils_validator.ValidateGroupbyAndAgg,
            "run_input": operations_validators.ValidateRunInput,
            "run_data_validation": operations_validators.ValidateRunDataValidation,
            "run_component": operations_validators.ValidateRunComponent,
            "run_dataframes_interaction": operations_validators.ValidateRunDataframesInteraction,
            "input_data_validator": misc_validator.ValidateInputDataValidator,
            "config_orchestrator": misc_validator.ValidateConfigOrchestrator,
        }