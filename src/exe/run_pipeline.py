import logging
import os
import pandas as pd
from pathlib import Path

from helpers.generic_helpers import GenericHelpers
from helpers.orchestrator_helpers import OrchestratorHelpers
from orchestrator.config_orchestrator import ConfigOrchestrator
from orchestrator.pipeline_orchestrator import PipelineOrchestrator
from utils.file_loader import FileLoader
from validators.run_validator import RunValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RunPipeline:

    @classmethod
    @RunValidator.validate_class_method(check="check_file_path_existence")
    def run_pipeline(cls, pipeline_path: str):
        _cfg: dict = FileLoader.read_local_file(file_path = pipeline_path)
        _pipeline_name = Path("pipeline_path").stem
        _cfg_orc = ConfigOrchestrator(config=_cfg, config_type="pipeline").orchestrate_config()
        _pipeline_result: dict =  PipelineOrchestrator(config=_cfg_orc, pipeline_name=_pipeline_name).run_pipeline_steps()
        if isinstance(_pipeline_result.get("output"), pd.DataFrame):
            _file_ext = ".csv"
        elif isinstance(_pipeline_result.get("output"), str):
            _file_ext = ".txt"
        else:
            raise ValueError("Pipeline output must be of type dataframe or str! Other outputs have not yet been implemented.")
        _save_name = f"pipeline_{_pipeline_name}_output_{GenericHelpers.get_time_stamp()}{_file_ext}"
        _save_fp = os.path.join(GenericHelpers.get_base_path(), "src", "outputs")
        _pipeline_result["save_name"] = _save_name
        _pipeline_result["save_file_path"] = _save_fp
        OrchestratorHelpers.save_pipeline_step_output(**_pipeline_result)

if __name__ == "__main__":
    _pipeline_name = input("Please enter pipeline name to run: ")
    logger.info(f"--- Starting run for pipeline {_pipeline_name}... ---")
    _file_ext = os.path.splitext(_pipeline_name)[1]
    _file_ext = _file_ext[1:]
    if len(_file_ext) == 0:
        _pipeline_name += _pipeline_name + ".yml"
    _pipeline_path = os.path.join(GenericHelpers.get_configs_path(), _pipeline_name)    
    RunPipeline.run_pipeline(pipeline_path=_pipeline_path)
    logger.info(f"--- Pipeline run successfully! ---")