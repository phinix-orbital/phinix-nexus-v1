import great_expectations as ge
import pandas as pd

from helpers.generic_helpers import GenericHelpers
from validators.run_validator import RunValidator

class ValidateInputData:

    @RunValidator.validate_instance_method(check="input_data_validator")
    def __init__(
            self,
            calibrate: pd.DataFrame,
            schema: pd.DataFrame | dict,
    ) -> None:
        self.df_calibrate = calibrate
        self.schema = schema
    
    def _get_schema_dict(self):
        if isinstance(self.schema, dict):
            return self.schema
        else:
            _schema_dict = dict(list(zip(self.schema["column_name"].tolist(), self.schema["column_type"].tolist())))
            return _schema_dict
    
    def validate_data(self):
        data = ge.from_pandas(self.df_calibrate)
        _schema = self._get_schema_dict()
        for _col in _schema.keys():
            GenericHelpers.run_ge_validation(dict(**data.expect_column_to_exist(_col)))
        for _col, _col_type in _schema.items():
            GenericHelpers.run_ge_validation(dict(**data.expect_column_values_to_be_of_type(_col, _col_type)))