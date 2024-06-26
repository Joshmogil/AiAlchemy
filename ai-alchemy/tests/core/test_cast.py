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
    return TestModel


@pytest.fixture
def openaiwrapper():
    openai = ai.OpenAIWrapper(api_key=os.environ["OPENAI_API_KEY"])
    return openai


def test_dict_to_pydantic_model(pydantic_model, openaiwrapper):
    data = {"full_name": "John", "user_age": 25, "height":"5'10", "weight": 150}
    model = cast.dict_to_pydantic_model(data, openaiwrapper,pydantic_model)

def test_str_to_pydantic_model(pydantic_model, openaiwrapper):
    data = "John Smith is 25 years old, five foot ten inches tall, and weighs 150 pounds."
    model = cast.str_to_pydantic_model(data, openaiwrapper,pydantic_model)

def test_pydantic_model_to_pydantic_model(pydantic_model, openaiwrapper):
    class PydanticModelTest(BaseModel):
        full_name: str
        user_age: int
    data = PydanticModelTest(full_name="John", user_age=25)
    model = cast.pydantic_model_to_pydantic_model(data, openaiwrapper,pydantic_model)
