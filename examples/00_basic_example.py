import ai_alchemy.core.cast as cast
import ai_alchemy.core.ai as ai
import os
from typing import List
from pydantic import BaseModel
from datetime import datetime

import logging
#logging.basicConfig(level=logging.DEBUG)

openai = ai.OpenAIWrapper(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo")

smart_openai = ai.SmartAiWrapper(ai=openai, max_attempts=2)

class Person(BaseModel):
    full_name: str
    age: int
    spouse: str
    children: List[str]
    pets: List[str]

#Transform unstructured to structured data
string = "Leonard Smith is 31 years old, and lives in New York with his wife Emily, child Richard, and pet cat Benji."
leonard = cast.str_to_pydantic_model(
    input=string,
    ai=smart_openai,
    output=Person
)
print("Result of transforming string to pydantic model\n" + str(leonard))

