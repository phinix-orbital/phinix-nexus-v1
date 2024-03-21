from pydantic import BaseModel, field_validator, model_validator
from stock.variables import PANDAS_FILTERS

class ValidateConvertKeyToPandasFilter(BaseModel):
    filter_name: str
    include: bool

    @field_validator("filter_name")
    def validate_filter_key_existence(
        cls,
        value: str,
    ) -> None:
        if value.lower() not in [i.lower() for i in PANDAS_FILTERS]:
            raise ValueError(f"{value} not in implemented list of pandas filters!")
    
    @model_validator(mode="after")
    def validate_fields_combination(
        cls,
        field_values: dict,
    ) -> None:
        _fname: str = field_values.get("filter_name")
        _inc = field_values.get("include")
        if _inc and _fname.lower() not in ["greater than", "less than"]:
            raise ValueError(f"{_fname} is not valid for include = True!")