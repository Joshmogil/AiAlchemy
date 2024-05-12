# Python program showing
# abstract base class work
from abc import ABC, abstractmethod


class AiWrapper(ABC):

    @abstractmethod
    def call(self, input: str, **kwargs) -> str:
        """
        Any implmentation of this method should take an input string and return a string,
        optionally taking keyword arguments that can be used to pass additional information.
        """
        pass


class OpenAI(AiWrapper):
    # overriding abstract method
    def noofsides(self):
        print("I have 3 sides")


class Anthropic(AiWrapper):
    # overriding abstract method
    def noofsides(self):
        print("I have 5 sides")

class Ollama(AiWrapper):
    # overriding abstract method
    def noofsides(self):
        print("I have 5 sides")