import pandas as pd

from validators.run_validator import RunValidator

class CalculationHelpers:

    @classmethod
    @RunValidator.validate_class_method(check="calculate_index")
    def calculate_index(
        base: str | int | float,
        value: str | int | float,
        df: pd.DataFrame | None = None,
        new_col_name: str | None = None,
    ) -> pd.DataFrame | float:
        if df is not None:
            df[new_col_name] = (df[value] - df[base])/df[base]
            return df
        else:
            return (value - base)/base