LOCAL_FILE_PATH_SUFFFIX_LIST = [
    "yml",
    "yaml",
    "csv",
    "xlsx",
    "txt",
    "j2"
]

CONFIG_TYPES = [
    "component",
    "pipeline",
]

PANDAS_FILTERS = [
    "equals",
    "greater than",
    "less than",
    "string contains",
    "match in list"
]

COMPONENT_OPERATIONS = [
    "input",
    "data_validation",
    "rename_df",
    "fill_na",
    "filter_df",
    "groupby",
    "arithmetic",
    "select_cols",
    "drop_duplicates",
    "drop_records",
    "pivot_cols",
    "reset_index",
]

COMPONENT_OPERATION_INPUT_TYPES = [
    "read_local",
    "basic",
]

PIPELINE_OPERATIONS = [
    "component",
    "dataframes_interaction",
]

DATAFRAMES_INTERACTION_TYPES = [
    "merge",
    "concat",
]

VISUALIZER_PARAMETERS_COLUMNS = [
    "ELEXXXXX_id",	
    "ELEXXXXX_name",	
    "PARXXXXX_id",	
    "PARXXXXX_name",	
    "fields",	
    "REQXXXXX_impacted",	
    "FORXXXXX_used",	
    "status",	
    "fill_color",	
    "line_XXXXX_id",	
    "target_PARXXXXX_id",
]

VISUALIZER_PARAMETER_XML_BLOCK_MXCELL_STYLE = ("swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;"
                                               "horizontal=1;startSize=25;horizontalStack=0;resizeParent=1;resizeParentMax=0;"
                                               "resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;"
                                               "points=[[0.5,0,0,0,0],[0.5,1,0,0,0]];backgroundOutline=0;enumerate=0;comic=0;"
                                               "labelBackgroundColor=none;labelBorderColor=none;textShadow=0;fillStyle=solid;"
                                               "swimlaneFillColor=none;swimlaneLine=1;rounded=1;arcSize=10;portConstraint=none;"
                                               "direction=east;fillColor=#484848;overflow=visible;allowArrows=0;container=1;"
                                               "autosize=0;resizeHeight=1;treeFolding=0;treeMoving=0;strokeColor=default;"
                                               "fontColor=#ffffff;fontSize=14;spacing=0;metaEdit=1;")

VISUALIZER_PARAMETER_XML_PARAMETER_OBJECT_TOOLTIP = ("ID: %%id%%&#xa;Status: %%status%%&#xa;Fields: %%fields%%&#xa;&#xa;"
                                                     "Value (if text): %%value_iftext%%&#xa;"
                                                     "Value (if nominal): %%value_ifnominal%% %%value_units%%&#xa;"
                                                     "Value min (if range): %%value_ifrange_min%% %%value_units%%&#xa;"
                                                     "Value max (if range): %%value_ifrange_max%% %%value_units%%&#xa;"
                                                     "Margin (percentage) : %%value_margin_percentage%% %%&#xa;"
                                                     "Formulas used: %%FORXXXXX_used%%&#xa;&#xa;"
                                                     "Requirements impacted: %%REQXXXXX_impacted%%&#xa;&#xa;"
                                                     "Description: %%description%%")

VISUALIZER_PARAMETER_XML_CONNECTION_MX_CELL_STYLE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
                                                     "html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;"
                                                     "entryDy=0;strokeColor=default;endArrow=block;opacity=50;strokeWidth=2;"
                                                     "startArrow=circle;startFill=1;startSize=1;endFill=1;endSize=4;flowAnimation=1;"
                                                     "flowAnimationDuration=2000;curved=1;")

def get_visualizer_parameter_xml_parameter_mx_cell_style(fill_color:str) -> str:
    if not isinstance(fill_color, str):
        raise ValueError("fill colour must be of type string!")
    return (f"text;strokeColor=default;fillColor={fill_color};align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;"
            "overflow=visible;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;container=0;"
            "fontFamily=Helvetica;fontSize=12;metaEdit=1;backgroundOutline=0;autosize=0;perimeterSpacing=0;rounded=1;glass=0;"
            "shadow=0;imageHeight=24;imageWidth=24;labelPadding=0;expand=1;strokeWidth=1;fontColor=default;fontStyle=0;"
            "fillStyle=solid;gradientColor=none;arcSize=12;")
