"""
Lesson 8 Solution: Email Parser
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
import json


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


class EmailContact(BaseModel):
    name: Optional[str] = Field(default=None, description="Contact name")
    email: str = Field(description="Email address")
    
    @validator('email')
    def lowercase_email(cls, v):
        return v.lower()


class ParsedEmail(BaseModel):
    sender: EmailContact
    recipients: List[EmailContact]
    subject: str
    sentiment: Sentiment
    action_items: List[str] = Field(default_factory=list)
    priority: Priority
    category: Category


def parse_email(email_text: str) -> ParsedEmail:
    """Parse email text into structured format"""
    llm = ChatOllama(model="llama3.2", format="json", temperature=0)
    parser = JsonOutputParser(pydantic_object=ParsedEmail)
    
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
    
    chain = prompt | llm | parser
    
    result = chain.invoke({
        "email_text": email_text,
        "format_instructions": parser.get_format_instructions()
    })
    
    return ParsedEmail(**result)


def main():
    """Test email parser"""
    sample_emails = [
        """
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
""",
        """
From: john@example.com
To: jane@example.com
Subject: Weekend Plans

Hey Jane,

Hope you're doing well! Want to grab coffee this weekend?

Let me know!
John
""",
        """
From: noreply@spam.com
To: victim@email.com
Subject: You've won $1,000,000!!!

Congratulations! Click here to claim your prize now!
"""
    ]
    
    print("=" * 60)
    print("Email Parser")
    print("=" * 60 + "\n")
    
    for i, email in enumerate(sample_emails, 1):
        print(f"Email {i}:")
        print(email.strip())
        print("\n" + "-" * 60 + "\n")
        
        try:
            result = parse_email(email)
            print("Parsed Output:")
            print(result.model_dump_json(indent=2))
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
