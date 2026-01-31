"""
Lesson 17 Demo: Multimodal AI with Vision Models

Note: Requires llama3.2-vision model: ollama pull llama3.2-vision
"""

print("Multimodal AI Demo")
print("=" * 70)
print("\nThis demo requires:")
print("  1. Ollama running: ollama serve")
print("  2. Vision model: ollama pull llama3.2-vision")
print("  3. Sample images in current directory")
print("\nExample usage:")
print("""
from ollama import chat

# Describe image
response = chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'Describe this image',
        'images': ['image.jpg']
    }]
)
print(response['message']['content'])

# Extract text (OCR)
response = chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'Extract all text from this image',
        'images': ['receipt.jpg']
    }]
)

# Structured extraction
response = chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': '''Extract items and prices from this receipt.
        Format as JSON: {"items": [{"name": "...", "price": ...}]}''',
        'images': ['receipt.jpg']
    }]
)
""")
print("\nSee challenge.py and solution.py for complete examples")
