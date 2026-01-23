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

## Challenge

Build a **Code Generator** that takes a feature description, generates Python code, writes tests, and validates the output.

See `demo.py`, `challenge.py`, `solution.py`, and `templates/` for examples.

## Resources
- [CodeLlama](https://ollama.com/library/codellama)
- [Code Generation Guide](https://python.langchain.com/docs/use_cases/code_understanding/)
