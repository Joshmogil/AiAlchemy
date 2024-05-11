from typing import Type, Callable, Any
from pandas import DataFrame
from pydantic import BaseModel
import inspect


def magic(input_data: Any, output_type: Type) -> Any:
    transformation_function = _get_specific_transformation_function(input_data, output_type)


    pass


def _get_specific_transformation_function(input:Type, output:Type):

    if isinstance(input, str) and output == str:
        return str_to_str
    elif isinstance(input, str) and issubclass(output, BaseModel):
        return str_to_pydantic_model
    elif isinstance(input, BaseModel) and output == str:
        return pydantic_model_to_str
    elif isinstance(input, BaseModel) and issubclass(output, BaseModel):
        return pydantic_model_to_pydantic_model
    elif isinstance(input, DataFrame) and type(output) == DataFrame:
        return dataframe_to_dataframe
    elif isinstance(input, DataFrame) and issubclass(output, BaseModel):
        return dataframe_to_pydantic_model
    elif isinstance(input, BaseModel) and type(output) == DataFrame:
        return pydantic_model_to_dataframe

    else:
        raise ValueError(f"Unsupported transformation {type(input)} -> {type(output)}")

def str_to_str(input: str, output: str):
    pass

def str_to_pydantic_model(input: str, output: BaseModel):
    pass

def pydantic_model_to_str(input: BaseModel, output: str):
    pass

def pydantic_model_to_pydantic_model(input: BaseModel, output: BaseModel):
    pass

def dataframe_to_dataframe(input: DataFrame, output: DataFrame):
    pass

def dataframe_to_pydantic_model(input: DataFrame, output: BaseModel):
    pass

def pydantic_model_to_dataframe(input: BaseModel, output: DataFrame):
    pass

#if __name__ == "__main__":
#    _register_transformation_functions()
#    print(TRANSFORMATION_FUNCTIONS)
