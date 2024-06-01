from abc import ABC 
from abc import abstractmethod
from openai import OpenAI
from typing import Any

from dataclasses import dataclass

@dataclass
class TransformationRequest:
    """
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
    """
    top_instruction: str
    output_schema_type: str
    output_schema: str
    input_data_type: str
    input: str
    additional_context: str
    bottom_instruction: str

    def __str__(self):
        base_prompt = [
            self.top_instruction,
            f"Here is the Output {self.output_schema_type} schema:",
            self.output_schema,
            f"Here is the Input {self.input_data_type}:",
            self.input,
        ]

        if self.additional_context:
            base_prompt.append(f"Additional Context: {self.additional_context}")

        base_prompt.append(self.bottom_instruction)

        return "\n".join(base_prompt)


class AiWrapper(ABC):
    
    @abstractmethod
    def call(self, input: str, **kwargs) -> str | None:
        """
        Any implmentation of this method should take an input string and return a string,
        optionally taking keyword arguments that can be used to pass additional information.
        """
        pass


class OpenAIWrapper(AiWrapper):
    # overriding abstract method
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = api_key
        self.model = model

    def call(self, input:str) -> str | None: # type: ignore
        client = OpenAI(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": input}],
            stream=False
        )
        response = resp.choices[0].message.content
        return response
        #for chunk in stream:
        #    if chunk.choices[0].delta.content is not None:
        #        yield chunk.choices[0].delta.content


class ComplexAiWrapper(AiWrapper):


    def __init__(self, ai: AiWrapper, max_attempts: int = 3) -> None:
        self.ai = ai
        self.original_input: str = ""
        self.current_transformation_instructions: str = "1. Sort the data\n2. Perform the final transformation\n3. Return the data\n"
        self.previous_transformation_result: str = "No response "
        self.attempts: int = 0
        self.max_attempts: int = max_attempts
    
    def _come_up_with_transformation(self):

        
        prompt=(f"You are an AI who creates data transformation instructions for another AI based on the following DATA TRANSFORMATION REQUEST: {self.original_input}\n"
            f"You previously came up with these instructions:\n"
            f"{self.current_transformation_instructions}\n"
            f"The previous transformation result was:\n"
            f"{self.previous_transformation_result}\n"
            f"Please come up with new transformation instructions based on the previous result."
            )
        result = self.ai.call(prompt)
        print("Should be something")
        print(result)
        self.current_transformation_instructions = self.ai.call(prompt)
    

    def _perform_current_transformation(self) -> Any:
        prompt = (
            f"You are an AI who performs data transformations based on the following instructions"
            f"{self.current_transformation_instructions}\n"
            f"Here is the input data:\n"
            f"{self.original_input}"
            )
        self.previous_transformation_result = str(self.ai.call(prompt))
    

    def call(self, input: str) -> str | None: # type: ignore
        self.original_input = input
        self.attempts += 1
        if self.attempts > self.max_attempts:
            raise MaxTransformationAttemptsExceededError(attempts=self.attempts, max_attempts=self.max_attempts)
        else:
            self._come_up_with_transformation()
            self._perform_current_transformation()
            return self.previous_transformation_result
        
class MaxTransformationAttemptsExceededError(Exception):
    """Exception raised when the maximum number of transformation attempts is exceeded.
    Attributes:
        attempts -- number of attempts made
        max_attempts -- maximum number of attempts allowed
    """
    def __init__(self, attempts: int, max_attempts: int):
        self.message = f"Max transformation attempts of {max_attempts} exceeded. {attempts} attempts made."
        super().__init__(self.message)



if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv()
    ai = OpenAIWrapper(api_key=os.environ["OPENAI_API_KEY"])
    ag = ComplexAiWrapper(ai=ai)

    

