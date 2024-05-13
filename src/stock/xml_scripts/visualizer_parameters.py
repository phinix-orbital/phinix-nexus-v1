import logging
from xml.etree.ElementTree import Element, SubElement

from stock.xml_scripts.abstract_xml_generator import XmlGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateVisualizerParameters(XmlGenerator):
    """
    Generate Visualizer Parameters XML doc using XML Generator abstract class.
    """

    def __init__(
            self,
            params: dict,
    ) -> None:
        super().__init__(params=params)
    
    def generate_xml(self) -> None:
        pass