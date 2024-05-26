from typing import Type, Any
from pandas import DataFrame
from pydantic import BaseModel
from ai_alchemy.core.ai import AiWrapper

def dict_to_pydantic_model(input: dict, ai: AiWrapper, output: BaseModel, additional_context:str="", debug: bool = False, strict: bool = True):
    base_prompt = [
        "Given the following Pydantic schema and input dictionary, transform the dictionary into a JSON object. The JSON object should match the Pydantic schema exactly, and should not include the schema itself.",
        "Pydantic schema:",
        f"{output.model_json_schema()}",
        f"Possibly some Additional Context: <{additional_context}>",
        "Input dictionary:",
        f"{input}",
        "Please provide only the transformed JSON object."
    ]
        
    joined_prompt="\n".join(base_prompt)
    final=""
    for out in ai.call("\n".join(joined_prompt)):
        final = final + out
    if debug:
        print(final)
    r_val = output.model_validate_json(json_data=final, strict=strict)
    return r_val

def str_to_pydantic_model(input: str, ai: AiWrapper, output: BaseModel, additional_context:str="", debug: bool =False, strict: bool = True):
    base_prompt = [
        "Given the following Pydantic schema and input string, transform the string into a JSON object. The JSON object must match the Pydantic schema exactly, and should not include the schema itself.",
        "Pydantic schema:",
        f"{output.model_json_schema()}",
        f"Possibly some Additional Context: <{additional_context}>",
        "Input string:",
        f"{input}",
        "Please provide the only transformed JSON object."
    ]
        
    joined_prompt="\n".join(base_prompt)
    final=""
    for out in ai.call("\n".join(joined_prompt)):
        final = final + out
    if debug:
        print(final)
    r_val = output.model_validate_json(json_data=final, strict=strict)
    return r_val

def pydantic_model_to_pydantic_model(input: BaseModel, ai: AiWrapper, output: BaseModel,  additional_context:str="", debug: bool =False, strict: bool = True):
    base_prompt = [
        "Given the following Input data and Output Pydantic schema, transform the Input data a into a JSON object that matches the Pydantic schema exactly, and should not include the schema itself.",
        "Pydantic schema:",
        f"{output.model_json_schema()}",
        f"Possibly some Additional Context: <{additional_context}>",
        "Input data:",
        f"{input.model_dump_json()}",
        "Please provide only the transformed JSON object."
    ]
        
    joined_prompt="\n".join(base_prompt)
    final=""
    for out in ai.call("\n".join(joined_prompt)):
        final = final + out
    if debug:
        print(final)
    r_val = output.model_validate_json(json_data=final, strict=strict)
    return r_val

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
