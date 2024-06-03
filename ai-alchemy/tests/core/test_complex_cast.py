import pytest
import ai_alchemy.core.cast as cast
import ai_alchemy.core.ai as ai
from pydantic import BaseModel
import dotenv
import os
import logging

logging.basicConfig(level=logging.DEBUG)

dotenv.load_dotenv()

@pytest.fixture
def pydantic_model_instance():
    class TestModel(BaseModel):
        name: str
        age: int
    return TestModel(name="John", age=25)

@pytest.fixture
def pydantic_model():

    class TestModel(BaseModel):
        name: str
        age: int
        friends: list[str]
        enemies: list[str]
        favorite_color: int
    return TestModel


@pytest.fixture
def complexopenaiwrapper():
    openai = ai.OpenAIWrapper(api_key=os.environ["OPENAI_API_KEY"])
    complex_ai = ai.SmartAiWrapper(ai=openai, max_attempts=2)
    return complex_ai


def test_complex_str_to_pydantic_model(pydantic_model, complexopenaiwrapper):
    data = "John was born in 1998 to Lauren and Michael Smith, his best friends are Lauren, Lisa, and Michael. He can often be seen around town in an orange tshirt. He often has run-ins with the police, specifically one named brad."    
    model = cast.str_to_pydantic_model(input=data,ai= complexopenaiwrapper, output =pydantic_model)

    #rely on error from pydantic
