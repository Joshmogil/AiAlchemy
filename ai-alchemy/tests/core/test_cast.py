import pytest
import ai_alchemy.core.cast as cast
import ai_alchemy.core.ai as ai
from pydantic import BaseModel
import dotenv
import os

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

@pytest.mark.skip(reason="Not implemented")
def test_get_specific_transformation_function(pydantic_model_instance, pydantic_model):
    assert cast._get_specific_transformation_function("hello", str) == cast.str_to_str
    assert cast._get_specific_transformation_function(pydantic_model_instance, str) == cast.pydantic_model_to_str
    assert cast._get_specific_transformation_function(pydantic_model_instance, pydantic_model) == cast.pydantic_model_to_pydantic_model
    assert cast._get_specific_transformation_function("hello", pydantic_model) == cast.str_to_pydantic_model
    try: 
        cast._get_specific_transformation_function(pydantic_model_instance, int)
        assert False
    except ValueError as e:
        assert "Unsupported transformation" in str(e)
        assert True

def test_dict_to_pydantic_model(pydantic_model, openaiwrapper):
    data = {"full_name": "John", "user_age": 25, "height":"5'10", "weight": 150}
    model = cast.dict_to_pydantic_model(data, openaiwrapper,pydantic_model, debug=True)
    assert model.name == "John"
    assert model.age == 25

def test_str_to_pydantic_model(pydantic_model, openaiwrapper):
    data = "John Smith is 25 years old, five foot ten inches tall, and weighs 150 pounds."
    model = cast.str_to_pydantic_model(data, openaiwrapper,pydantic_model, debug=True)
    assert model.name == "John Smith"
    assert model.age == 25

def test_pydantic_model_to_pydantic_model(pydantic_model, openaiwrapper):
    class PydanticModelTest(BaseModel):
        full_name: str
        user_age: int
    data = PydanticModelTest(full_name="John", user_age=25)
    model = cast.pydantic_model_to_pydantic_model(data, openaiwrapper,pydantic_model, debug=True)
    assert model.name == "John"
    assert model.age == 25