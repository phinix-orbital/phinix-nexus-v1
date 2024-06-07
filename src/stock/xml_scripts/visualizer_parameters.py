import logging
import pandas as pd
from typing import Tuple
from xml.etree.ElementTree import Element, SubElement, ElementTree

from stock.variables import (
    VISUALIZER_PARAMETER_XML_BLOCK_MXCELL_STYLE,
    VISUALIZER_PARAMETER_XML_CONNECTION_MX_CELL_STYLE,
    VISUALIZER_PARAMETER_XML_PARAMETER_OBJECT_TOOLTIP,
    get_visualizer_parameter_xml_parameter_mx_cell_style,
)
from stock.xml_scripts.abstract_xml_generator import XmlGenerator
from validators.run_validator import RunValidator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenerateVisualizerParameters(XmlGenerator):
    """
    Generate Visualizer Parameters XML doc using XML Generator abstract class.
    """

    @RunValidator.validate_instance_method(check="visualizer_parameters")
    def __init__(
            self,
            params: pd.DataFrame,
    ) -> None:
        super().__init__(params=params)
    
    def _get_setup(self) -> Element:
        return Element("mxGraphModel", dx="919", dy="1583", grid="1", gridSize="10", guides="1", tooltips="1",
                        connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="850",
                        pageHeight="1100", math="0", shadow="0")
    
    def _get_root_elements(self, setup: Element) -> Tuple[Element, Element, Element]:
        _root = SubElement(setup, "root")
        _mx_cell_0 = SubElement(_root, "mxCell", id="0")
        _mx_cell_1 = SubElement(_root, "mxCell", id="1", parent="0")
        return _root, _mx_cell_0, _mx_cell_1
    
    def _get_block_elements(
            self,
            root: Element,
            attr: dict,
    ) -> Tuple[Element, Element, Element]:
        _object = SubElement(root, "object", label="%%ELEXXXXX_name%%", ELEXXXXX_name=attr.get("element_name"),
                             placeholders="1", tooltip="", id=attr.get("element_id"))
        _mx_cell = SubElement(_object, "mxCell", style=VISUALIZER_PARAMETER_XML_BLOCK_MXCELL_STYLE, 
                              vertex="1", parent="1")
        _mx_geo = SubElement(_mx_cell, "mxGeometry", {"as":"geometry"}, x=attr.get("x"), y="0", 
                             width="150", height="172")
        return _object, _mx_cell, _mx_geo
    
    def _get_parameter_elements(
            self,
            root: Element,
            attr: dict,
    ) -> Tuple[Element, Element, Element]:
        _object = SubElement(root, "object", label="%%parameter_name%%", placeholders="1",
                             tooltip=VISUALIZER_PARAMETER_XML_PARAMETER_OBJECT_TOOLTIP, 
                             FORXXXXX_used=attr.get("formula_used"), REQXXXXX_impacted=attr.get("requirements"), 
                             parameter_name=attr.get("parameter_name"), fields=attr.get("fields"), 
                             status=attr.get("status"), id = attr.get("parameter_id"))
        _mx_cell = SubElement(_object, "mxCell", style=get_visualizer_parameter_xml_parameter_mx_cell_style(attr.get("fill_colour")), 
                              vertex="1", parent=attr.get("element_id"))
        _mx_geo = SubElement(_mx_cell, "mxGeometry", {"as":"geometry"}, y=attr.get("y"), 
                             width="150", height="25")
        return _object, _mx_cell, _mx_geo
    
    def _get_connection_elements(
            self,
            root: Element,
            attr: dict,
    ) -> Tuple[Element, Element]:
        _mx_cell = SubElement(root, "mxCell", id=attr.get("line_id"), style=VISUALIZER_PARAMETER_XML_CONNECTION_MX_CELL_STYLE, 
                              edge="1", parent="1", source=attr.get("start_parameter"), target=attr.get("target_parameter"))
        _mx_geo = SubElement(_mx_cell, "mxGeometry", {"as":"geometry"}, relative="1")
        return _mx_cell, _mx_geo

    def generate_xml(self) -> None:
        df = self.params
        _mx_graph_model = self._get_setup()
        _root, _root_cell_0, _root_cell_1 = self._get_root_elements(setup=_mx_graph_model)
        _elements: list = df["ELEXXXXX_id"].unique().tolist()
        for _elem in _elements:
            _block_attr = {
                "element_id": _elem,
                "element_name": df[df["ELEXXXXX_id"] == _elem]["ELEXXXXX_name"].unique().tolist()[0],
                "x": df[df["ELEXXXXX_id"] == _elem]["x"].unique().tolist()[0],
            }
            _block_object, _block_cell, _block_geo = self._get_block_elements(root=_root, attr=_block_attr)
            _parameter_ids: list = df[df["ELEXXXXX_id"] == _elem]["PARXXXXX_id"].tolist()
            _parameter_names: list = df[df["ELEXXXXX_id"] == _elem]["PARXXXXX_name"].tolist()
            _formulas_used: list = df[df["ELEXXXXX_id"] == _elem]["FORXXXXX_used"].tolist()
            _requirements: list = df[df["ELEXXXXX_id"] == _elem]["REQXXXXX_impacted"].tolist()
            _fields: list = df[df["ELEXXXXX_id"] == _elem]["fields"].tolist()
            _statuses: list = df[df["ELEXXXXX_id"] == _elem]["fields"].tolist()
            _fcolours: list = df[df["ELEXXXXX_id"] == _elem]["fill_color"].tolist()
            _ycoords: list = df[df["ELEXXXXX_id"] == _elem]["y"].tolist()
            for _pid, _pname, _form, _req, _fld, _st, _fcolour, _y in zip(_parameter_ids, _parameter_names, 
                                                            _formulas_used, _requirements, 
                                                            _fields, _statuses, _fcolours,
                                                            _ycoords):
                _parameter_attributes = {
                    "parameter_id": _pid,
                    "parameter_name": _pname,
                    "formula_used": _form,
                    "requirements": _req,
                    "fields": _fld,
                    "status": _st,
                    "fill_colour": _fcolour,
                    "element_id": _elem,
                    "y": _y,
                }
                _param_object, _param_cell, _param_geo = self._get_parameter_elements(root=_block_object, 
                                                                attr=_parameter_attributes)
        _lines: list = df[~df["line_XXXXX_id"].isna()].unique().tolist()
        for _lid in _lines:
            _line_attr = {
                "line_id": _lid,
                "start_parameter": df[df["line_XXXXX_id"] == _lid]["PARXXXXX_id"].tolist()[0],
                "target_parameter": df[df["line_XXXXX_id"] == _lid]["target_PARXXXXX_id"].tolist()[0],
            }
            _line_cell, _line_geo = self._get_connection_elements(root=_root, attr=_line_attr)
        tree = ElementTree(_mx_graph_model)
        return tree