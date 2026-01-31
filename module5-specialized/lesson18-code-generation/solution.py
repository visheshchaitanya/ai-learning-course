"""Lesson 18 Solution: Code Generator with Validation"""
print("Solution: Code Generator")
print("=" * 70)
print("\nImplementation approach:")
print("  1. Use CodeLlama model via ollama")
print("  2. Generate function from description")
print("  3. Validate with ast.parse()")
print("  4. Generate tests")
print("  5. Execute tests in isolated namespace")
print("\nKey code:")
print("""
from ollama import chat
import ast

def generate_function(description: str) -> str:
    response = chat(
        model='codellama',
        messages=[{
            'role': 'user',
            'content': f'''Write a Python function: {description}
            Include:
            - Docstring
            - Type hints
            - Error handling
            Return only the code, no explanations.'''
        }]
    )
    return response['message']['content']

def validate_syntax(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def generate_tests(code: str) -> str:
    response = chat(
        model='codellama',
        messages=[{
            'role': 'user',
            'content': f'''Write pytest tests for this code:
            {code}
            Include edge cases and error conditions.'''
        }]
    )
    return response['message']['content']
""")
print("\nSee demo.py for more examples")
