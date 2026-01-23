# Lesson 8: Structured Output

## Theory

### Why Structured Output?

LLMs generate unstructured text by default. For applications, we often need:
- **Consistent format**: Same structure every time
- **Type safety**: Validated data types
- **Easy parsing**: Direct conversion to objects
- **Error handling**: Catch invalid outputs

**Unstructured**: "The user is John, age 30, from NYC"  
**Structured**: `{"name": "John", "age": 30, "city": "NYC"}`

### Pydantic Models

Pydantic provides data validation using Python type hints:

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Age in years", ge=0, le=150)
    city: str = Field(description="City of residence")

# Usage
person = Person(name="John", age=30, city="NYC")
print(person.model_dump())  # {"name": "John", "age": 30, "city": "NYC"}
```

### Structured Output Methods

**1. JSON Mode**
```python
llm = ChatOllama(model="llama3.2", format="json")
```

**2. Output Parsers**
```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(pydantic_object=Person)
chain = prompt | llm | parser
```

**3. Function Calling** (for supported models)
```python
llm_with_structure = llm.with_structured_output(Person)
result = llm_with_structure.invoke("Tell me about John, 30, from NYC")
```

### Pydantic Field Types

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str = Field(description="Task title")
    description: Optional[str] = Field(default=None, description="Detailed description")
    priority: Priority = Field(description="Task priority level")
    tags: List[str] = Field(default_factory=list, description="Task tags")
    completed: bool = Field(default=False, description="Completion status")
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # Nested model
```

### Validation

Pydantic automatically validates:
- Type correctness
- Required fields
- Value constraints (min, max, regex)
- Custom validators

```python
from pydantic import BaseModel, Field, validator

class Email(BaseModel):
    address: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    
    @validator('address')
    def validate_email(cls, v):
        if not '@' in v:
            raise ValueError('Invalid email')
        return v.lower()
```

### Error Handling

```python
from pydantic import ValidationError

try:
    person = Person(name="John", age="invalid", city="NYC")
except ValidationError as e:
    print(e.json())
```

### Prompting for Structure

Clear instructions help LLMs generate valid JSON:

```python
prompt = ChatPromptTemplate.from_template("""
Extract information from the text and return as JSON.

Required format:
{{
    "name": "string",
    "age": "integer",
    "city": "string"
}}

Text: {text}

JSON:""")
```

## Demo

See `demo.py` for examples:
1. Basic Pydantic models
2. JSON output parsing
3. Nested models
4. Enums and lists
5. Validation and error handling
6. Structured output with LLMs
7. Batch processing

### Quick Example

```python
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")

llm = ChatOllama(model="llama3.2", format="json")
parser = JsonOutputParser(pydantic_object=Person)

prompt = ChatPromptTemplate.from_template("""
Extract person info as JSON: {text}

{format_instructions}
""")

chain = prompt | llm | parser
result = chain.invoke({
    "text": "John is 30 years old",
    "format_instructions": parser.get_format_instructions()
})
# {"name": "John", "age": 30}
```

## Challenge

Build an **Email Parser** that extracts structured data from email text:

**Extract:**
1. Sender name and email
2. Recipients (list)
3. Subject
4. Sentiment (positive/neutral/negative)
5. Action items (list)
6. Priority (low/medium/high)
7. Category (work/personal/spam)

**Requirements:**
- Use Pydantic models with proper validation
- Handle missing fields gracefully
- Support nested structures (sender/recipient objects)
- Use enums for sentiment, priority, category
- Validate email addresses with regex
- Process multiple emails in batch
- Export results to JSON file

**Example Input:**
```
From: alice@company.com
To: bob@company.com, charlie@company.com
Subject: Q4 Planning Meeting

Hi team,

We need to schedule our Q4 planning meeting. Please:
1. Review the attached budget
2. Prepare your department goals
3. Submit availability by Friday

This is urgent!

Best,
Alice
```

**Expected Output:**
```json
{
  "sender": {"name": "Alice", "email": "alice@company.com"},
  "recipients": [
    {"name": "Bob", "email": "bob@company.com"},
    {"name": "Charlie", "email": "charlie@company.com"}
  ],
  "subject": "Q4 Planning Meeting",
  "sentiment": "neutral",
  "action_items": [
    "Review the attached budget",
    "Prepare your department goals",
    "Submit availability by Friday"
  ],
  "priority": "high",
  "category": "work"
}
```

**Bonus:**
- Add date/time extraction
- Detect meeting requests
- Extract attachments mentioned
- Calculate urgency score

**Starter code in `challenge.py`**

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Output Parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/)
- [Structured Output Guide](https://python.langchain.com/docs/modules/model_io/chat/structured_output/)
- [JSON Mode](https://python.langchain.com/docs/integrations/chat/ollama/)
