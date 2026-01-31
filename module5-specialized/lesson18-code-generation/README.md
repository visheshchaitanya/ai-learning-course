# Lesson 18: Code Generation

## Theory

Using specialized code models to generate, test, and validate code.

### CodeLlama

Specialized for code generation, completion, and explanation.

```python
from ollama import chat

response = chat(
    model='codellama',
    messages=[{
        'role': 'user',
        'content': 'Write a Python function to calculate fibonacci numbers'
    }]
)
```

### Patterns
1. **Function Generation**: Create functions from descriptions
2. **Test Generation**: Generate unit tests
3. **Code Explanation**: Document existing code
4. **Refactoring**: Improve code quality
5. **Bug Fixing**: Identify and fix issues

### Validation

Always validate generated code:
- Syntax checking (ast.parse)
- Static analysis (pylint, mypy)
- Unit tests
- Security scanning

### Validation Pipeline

```python
def validate_generated_code(code: str) -> dict:
    """Validate generated code"""
    results = {
        "syntax_valid": False,
        "has_docstring": False,
        "has_tests": False,
        "passes_tests": False
    }
    
    # Syntax check
    try:
        ast.parse(code)
        results["syntax_valid"] = True
    except SyntaxError:
        return results
    
    # Check for docstrings
    results["has_docstring"] = '"""' in code or "'''" in code
    
    # Additional checks...
    return results
```

## Challenge

Build a **Code Generator** that:
- Takes feature description
- Generates Python function with CodeLlama
- Creates unit tests
- Validates syntax with ast.parse()
- Runs tests
- Provides feedback

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [CodeLlama](https://ollama.com/library/codellama)
- [Code Generation Guide](https://python.langchain.com/docs/use_cases/code_understanding/)
- [AST Module](https://docs.python.org/3/library/ast.html)
