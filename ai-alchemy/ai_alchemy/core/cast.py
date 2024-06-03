from typing import Any, Callable, Type
from pydantic import BaseModel
from ai_alchemy.core.ai import AiWrapper, SmartAiWrapper, MaxTransformationAttemptsMetError
import logging
from dataclasses import dataclass
from copy import deepcopy

from typing import Protocol, TypeVar

class HasStrMethod(Protocol):
    """
    Protocol class for objects that have a __str__ method.
    """
    def __str__(self) -> str: ...

PydanticModel = TypeVar('PydanticModel', bound=BaseModel)

@dataclass
class TransformationContext:
    """
    Dataclass for storing the context of a transformation.

    Attributes:
    instruction: A string that describes the transformation task.
    output_type: The type of the output.
    output_schema: The schema of the output.
    input_data_type: The type of the input data.
    input_data: The input data.
    additional_context: Additional context for the transformation.
    final_instruction: The final instruction for the transformation.
    """
    instruction: str
    output_type: Type
    output_schema: str
    input_data_type: Type
    input_data: HasStrMethod
    additional_context: str
    final_instruction: str

    def __str__(self):
        """
        Returns a string representation of the TransformationContext.
        """
        base_prompt = [
            self.instruction,
            f"Here is the Output {self.output_type} schema:",
            self.output_schema,
            f"Here is the Input {self.input_data_type}:",
            str(self.input_data),
        ]

        if self.additional_context:
            base_prompt.append(f"Additional Context: {self.additional_context}")

        base_prompt.append(self.final_instruction)

        return "\n".join(base_prompt)
    
def _run_transformation(ai: AiWrapper, context: TransformationContext, validating_marshalling_function: Callable[[str], Any]) -> Any:
    """
    Runs a transformation using an AI model.

    Args:
    ai: The AI model to use for the transformation.
    context: The context of the transformation.
    validating_marshalling_function: A function that validates the output of the transformation.

    Returns:
    The result of the transformation.
    """
    

    prompt = str(context)
    ai_copy=deepcopy(ai)
    if type(ai_copy) == SmartAiWrapper:
        max_attempts = ai_copy.max_attempts
        num_attempts = 0
        while True:
            if num_attempts == max_attempts:
                raise MaxTransformationAttemptsMetError(attempts=num_attempts, max_attempts=max_attempts)
                # TODO This check logic is duplicated here from the smart ai wrapper, this is a better place to put it.
            try:
                import time
                time.sleep(1)

                initial = ai_copy.call(prompt)
                logging.debug(initial)
                if type(initial) == str:
                    r_val = validating_marshalling_function(initial)
                logging.debug(r_val)
                return r_val
            except Exception as e:

                num_attempts += 1
                ai_copy.previous_transformation_error = str(e)
                continue
    else:
        initial = ai_copy.call(prompt)
        logging.debug(initial)
        if type(initial) == str:
            r_val = validating_marshalling_function(initial)
        logging.debug(r_val)
        return r_val

def dict_to_pydantic_model(input: dict, ai: AiWrapper, output: Type[PydanticModel], additional_context:str="", strict: bool = True) -> PydanticModel:
    """
    Transforms a dictionary into a Pydantic model using an AI model.

    Args:
    input: The input dictionary.
    ai: The AI model to use for the transformation.
    output: The type of the Pydantic model to output.
    additional_context: Additional context for the transformation.
    strict: Whether to use strict validation for the Pydantic model.

    Returns:
    The transformed data as an instance of the ouput Pydantic Model.
    """
    context = TransformationContext(
        instruction="Given the following Pydantic schema and input dictionary, your task is to transform the dictionary into a JSON object that matches the Pydantic schema exactly. The transformed JSON object should not include the schema itself.",
        output_type=type(output),
        output_schema=str(output.model_json_schema()),
        input_data=input,
        input_data_type=type(input),
        additional_context=additional_context,
        final_instruction="Please provide the transformed JSON object."
    )

    def pydantic_validation_wrapper(data):
        return output.model_validate_json(json_data=data,strict=strict)
    
    return _run_transformation(ai=ai, context=context,validating_marshalling_function=pydantic_validation_wrapper)

def str_to_pydantic_model(input: str, ai: AiWrapper, output: Type[PydanticModel], additional_context:str="", strict: bool = True) -> PydanticModel:
    """
    Transforms a string into a Pydantic model using an AI model.

    Args:
    input: The input string.
    ai: The AI model to use for the transformation.
    output: The type of the Pydantic model to output.
    additional_context: Additional context for the transformation.
    strict: Whether to use strict validation for the Pydantic model.

    Returns:
    The transformed data as an instance of the ouput Pydantic Model.
    """
    context = TransformationContext(
        instruction="Given the following Pydantic schema and input string, your task is to transform the string into a JSON object that matches the Pydantic schema exactly. The transformed JSON object should not include the schema itself.",
        output_type=type(output),
        output_schema=str(output.model_json_schema()),
        input_data=input,
        input_data_type=type(input),
        additional_context=additional_context,
        final_instruction="Please provide the transformed JSON object."
    )

    def pydantic_validation_wrapper(data):
        return output.model_validate_json(json_data=data,strict=strict)
    
    return _run_transformation(ai=ai, context=context,validating_marshalling_function=pydantic_validation_wrapper)

def pydantic_model_to_pydantic_model(input: BaseModel, ai: AiWrapper, output: Type[PydanticModel], additional_context:str="", strict: bool = True) -> PydanticModel:
    """
    Transforms a Pydantic model into another Pydantic model using an AI model.

    Args:
    input: The input Pydantic model.
    ai: The AI model to use for the transformation.
    output: The type of the Pydantic model to output.
    additional_context: Additional context for the transformation.
    strict: Whether to use strict validation for the Pydantic model.

    Returns:
    The transformed data as an instance of the ouput Pydantic Model.
    """
    context = TransformationContext(
        instruction="Given the following Input data and Output Pydantic schema, your task is to transform the Input data into a JSON object that matches the Pydantic schema exactly. The transformed JSON object should not include the schema itself.",
        output_type=type(output),
        output_schema=str(output.model_json_schema()),
        input_data=input.model_dump_json(),
        input_data_type=type(input),
        additional_context=additional_context,
        final_instruction="Please provide the transformed JSON object."
    )
    def pydantic_validation_wrapper(data):
        return output.model_validate_json(json_data=data,strict=strict)
    
    return _run_transformation(ai=ai, context=context,validating_marshalling_function=pydantic_validation_wrapper)