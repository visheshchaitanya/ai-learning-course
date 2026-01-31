"""
Lesson 8 Challenge: Email Parser

Extract structured data from email text including:
- Sender/recipients
- Subject
- Sentiment
- Action items
- Priority
- Category
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
import traceback


# TODO: Define enums
class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Category(str, Enum):
    WORK = "work"
    PERSONAL = "personal"
    SPAM = "spam"


# TODO: Define models
class EmailContact(BaseModel):
    name: Optional[str] = Field(default=None, description="Contact name")
    email: str = Field(description="Email address", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')


class ParsedEmail(BaseModel):
    sender: EmailContact
    recipients: List[EmailContact]
    subject: str
    sentiment: Sentiment
    action_items: List[str] = Field(default_factory=list)
    priority: Priority
    category: Category = Field(default=Category.WORK, description="Email category: work, personal, or spam")


def parse_email(email_text: str) -> ParsedEmail:
    """Parse email text into structured format"""
    # TODO: Implement email parsing with LLM
    llm = ChatOllama(model="llama3.2", format="json", temperature=0)
    prompt = ChatPromptTemplate.from_template("""
Parse the following email and extract structured information.

Email:
{email_text}

Return JSON with this exact structure:
{format_instructions}

Analyze the email content to determine:
- sentiment: positive/neutral/negative based on tone
- priority: low/medium/high based on urgency indicators
- category: work/personal/spam based on content
- action_items: numbered or bulleted tasks mentioned

JSON:""")
    
    chain = prompt | llm | JsonOutputParser(pydantic_object=ParsedEmail)
    
    result = chain.invoke({
        "email_text": email_text,
        "format_instructions": JsonOutputParser(pydantic_object=ParsedEmail).get_format_instructions()
    })
    
    return ParsedEmail(**result)


def main():
    """Test email parser"""
    sample_email = """
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
"""
    
    print("=" * 60)
    print("Email Parser")
    print("=" * 60 + "\n")
    
    print("Input Email:")
    print(sample_email)
    print("\n" + "=" * 60 + "\n")
    
    try:
        result = parse_email(sample_email)
        print("Parsed Output:")
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
