import pytest
import ai_alchemy.core as core


def test_register_transformation_functions()
    core._register_transformation_functions(core._transform_str_to_str)
    core._register_transformation_functions(core._transform_str_to_pydantic_model)
    core._register_transformation_functions(core._transform_pydantic_model_to_str)
    core._register_transformation_functions(core._transform_pydantic_model_to_pydantic_model)