from abc import ABC 
from abc import abstractmethod
from openai import OpenAI
from typing import Any
import logging

class AiWrapper(ABC):
    """
    Abstract base class for AI wrappers.
    """

    @abstractmethod
    def call(self, input: str, **kwargs) -> str:
        """
        Abstract method to be implemented by subclasses. 

        Args:
            input (str): The input string.
            **kwargs: Optional keyword arguments.

        Returns:
            str: The output string.
        """
        raise NotImplementedError


class OpenAIWrapper(AiWrapper):
    """
    Wrapper for the OpenAI API.
    """

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo") -> None:
        """
        Initialize the OpenAIWrapper with the given API key and model.

        Args:
            api_key (str): The API key for OpenAI.
            model (str, optional): The model to use. Defaults to "gpt-3.5-turbo".
        """
        self.api_key = api_key
        self.model = model

    def call(self, input:str) -> str: # type: ignore
        """
        Call the OpenAI API with the given input and return the response.

        Args:
            input (str): The input string.

        Returns:
            str: The output string.
        """
        client = OpenAI(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": input}],
            stream=False
        )
        response = resp.choices[0].message.content
        return str(response)

class SmartAiWrapper(AiWrapper):
    """
    Wrapper for complex AI operations.
    """

    def __init__(self, ai: AiWrapper, max_attempts: int = 3) -> None:
        """
        Initialize the ComplexAiWrapper with the given AI and maximum number of attempts.

        Args:
            ai (AiWrapper): The AI wrapper to use.
            max_attempts (int, optional): The maximum number of attempts. Defaults to 3.
        """
        self.ai = ai
        self.original_input: str = ""
        self._current_transformation_instructions: str = "1. Sort the data\n2. Perform the final transformation\n3. Return the data\n"
        self._previous_transformation_result: str = "No response"
        self.previous_transformation_error: str = "No Error"
        self.attempts: int = 0
        self.max_attempts: int = max_attempts
    
    def _come_up_with_transformation(self):
        """
        Come up with a new transformation based on the previous result.
        """
        prompt=(f"You are an AI who creates data transformation instructions for another AI based on the following DATA TRANSFORMATION REQUEST: {self.original_input}\n"
            f"You previously came up with these instructions:\n"
            f"{self._current_transformation_instructions}\n"
            f"The previous transformation result was:\n"
            f"{self._previous_transformation_result}\n"
            f"The previous transformation failed with the error:\n"
            f"{self.previous_transformation_error}\n"
            f"Please come up with new transformation instructions based on the previous result and error."
            )
        result = self.ai.call(prompt)
        logging.debug(result)
        
        self._current_transformation_instructions = self.ai.call(prompt)
    

    def _perform_current_transformation(self) -> Any:
        """
        Perform the current transformation and store the result.

        Returns:
            Any: The result of the transformation.
        """
        prompt = (
            f"You are an AI who performs data transformations based on the following instructions\n"
            f"{self._current_transformation_instructions}\n"
            f"Here is the input data:\n"
            f"{self.original_input}"
            )
        self.previous_transformation_result = str(self.ai.call(prompt))
    

    def call(self, input: str) -> str: # type: ignore
        """
        Perform a transformation on the input and return the result.

        Args:
            input (str): The input string.

        Returns:
            str: The output string.

        Raises:
            MaxTransformationAttemptsExceededError: If the maximum number of transformation attempts is exceeded.
        """
        self.original_input = input
        
        if self.attempts == self.max_attempts:
            raise MaxTransformationAttemptsMetError(attempts=self.attempts, max_attempts=self.max_attempts)
        else:
            self._come_up_with_transformation()
            self._perform_current_transformation()
            self.attempts += 1
            return self.previous_transformation_result
        
        
class MaxTransformationAttemptsMetError(Exception):
    """
    Exception raised when the maximum number of transformation attempts is exceeded.
    Attributes:
        attempts -- number of attempts made
        max_attempts -- maximum number of attempts allowed
    """
    def __init__(self, attempts: int, max_attempts: int):
        """
        Initialize the exception with the number of attempts made and the maximum number of attempts allowed.

        Args:
            attempts (int): The number of attempts made.
            max_attempts (int): The maximum number of attempts allowed.
        """
        self.message = f"Max transformation attempts of {max_attempts} exceeded. {attempts} attempts made."
        super().__init__(self.message)