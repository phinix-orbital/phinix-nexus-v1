import pandas as pd

from validators.run_validator import RunValidator

class CalculationHelpers:

    @classmethod
    @RunValidator.validate_class_method(check="calculate_index")
    def calculate_index(
        base: str | int | float,
        value: str | int | float,
        movement_base: str = "to",
        df: pd.DataFrame | None = None,
        new_col_name: str | None = None,
    ) -> pd.DataFrame | float:
        if df is not None:
            if movement_base == "to":
                df[new_col_name] = (df[value] - df[base])/df[base]
            else:
                df[new_col_name] = (df[base] - df[value])/df[base]
            return df
        else:
            if movement_base == "to":
                return (value - base)/base
            else:
                return (base - value)/base