# Lesson 17: Multimodal AI

## Theory

Working with vision models that understand both images and text.

### Capabilities
- Image description
- Visual question answering
- OCR and document analysis
- Chart/diagram understanding
- Image comparison

### Ollama Vision Models

```python
from ollama import chat

response = chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'What's in this image?',
        'images': ['path/to/image.jpg']
    }]
)
```

### Use Cases
- Receipt/invoice processing
- Document digitization
- Visual QA systems
- Content moderation
- Accessibility tools

### Best Practices

**Image Preprocessing:**
- Resize large images
- Ensure good contrast
- Crop to relevant area
- Convert to supported formats (JPEG, PNG)

**Prompt Engineering:**
- Be specific about what to extract
- Provide examples in prompt
- Ask for structured output
- Request confidence scores

**Error Handling:**
- Validate image format/size
- Handle OCR failures
- Provide fallback responses
- Log unclear results

## Challenge

Build a **Receipt Analyzer** that:
- Loads receipt images
- Extracts items and prices using vision model
- Categorizes expenses (food, transport, etc.)
- Calculates totals and validates
- Exports to JSON/CSV

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Llama 3.2 Vision](https://ollama.com/library/llama3.2-vision)
- [Multimodal RAG](https://python.langchain.com/docs/use_cases/multimodal/)
- [Ollama Vision API](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion)
