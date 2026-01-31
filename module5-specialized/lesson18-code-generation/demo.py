"""
Lesson 18 Demo: Code Generation with CodeLlama

Note: Requires codellama model: ollama pull codellama
"""

print("Code Generation Demo")
print("=" * 70)
print("\nThis demo requires:")
print("  1. Ollama running: ollama serve")
print("  2. CodeLlama model: ollama pull codellama")
print("\nExample usage:")
print("""
from ollama import chat
import ast

# Generate function
response = chat(
    model='codellama',
    messages=[{
        'role': 'user',
        'content': '''Write a Python function to calculate factorial.
        Include docstring and type hints.'''
    }]
)

code = response['message']['content']

# Validate syntax
try:
    ast.parse(code)
    print("✅ Syntax valid")
except SyntaxError as e:
    print(f"❌ Syntax error: {e}")

# Generate tests
test_prompt = f'''Write pytest tests for this function:
{code}
'''

test_response = chat(model='codellama', messages=[{
    'role': 'user',
    'content': test_prompt
}])

tests = test_response['message']['content']
""")
print("\nSee challenge.py and solution.py for complete examples")
