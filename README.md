# AIAlchemy

AIAlchemy is a Python library that provides a convenient way to interact with AI models to perform data transformations and validation using the standard library and gold star libraries like Pydantic and Pandas.

It is initially focused on 3 key transformations:
- String to Pydantic Model
- Dict to Pydantic Model
- Pydantic to Pydantic Model

This allows stepwise transformations that can be lego'd together with validation every step of the way, as well as easy integration into existing programs with a learn as you go approach to prompting.



More features comming soon, see the [roadmap](roadmap.md)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download Python [here](https://www.python.org/downloads/).

### Installation

You can install AI Alchemy via pip:

```bash
pip install ai_alchemy
```

### Usage
Here's a basic example of how to use AI Alchemy:

```python
import ai_alchemy.core.ai as ai
import ai_alchemy.core.cast as cast
from pydantic import BaseModel
import os

openai = ai.OpenAIWrapper(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo")

# Define a Pydantic model
class User(BaseModel):
    name: str
    age: int

# Input data
data = "John Smith is 25 years old, five foot ten inches tall, and weighs 150 pounds."

# Use AI Alchemy to transform the data into a Pydantic model
model = cast.str_to_pydantic_model(data, openai, User)

# Use AI Alchemy to transform the data into a Pydantic model
model = ai_alchemy.cast.str_to_pydantic_model(data, openai, User)

# Now `model` is a `User` instance with `name` and `age` populated from `data`
```

For more inspiration see [examples](https://github.com/Joshmogil/AiAlchemy/tree/main/examples)
