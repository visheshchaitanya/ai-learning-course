# Lesson 6: Tools & Function Calling

## Theory

### What are Tools?

Tools extend LLM capabilities by allowing them to:
- Perform calculations
- Access external APIs
- Read/write files
- Query databases
- Execute code

**Without Tools**: LLM can only generate text  
**With Tools**: LLM can take actions in the world

### Tool Anatomy

A tool consists of:
1. **Name**: Identifier for the tool
2. **Description**: What it does (LLM uses this to decide when to use it)
3. **Parameters**: Inputs the tool accepts
4. **Function**: The actual code that runs

### Creating Tools in LangChain

**Method 1: @tool Decorator**
```python
from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return str(eval(expression))
```

**Method 2: StructuredTool**
```python
from langchain.tools import StructuredTool

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tool = StructuredTool.from_function(
    func=multiply,
    name="Multiply",
    description="Multiply two integers together"
)
```

**Method 3: BaseTool Class**
```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate math expressions"
    args_schema = CalculatorInput
    
    def _run(self, expression: str) -> str:
        return str(eval(expression))
```

### Tool Descriptions

The description is crucial—it tells the LLM when to use the tool:

**Bad**: "A tool"  
**Good**: "Calculate mathematical expressions like '2 + 2' or '10 * 5'"

**Bad**: "Search"  
**Good**: "Search Wikipedia for factual information about people, places, and events"

### Tool Parameters with Pydantic

Use Pydantic for type validation:

```python
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="City name, e.g., 'San Francisco'")
    unit: str = Field(description="Temperature unit: 'celsius' or 'fahrenheit'")

@tool(args_schema=WeatherInput)
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get current weather for a location."""
    # API call here
    return f"Weather in {location}: 72°{unit[0].upper()}"
```

### Error Handling

Tools should handle errors gracefully:

```python
@tool
def divide(a: float, b: float) -> str:
    """Divide two numbers."""
    try:
        result = a / b
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Built-in Tools

LangChain provides many built-in tools:
- **WikipediaQueryRun**: Search Wikipedia
- **DuckDuckGoSearchRun**: Web search
- **PythonREPLTool**: Execute Python code
- **ShellTool**: Run shell commands
- **FileManagementToolkit**: File operations

### Tool Calling vs Function Calling

These terms are often used interchangeably, but there are important distinctions:

**Function Calling** (Native LLM Feature):
- Built into modern LLMs (GPT-4, GPT-3.5-turbo, Claude 3+, Gemini)
- LLM is trained to output structured JSON matching function schemas
- The model outputs: function name + arguments as JSON
- YOU execute the function and return results to the LLM
- Protocol: `functions` or `tools` parameter in API calls
- More reliable—model is specifically trained for this

Example flow:
```
User: "What's the weather in SF?"
→ LLM outputs: {"name": "get_weather", "arguments": {"location": "San Francisco"}}
→ You call get_weather("San Francisco")
→ You send result back to LLM
→ LLM responds: "It's 72°F in San Francisco"
```

**Tool Calling** (Framework Abstraction):
- LangChain/framework wrapper around function calling
- Provides unified interface across different LLMs
- Handles the execute-and-return loop automatically
- Works with models that don't have native function calling (via prompting)
- Includes tool definition, invocation, and result handling

Key differences:
- **Function calling** = LLM capability (model outputs structured function calls)
- **Tool calling** = Framework pattern (abstracts the entire flow)
- Function calling requires you to manually execute functions
- Tool calling can auto-execute and manage the loop

**For OpenAI/Anthropic**: Use native function calling (more reliable)  
**For Ollama/local models**: Use tool calling with prompt engineering (model may not be trained for it)

LangChain's tool abstraction works with both—it uses native function calling when available, falls back to prompting otherwise.

## Demo

See `demo.py` for examples:
1. Basic tool with @tool decorator
2. Tool with multiple parameters
3. Tool with Pydantic validation
4. Error handling in tools
5. Multiple tools working together
6. Built-in tools (Wikipedia, calculator)
7. Custom file operations tool

### Quick Example

```python
from langchain.tools import tool

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def reverse_string(text: str) -> str:
    """Reverses a string."""
    return text[::-1]

# Tools can be used directly
result = get_word_length.invoke({"word": "hello"})
print(result)  # 5

# Or with an agent (next lesson)
```

## Challenge

Build a **Tool Suite** with:

1. **Calculator Tool**: Evaluate math expressions safely
2. **Unit Converter Tool**: Convert between units (length, weight, temperature)
3. **Date Calculator Tool**: Calculate days between dates, add/subtract days
4. **Text Analyzer Tool**: Count words, characters, sentences
5. **File Tool**: Read/write text files

**Requirements:**
- Use Pydantic for input validation
- Add comprehensive descriptions
- Handle errors gracefully
- Create a simple CLI to test tools
- Tools should work independently (no LLM needed for testing)

**Bonus:**
- Add a currency converter tool (with API)
- Create a tool that uses another tool
- Add async support for API calls
- Implement tool usage logging

**Starter code in `challenge.py`**

**Example Usage:**
```python
# Calculator
calculator.invoke({"expression": "2 + 2 * 3"})
# "8"

# Unit Converter
convert_units.invoke({"value": 100, "from_unit": "cm", "to_unit": "inches"})
# "39.37 inches"

# Date Calculator
days_between.invoke({"date1": "2024-01-01", "date2": "2024-12-31"})
# "365 days"

# Text Analyzer
analyze_text.invoke({"text": "Hello world! This is a test."})
# "Words: 6, Characters: 28, Sentences: 2"
```

## Resources

- [Tools Documentation](https://python.langchain.com/docs/modules/agents/tools/)
- [Custom Tools Guide](https://python.langchain.com/docs/modules/agents/tools/custom_tools/)
- [Tool Calling](https://python.langchain.com/docs/modules/model_io/chat/function_calling/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
