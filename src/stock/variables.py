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
    "concat"
]
