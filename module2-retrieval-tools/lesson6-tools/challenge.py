"""
Lesson 6 Challenge: Tool Suite

Create a comprehensive tool suite with:
1. Calculator
2. Unit Converter
3. Date Calculator
4. Text Analyzer
5. File Operations
"""

from langchain.tools import tool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Literal


# TODO: Implement Calculator Tool
@tool
def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    # TODO: Implement safe evaluation
    # Consider using ast.literal_eval or a proper parser
    pass


# TODO: Implement Unit Converter Tool
class UnitConversionInput(BaseModel):
    value: float = Field(description="The value to convert")
    from_unit: str = Field(description="Source unit (e.g., 'cm', 'kg', 'celsius')")
    to_unit: str = Field(description="Target unit (e.g., 'inches', 'lbs', 'fahrenheit')")

@tool(args_schema=UnitConversionInput)
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between different units of measurement."""
    # TODO: Implement conversions for:
    # - Length: cm, m, km, inches, feet, miles
    # - Weight: g, kg, lbs, oz
    # - Temperature: celsius, fahrenheit, kelvin
    pass


# TODO: Implement Date Calculator
@tool
def days_between_dates(date1: str, date2: str) -> str:
    """Calculate days between two dates (format: YYYY-MM-DD)."""
    # TODO: Parse dates and calculate difference
    pass


@tool
def add_days_to_date(date: str, days: int) -> str:
    """Add or subtract days from a date (format: YYYY-MM-DD)."""
    # TODO: Add days to date
    pass


# TODO: Implement Text Analyzer
@tool
def analyze_text(text: str) -> str:
    """Analyze text and return word count, character count, and sentence count."""
    # TODO: Count words, characters, sentences
    pass


# TODO: Implement File Tools
@tool
def read_text_file(filepath: str) -> str:
    """Read and return contents of a text file."""
    # TODO: Read file with error handling
    pass


@tool
def write_text_file(filepath: str, content: str) -> str:
    """Write content to a text file."""
    # TODO: Write file with error handling
    pass


def test_tools():
    """Test all tools"""
    print("=" * 60)
    print("Tool Suite Test")
    print("=" * 60 + "\n")
    
    # TODO: Test calculator
    print("Calculator:")
    # result = calculator.invoke({"expression": "2 + 2 * 3"})
    # print(f"  2 + 2 * 3 = {result}\n")
    
    # TODO: Test unit converter
    print("Unit Converter:")
    # result = convert_units.invoke({"value": 100, "from_unit": "cm", "to_unit": "inches"})
    # print(f"  {result}\n")
    
    # TODO: Test date calculator
    print("Date Calculator:")
    # result = days_between_dates.invoke({"date1": "2024-01-01", "date2": "2024-12-31"})
    # print(f"  {result}\n")
    
    # TODO: Test text analyzer
    print("Text Analyzer:")
    # result = analyze_text.invoke({"text": "Hello world! This is a test."})
    # print(f"  {result}\n")
    
    # TODO: Test file operations
    print("File Operations:")
    # write_result = write_text_file.invoke({"filepath": "test.txt", "content": "Test content"})
    # print(f"  Write: {write_result}")
    # read_result = read_text_file.invoke({"filepath": "test.txt"})
    # print(f"  Read: {read_result}\n")


def interactive_cli():
    """Interactive CLI to test tools"""
    print("\n" + "=" * 60)
    print("Interactive Tool Testing")
    print("=" * 60)
    print("\nAvailable tools:")
    print("  1. calculator")
    print("  2. convert_units")
    print("  3. days_between_dates")
    print("  4. add_days_to_date")
    print("  5. analyze_text")
    print("  6. read_text_file")
    print("  7. write_text_file")
    print("  q. quit\n")
    
    while True:
        choice = input("Select a tool (1-7, q to quit): ").strip()
        
        if choice == 'q':
            break
        
        # TODO: Implement interactive tool testing
        # Get inputs from user and invoke the selected tool
        
        print()


if __name__ == "__main__":
    test_tools()
    # interactive_cli()
