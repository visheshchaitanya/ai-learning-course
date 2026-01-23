"""
Lesson 6 Demo: Tools and Function Calling
"""

from langchain.tools import tool, StructuredTool, BaseTool
from pydantic import BaseModel, Field
from typing import Optional
import math


# Method 1: Simple @tool decorator
@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression like '2 + 2' or '10 * 5'."""
    try:
        # Safe evaluation (in production, use ast.literal_eval or a proper parser)
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Method 2: Tool with multiple parameters
@tool
def multiply_numbers(a: float, b: float) -> str:
    """Multiply two numbers together."""
    result = a * b
    return f"{a} × {b} = {result}"


# Method 3: Tool with Pydantic validation
class TemperatureInput(BaseModel):
    celsius: float = Field(description="Temperature in Celsius")

@tool(args_schema=TemperatureInput)
def celsius_to_fahrenheit(celsius: float) -> str:
    """Convert temperature from Celsius to Fahrenheit."""
    fahrenheit = (celsius * 9/5) + 32
    return f"{celsius}°C = {fahrenheit}°F"


# Method 4: StructuredTool
def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle given its radius."""
    return math.pi * radius ** 2

circle_area_tool = StructuredTool.from_function(
    func=calculate_circle_area,
    name="CircleArea",
    description="Calculate the area of a circle. Input is the radius."
)


# Method 5: BaseTool class (most control)
class PowerInput(BaseModel):
    base: float = Field(description="The base number")
    exponent: float = Field(description="The exponent")

class PowerTool(BaseTool):
    name = "power_calculator"
    description = "Calculate base raised to exponent (base^exponent)"
    args_schema = PowerInput
    
    def _run(self, base: float, exponent: float) -> str:
        """Execute the tool."""
        try:
            result = base ** exponent
            return f"{base}^{exponent} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, base: float, exponent: float) -> str:
        """Async version (optional)."""
        return self._run(base, exponent)


# Tool with error handling
@tool
def divide_numbers(a: float, b: float) -> str:
    """Divide two numbers. Returns error if dividing by zero."""
    try:
        if b == 0:
            return "Error: Cannot divide by zero"
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool that reads files
@tool
def read_file(filepath: str) -> str:
    """Read contents of a text file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return f"File content ({len(content)} characters):\n{content[:200]}..."
    except FileNotFoundError:
        return f"Error: File '{filepath}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


# Tool that writes files
@tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a text file."""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {filepath}"
    except Exception as e:
        return f"Error: {str(e)}"


def demo_basic_tools():
    """Demonstrate basic tool usage"""
    print("=== Basic Tool Usage ===\n")
    
    # Direct invocation
    result = calculator.invoke({"expression": "2 + 2 * 3"})
    print(f"Calculator: {result}")
    
    result = multiply_numbers.invoke({"a": 7, "b": 6})
    print(f"Multiply: {result}")
    
    result = celsius_to_fahrenheit.invoke({"celsius": 25})
    print(f"Temperature: {result}\n")


def demo_structured_tool():
    """Demonstrate StructuredTool"""
    print("=== StructuredTool ===\n")
    
    result = circle_area_tool.invoke({"radius": 5})
    print(f"Circle area: {result}\n")


def demo_base_tool():
    """Demonstrate BaseTool"""
    print("=== BaseTool (Custom Class) ===\n")
    
    power_tool = PowerTool()
    result = power_tool.invoke({"base": 2, "exponent": 10})
    print(f"Power: {result}\n")


def demo_error_handling():
    """Demonstrate error handling"""
    print("=== Error Handling ===\n")
    
    result1 = divide_numbers.invoke({"a": 10, "b": 2})
    print(f"Valid division: {result1}")
    
    result2 = divide_numbers.invoke({"a": 10, "b": 0})
    print(f"Division by zero: {result2}")
    
    result3 = calculator.invoke({"expression": "invalid"})
    print(f"Invalid expression: {result3}\n")


def demo_file_tools():
    """Demonstrate file operation tools"""
    print("=== File Operation Tools ===\n")
    
    # Write a file
    test_file = "demo_test.txt"
    write_result = write_file.invoke({
        "filepath": test_file,
        "content": "Hello from LangChain tools!\nThis is a test file."
    })
    print(write_result)
    
    # Read the file
    read_result = read_file.invoke({"filepath": test_file})
    print(read_result)
    
    # Clean up
    import os
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"\nCleaned up {test_file}\n")


def demo_tool_metadata():
    """Show tool metadata"""
    print("=== Tool Metadata ===\n")
    
    tools = [calculator, multiply_numbers, celsius_to_fahrenheit, divide_numbers]
    
    for tool_obj in tools:
        print(f"Name: {tool_obj.name}")
        print(f"Description: {tool_obj.description}")
        print(f"Args: {tool_obj.args}\n")


def demo_multiple_tools():
    """Use multiple tools together"""
    print("=== Multiple Tools Working Together ===\n")
    
    # Calculate circle area, then convert to string for display
    radius = 7
    area = circle_area_tool.invoke({"radius": radius})
    print(f"Circle with radius {radius} has area: {area}")
    
    # Calculate and compare temperatures
    temps_c = [0, 25, 100]
    print("\nTemperature conversions:")
    for temp in temps_c:
        result = celsius_to_fahrenheit.invoke({"celsius": temp})
        print(f"  {result}")
    print()


if __name__ == "__main__":
    print("Tools Demo\n")
    print("=" * 60 + "\n")
    
    try:
        demo_basic_tools()
        demo_structured_tool()
        demo_base_tool()
        demo_error_handling()
        demo_file_tools()
        demo_tool_metadata()
        demo_multiple_tools()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
