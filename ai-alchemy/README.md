# AI Alchemy

AI Alchemy is a Python library that provides a convenient way to interact with AI models, such as OpenAI's GPT-3.5 Turbo, and perform transformations on data.

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
# Import necessary libraries
import os
import ai_alchemy
from ai_alchemy.ai import OpenAIWrapper
from pydantic import BaseModel

# Instantiate a wrapper for an AI model
openai = OpenAIWrapper(api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo")

# Define a Pydantic model
class User(BaseModel):
    name: str
    age: int

# Input data
data = "John Smith is 25 years old, five foot ten inches tall, and weighs 150 pounds."

# Use AI Alchemy to transform the data into a Pydantic model
model = ai_alchemy.cast.str_to_pydantic_model(data, openai, User)

# Now `model` is a `User` instance with `name` and `age` populated from `data`
```