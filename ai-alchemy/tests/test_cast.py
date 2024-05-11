import pytest
import ai_alchemy.cast as cast
from pydantic import BaseModel
import inspect


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
