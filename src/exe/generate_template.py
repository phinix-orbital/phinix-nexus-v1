from argparse import ArgumentParser, Namespace
from jinja2 import Environment, FileSystemLoader
import logging

from helpers.generic_helpers import GenericHelpers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateTemplate:

    @classmethod
    def parse_args(cls) -> Namespace:
        parser = ArgumentParser(description="Script to generate templates from Jinja files.")
        parser.add_argument("template_name", help="Jinja template name to use for file generation.")
        parser.add_argument("-n", "--number_of_files", type=int, help="Number of files to generate from the template.")
        parser.add_argument("-e", "--extension", default=".yml", help="File extension of files generated from the template.")
        parser.add_argument("-l", "--list_filenames", type=list, help="Optional argument providing list of filenames to use.")
        args=parser.parse_args()
        return args
    
    @classmethod
    def main(cls):
        _inputs: Namespace = cls.parse_args()
        logger.info(f"--- Starting file generation using template {_inputs.template_name}... ---")
        _ext = _inputs.extension
        if _inputs.list_filenames:
            _fnames = _inputs.list_filenames
        else:
            _fnames = []
            for i in range(_inputs.number_of_files):
                _fnames.append(GenericHelpers.generate_random_name(...))
