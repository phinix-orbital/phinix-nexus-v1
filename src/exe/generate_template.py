from argparse import ArgumentParser, Namespace
from jinja2 import Environment, FileSystemLoader
import os
import logging
from pydantic import ValidationError

from helpers.generic_helpers import GenericHelpers
from validators.extract_validator import ValidateLocalFilePath
from validators.operations_validators import ValidateGenerateTemplate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateTemplate:

    @classmethod
    def parse_args(cls) -> Namespace:
        parser = ArgumentParser(description="Script to generate templates from Jinja files.")
        parser.add_argument("template_name", help="Jinja template name to use for file generation.")
        parser.add_argument("-n", "--number_of_files", type=int, default=1, help="Number of files to generate from the template.")
        parser.add_argument("-e", "--extension", help="File extension of files generated from the template.")
        parser.add_argument("-l", "--list_filenames", nargs="*", help="Optional argument providing list of filenames to use.")
        parser.add_argument("-d", "--directory", default="stock\configs\components", help="Default directory within src to store generated templates.")
        args=parser.parse_args()
        return args
    
    @classmethod
    def main(cls):
        _inputs: Namespace = cls.parse_args()     
        _temp_name = _inputs.template_name
        if _temp_name[-3:]!=".j2":
            _temp_name = os.path.splitext(_temp_name)[0] + ".j2"
        _temp_dir = os.path.join(GenericHelpers.get_base_path(), "src", "stock", "templates")
        try:
            _ = ValidateLocalFilePath(file_path=os.path.join(_temp_dir, _temp_name))
        except ValidationError as e:
            raise e
        logger.info(f"--- Starting file generation using template {_temp_name}... ---")
        if _inputs.number_of_files:
            n_files = _inputs.number_of_files
        else:
            n_files = None
        if _inputs.extension:
            _ext = _inputs.extension
            if _ext[0] == ".":
                _ext = _ext[1:]
        else:
            _ext = None        
        if _inputs.list_filenames:
            _fnames = _inputs.list_filenames
        else:
            _fnames = None
        try:
            _  = ValidateGenerateTemplate(template_name=_temp_name, n_files=n_files, extension=_ext, list_filenames=_fnames)
        except ValidationError as e:
            raise e
        _dir = os.path.join(GenericHelpers.get_base_path(), "src", _inputs.directory)
        if not os.path.exists(_dir):
            raise ValueError(f"{_dir} directory does not exist!")
        if not _fnames:
            _fnames = []
            for i in range(n_files):
                _fnames.append(GenericHelpers.generate_random_name(output_dir=_dir, seed=i))
        if _ext:
            _fnames = [f"{i}.{_ext}" for i in [os.path.splitext(j)[0] for j in _fnames]]
        _template_env = Environment(loader=FileSystemLoader(searchpath=_temp_dir))
        _template = _template_env.get_template(_temp_name)
        logger.info(f"--- Generating templates at dir {_dir}... ---")
        for f in _fnames:
            _file = open(os.path.join(_dir, f), "w")
            _file.write(_template.render())
            _file.close()
        logger.info(f"--- Template generation completed successfully! ---")

if __name__ == "__main__":
    GenerateTemplate.main()
