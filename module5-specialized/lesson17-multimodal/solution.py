"""Lesson 17 Solution: Receipt Analyzer with Vision Model"""
print("Solution: Receipt Analyzer")
print("=" * 70)
print("\nImplementation approach:")
print("  1. Use ollama.chat() with llama3.2-vision model")
print("  2. Pass receipt image in 'images' parameter")
print("  3. Prompt for structured JSON extraction")
print("  4. Parse JSON response")
print("  5. Validate and categorize items")
print("  6. Calculate totals")
print("  7. Export results")
print("\nKey code:")
print("""
from ollama import chat
import json

def analyze_receipt(image_path):
    response = chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': '''Extract all items and prices from this receipt.
            Return as JSON: {"items": [{"name": "...", "price": 0.00}], "total": 0.00}''',
            'images': [image_path]
        }]
    )
    
    # Parse JSON from response
    data = json.loads(response['message']['content'])
    
    # Categorize items
    for item in data['items']:
        item['category'] = categorize_item(item['name'])
    
    return data
""")
print("\nSee demo.py for more examples")
