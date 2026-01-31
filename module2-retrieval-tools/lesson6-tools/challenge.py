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
import re
import os


@tool
def calculator(expression: str) -> str:
    """Safely evaluate a mathematical expression like '2 + 2' or '10 * 5'."""
    try:
        # Remove any non-math characters for safety
        allowed = set('0123456789+-*/(). ')
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"


class UnitConversionInput(BaseModel):
    value: float = Field(description="The value to convert")
    from_unit: str = Field(description="Source unit")
    to_unit: str = Field(description="Target unit")

@tool(args_schema=UnitConversionInput)
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between units. Supports length (cm/m/km/in/ft/mi), weight (g/kg/lb/oz), temp (C/F/K)."""
    
    # Length conversions (to meters)
    length_to_m = {
        'cm': 0.01, 'm': 1, 'km': 1000,
        'in': 0.0254, 'inch': 0.0254, 'inches': 0.0254,
        'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048,
        'mi': 1609.34, 'mile': 1609.34, 'miles': 1609.34
    }
    
    # Weight conversions (to grams)
    weight_to_g = {
        'g': 1, 'kg': 1000,
        'lb': 453.592, 'lbs': 453.592, 'pound': 453.592, 'pounds': 453.592,
        'oz': 28.3495, 'ounce': 28.3495, 'ounces': 28.3495
    }
    
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Length conversion
    if from_unit in length_to_m and to_unit in length_to_m:
        meters = value * length_to_m[from_unit]
        result = meters / length_to_m[to_unit]
        return f"{value} {from_unit} = {result:.2f} {to_unit}"
    
    # Weight conversion
    if from_unit in weight_to_g and to_unit in weight_to_g:
        grams = value * weight_to_g[from_unit]
        result = grams / weight_to_g[to_unit]
        return f"{value} {from_unit} = {result:.2f} {to_unit}"
    
    # Temperature conversion
    if from_unit in ['c', 'celsius'] and to_unit in ['f', 'fahrenheit']:
        result = (value * 9/5) + 32
        return f"{value}°C = {result:.2f}°F"
    elif from_unit in ['f', 'fahrenheit'] and to_unit in ['c', 'celsius']:
        result = (value - 32) * 5/9
        return f"{value}°F = {result:.2f}°C"
    elif from_unit in ['c', 'celsius'] and to_unit in ['k', 'kelvin']:
        result = value + 273.15
        return f"{value}°C = {result:.2f}K"
    elif from_unit in ['k', 'kelvin'] and to_unit in ['c', 'celsius']:
        result = value - 273.15
        return f"{value}K = {result:.2f}°C"
    
    return f"Error: Cannot convert from '{from_unit}' to '{to_unit}'"


@tool
def days_between_dates(date1: str, date2: str) -> str:
    """Calculate days between two dates (format: YYYY-MM-DD)."""
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        diff = abs((d2 - d1).days)
        return f"{diff} days between {date1} and {date2}"
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def add_days_to_date(date: str, days: int) -> str:
    """Add or subtract days from a date (format: YYYY-MM-DD)."""
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        new_date = d + timedelta(days=days)
        return f"{date} + {days} days = {new_date.strftime('%Y-%m-%d')}"
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def analyze_text(text: str) -> str:
    """Analyze text and return word count, character count, and sentence count."""
    try:
        # Word count
        words = len(text.split())
        
        # Character count (with and without spaces)
        chars_with_spaces = len(text)
        chars_without_spaces = len(text.replace(' ', ''))
        
        # Sentence count (approximate)
        sentences = len(re.split(r'[.!?]+', text.strip()))
        
        return (f"Words: {words}, Characters: {chars_with_spaces} "
                f"(without spaces: {chars_without_spaces}), Sentences: {sentences}")
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def read_text_file(filepath: str) -> str:
    """Read and return contents of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"File: {filepath} ({len(content)} characters)\n\n{content}"
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def write_text_file(filepath: str, content: str) -> str:
    """Write content to a text file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{filepath}'"
    except Exception as e:
        return f"Error: {str(e)}"


def test_tools():
    """Test all tools"""
    print("=" * 60)
    print("Tool Suite Test")
    print("=" * 60 + "\n")
    
    print("Calculator:")
    print(f"  {calculator.invoke({'expression': '2 + 2 * 3'})}")
    print(f"  {calculator.invoke({'expression': '(10 + 5) / 3'})}\n")
    
    print("Unit Converter:")
    print(f"  {convert_units.invoke({'value': 100, 'from_unit': 'cm', 'to_unit': 'inches'})}")
    print(f"  {convert_units.invoke({'value': 5, 'from_unit': 'kg', 'to_unit': 'lbs'})}")
    print(f"  {convert_units.invoke({'value': 25, 'from_unit': 'celsius', 'to_unit': 'fahrenheit'})}\n")
    
    print("Date Calculator:")
    print(f"  {days_between_dates.invoke({'date1': '2024-01-01', 'date2': '2024-12-31'})}")
    print(f"  {add_days_to_date.invoke({'date': '2024-01-01', 'days': 100})}\n")
    
    print("Text Analyzer:")
    text = "Hello world! This is a test. How are you?"
    print(f"  {analyze_text.invoke({'text': text})}\n")
    
    print("File Operations:")
    test_file = "tool_test.txt"
    write_result = write_text_file.invoke({'filepath': test_file, 'content': 'Test content from tools!'})
    print(f"  Write: {write_result}")
    read_result = read_text_file.invoke({'filepath': test_file})
    print(f"  Read: {read_result[:80]}...")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"  Cleaned up {test_file}\n")


def interactive_cli():
    """Interactive CLI to test tools"""
    print("\n" + "=" * 60)
    print("Interactive Tool Testing")
    print("=" * 60)
    print("\nAvailable tools:")
    print("  1. calculator - Evaluate math expression")
    print("  2. convert_units - Convert between units")
    print("  3. days_between_dates - Calculate days between dates")
    print("  4. add_days_to_date - Add days to a date")
    print("  5. analyze_text - Analyze text statistics")
    print("  6. read_text_file - Read a file")
    print("  7. write_text_file - Write to a file")
    print("  q. quit\n")
    
    while True:
        choice = input("Select a tool (1-7, q to quit): ").strip()
        
        if choice == 'q':
            break
        
        try:
            if choice == '1':
                expr = input("  Expression: ")
                print(f"  {calculator.invoke({'expression': expr})}\n")
            
            elif choice == '2':
                value = float(input("  Value: "))
                from_unit = input("  From unit: ")
                to_unit = input("  To unit: ")
                print(f"  {convert_units.invoke({'value': value, 'from_unit': from_unit, 'to_unit': to_unit})}\n")
            
            elif choice == '3':
                date1 = input("  Date 1 (YYYY-MM-DD): ")
                date2 = input("  Date 2 (YYYY-MM-DD): ")
                print(f"  {days_between_dates.invoke({'date1': date1, 'date2': date2})}\n")
            
            elif choice == '4':
                date = input("  Date (YYYY-MM-DD): ")
                days = int(input("  Days to add: "))
                print(f"  {add_days_to_date.invoke({'date': date, 'days': days})}\n")
            
            elif choice == '5':
                text = input("  Text: ")
                print(f"  {analyze_text.invoke({'text': text})}\n")
            
            elif choice == '6':
                filepath = input("  File path: ")
                result = read_text_file.invoke({'filepath': filepath})
                print(f"  {result[:200]}...\n")
            
            elif choice == '7':
                filepath = input("  File path: ")
                content = input("  Content: ")
                print(f"  {write_text_file.invoke({'filepath': filepath, 'content': content})}\n")
            
            else:
                print("  Invalid choice\n")
        
        except Exception as e:
            print(f"  Error: {e}\n")


if __name__ == "__main__":
    test_tools()
    
    # Uncomment to run interactive mode
    # interactive_cli()
