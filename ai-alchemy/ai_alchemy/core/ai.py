from abc import ABC, abstractmethod
from openai import OpenAI
from typing import Generator

class AiWrapper(ABC):

    @abstractmethod
    def call(self, input: str, **kwargs) -> Generator[str, None, None]:
        """
        Any implmentation of this method should take an input string and return a string,
        optionally taking keyword arguments that can be used to pass additional information.
        """
        pass


class OpenAIWrapper(AiWrapper):
    # overriding abstract method
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = OpenAI()
        self.client.api_key = api_key
        self.model = "gpt-3.5-turbo"

    def call(self, input:str) -> Generator[str, None, None]: # type: ignore
        client = OpenAI()
        client.api_key = self.api_key
        stream = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": input}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


