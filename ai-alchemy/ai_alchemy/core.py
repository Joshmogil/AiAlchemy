from typing import Type, Callable
from pandas import DataFrame
from pydantic import BaseModel
import inspect

def cast(input: Type, output: Type):
    pass

def _register_transformation_functions():
    """
    Registers the transformation functions that are available in the core module.
    Creates a global variable called TRANSFORMATION_FUNCTIONS that is a dictionary.
    """
    global TRANSFORMATION_FUNCTIONS
    functions = [
        _transform_str_to_str,
        _transform_str_to_pydantic_model,
        _transform_pydantic_model_to_str,
        _transform_pydantic_model_to_pydantic_model,
    ]
    for function in functions:
        input_type, output_type = _validate_signature_and_return_input_output_types(function)
        TRANSFORMATION_FUNCTIONS[(input_type, output_type)] = function


def _validate_signature_and_return_input_output_types(function: Callable):
    params = inspect.signature(function).parameters
    if params.keys() != {"input", "output"}:
        raise ValueError("The function should have exactly two parameters: input and output")
    return params["input"].annotation, params["output"].annotation
    


TRANSFORMATION_FUNCTIONS: dict[str, Callable] = {}


def _get_specific_tranformation_function(input:Type, output:Type):
    input_type=type(input)
    output_type=type(output)

def _transform_str_to_str(input: str, output: str):
    pass

def _transform_str_to_pydantic_model(input: str, output: BaseModel):
    pass

def _transform_pydantic_model_to_str(input: BaseModel, output: str):
    pass

def _transform_pydantic_model_to_pydantic_model(input: str, output: BaseModel):
    pass

if __name__ == "__main__":
    _register_transformation_functions()
    print(TRANSFORMATION_FUNCTIONS)
