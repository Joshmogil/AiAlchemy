from typing import Any, Callable, Type
from pandas import DataFrame
from pydantic import BaseModel
from ai_alchemy.core.ai import AiWrapper, MaxTransformationAttemptsExceededError

def dict_to_pydantic_model(input: dict, ai: AiWrapper, output: BaseModel, additional_context:str="", debug: bool = False, strict: bool = True):
    base_prompt = [
        "Given the following Pydantic schema and input dictionary, your task is to transform the dictionary into a JSON object that matches the Pydantic schema exactly. The transformed JSON object should not include the schema itself.",
        "Here is the Pydantic schema:",
        f"{output.model_json_schema()}",
        "Here is the Input dictionary:",
        f"{input}",
    ]
    
    if additional_context:
        base_prompt.append(f"Additional Context: {additional_context}")
    
    base_prompt.append("Please provide the transformed JSON object.")
    
    joined_prompt = "\n".join(base_prompt)
    
    final = ai.call(joined_prompt)
    if debug:
        print(final)
    r_val = output.model_validate_json(json_data=final, strict=strict)
    return r_val

def str_to_pydantic_model(input: str, ai: AiWrapper, output: BaseModel, additional_context:str="", debug: bool =False, strict: bool = True):
    base_prompt = [
        "Given the following Pydantic schema and input string, your task is to transform the string into a JSON object that matches the Pydantic schema exactly. The transformed JSON object should not include the schema itself.",
        "Here is the Pydantic schema:",
        f"{output.model_json_schema()}",
        "Here is the Input string:",
        f"{input}",
    ]
    
    if additional_context:
        base_prompt.append(f"Additional Context: {additional_context}")
    
    base_prompt.append("Please provide the transformed JSON object.")
    
    joined_prompt = "\n".join(base_prompt)
    
    while True:
        try:
            final = ai.call(joined_prompt)
            if debug:
                print(final)
            if type(final) == str:
                r_val = output.model_validate_json(json_data=final, strict=strict)
            return r_val
        except MaxTransformationAttemptsExceededError:
            raise
        except:
            continue

def pydantic_model_to_pydantic_model(input: BaseModel, ai: AiWrapper, output: BaseModel, additional_context:str="", debug: bool =False, strict: bool = True):
    base_prompt = [
        "Given the following Input data and Output Pydantic schema, your task is to transform the Input data into a JSON object that matches the Pydantic schema exactly. The transformed JSON object should not include the schema itself.",
        "Here is the Pydantic schema:",
        f"{output.model_json_schema()}",
        "Here is the Input data:",
        f"{input.model_dump_json()}",
    ]
    
    if additional_context:
        base_prompt.append(f"Additional Context: {additional_context}")
    
    base_prompt.append("Please provide the transformed JSON object.")
    
    joined_prompt = "\n".join(base_prompt)
    
    final = ai.call(joined_prompt)
    if debug:
        print(final)
    r_val = output.model_validate_json(json_data=final, strict=strict)
    return r_val

def _run_transformation(ai: AiWrapper, marshalling_function: Callable[[str], Any]) -> Any:
    
    
    pass

def _pydantic_model_to_dataframe(input: BaseModel, ai: AiWrapper, output: DataFrame):
    pass



def _magic(input_data: Any, output_type: Type) -> Any:
    transformation_function = _get_specific_transformation_function(input_data, output_type)


    pass


def _get_specific_transformation_function(input:Type, output:Type):
    pass

    #if isinstance(input, str) and output == str:
    #    return str_to_str
    #elif isinstance(input, str) and issubclass(output, BaseModel):
    #    return str_to_pydantic_model
    #elif isinstance(input, BaseModel) and output == str:
    #    return pydantic_model_to_str
    #elif isinstance(input, BaseModel) and issubclass(output, BaseModel):
    #    return pydantic_model_to_pydantic_model
    #elif isinstance(input, DataFrame) and type(output) == DataFrame:
    #    return dataframe_to_dataframe
    #elif isinstance(input, DataFrame) and issubclass(output, BaseModel):
    #    return dataframe_to_pydantic_model
    #elif isinstance(input, BaseModel) and type(output) == DataFrame:
    #    return pydantic_model_to_dataframe
    #else:
    #    raise ValueError(f"Unsupported transformation {type(input)} -> {type(output)}")



#def str_to_str(input: str, output: str):
#    pass

#def str_to_pydantic_model(input: str, output: BaseModel):
#    pass

#def pydantic_model_to_str(input: BaseModel, output: str):
#    pass



#def dataframe_to_dataframe(input: DataFrame, output: DataFrame):
#    pass

#def dataframe_to_pydantic_model(input: DataFrame, output: BaseModel):
#    pass



#if __name__ == "__main__":
#    _register_transformation_functions()
#    print(TRANSFORMATION_FUNCTIONS)
