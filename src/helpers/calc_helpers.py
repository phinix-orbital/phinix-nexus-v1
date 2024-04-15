import logging
import pandas as pd

logger = logging.getLogger(__name__)

class CalculationHelpers:

    @classmethod
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
            if base == 0.:
                logger.error("Cannot divide by 0!")
                raise ZeroDivisionError
            if movement_base == "to":
                return (value - base)/base
            else:
                return (base - value)/base