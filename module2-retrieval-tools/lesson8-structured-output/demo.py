"""
Lesson 8 Demo: Structured Output with Pydantic
"""

from pydantic import BaseModel, Field, validator, ValidationError
from typing import List, Optional
from enum import Enum
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate


# Basic Pydantic model
class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Age in years", ge=0, le=150)
    email: str = Field(description="Email address")


# Enum example
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Complex nested model
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str


class Employee(BaseModel):
    name: str
    employee_id: int
    department: str
    address: Address
    skills: List[str] = Field(default_factory=list)
    priority: Priority = Priority.MEDIUM


def basic_pydantic_demo():
    """Basic Pydantic usage"""
    print("=== Basic Pydantic Models ===\n")
    
    # Valid person
    person = Person(name="Alice", age=30, email="alice@example.com")
    print(f"Valid person: {person.model_dump()}")
    
    # Invalid age (will raise error)
    try:
        invalid = Person(name="Bob", age=200, email="bob@example.com")
    except ValidationError as e:
        print(f"\nValidation error: {e.errors()[0]['msg']}\n")


def nested_models_demo():
    """Nested Pydantic models"""
    print("=== Nested Models ===\n")
    
    employee = Employee(
        name="John Doe",
        employee_id=12345,
        department="Engineering",
        address=Address(
            street="123 Main St",
            city="San Francisco",
            country="USA",
            postal_code="94102"
        ),
        skills=["Python", "LangChain", "AI"],
        priority=Priority.HIGH
    )
    
    print(f"Employee data:\n{employee.model_dump_json(indent=2)}\n")


def llm_structured_output():
    """Extract structured data with LLM"""
    print("=== LLM Structured Output ===\n")
    
    class Movie(BaseModel):
        title: str = Field(description="Movie title")
        year: int = Field(description="Release year")
        genre: str = Field(description="Movie genre")
        rating: float = Field(description="Rating out of 10", ge=0, le=10)
    
    llm = ChatOllama(model="llama3.2", format="json", temperature=0)
    parser = JsonOutputParser(pydantic_object=Movie)
    
    prompt = ChatPromptTemplate.from_template("""
Extract movie information from the text and return as JSON.

Format: {format_instructions}

Text: {text}

JSON:""")
    
    chain = prompt | llm | parser
    
    text = "The Matrix came out in 1999. It's a sci-fi action film rated 8.7/10."
    result = chain.invoke({
        "text": text,
        "format_instructions": parser.get_format_instructions()
    })
    
    print(f"Input: {text}")
    print(f"Extracted: {result}\n")


def batch_processing_demo():
    """Process multiple items"""
    print("=== Batch Processing ===\n")
    
    class Product(BaseModel):
        name: str
        price: float = Field(ge=0)
        in_stock: bool
    
    texts = [
        "iPhone 15 costs $999 and is available",
        "MacBook Pro is $2499 but out of stock",
        "AirPods are $199 and in stock"
    ]
    
    llm = ChatOllama(model="llama3.2", format="json", temperature=0)
    parser = JsonOutputParser(pydantic_object=Product)
    
    prompt = ChatPromptTemplate.from_template("""
Extract product info as JSON: {text}

{format_instructions}
""")
    
    chain = prompt | llm | parser
    
    for text in texts:
        try:
            result = chain.invoke({
                "text": text,
                "format_instructions": parser.get_format_instructions()
            })
            print(f"✓ {result}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print()


def validation_demo():
    """Custom validation"""
    print("=== Custom Validation ===\n")
    
    class Email(BaseModel):
        address: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
        verified: bool = False
        
        @validator('address')
        def lowercase_email(cls, v):
            return v.lower()
    
    # Valid email
    email1 = Email(address="Alice@Example.COM")
    print(f"Valid email (lowercased): {email1.address}")
    
    # Invalid email
    try:
        email2 = Email(address="invalid-email")
    except ValidationError as e:
        print(f"Invalid email error: {e.errors()[0]['msg']}\n")


if __name__ == "__main__":
    print("Structured Output Demo\n")
    print("=" * 60 + "\n")
    
    try:
        basic_pydantic_demo()
        nested_models_demo()
        llm_structured_output()
        batch_processing_demo()
        validation_demo()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
