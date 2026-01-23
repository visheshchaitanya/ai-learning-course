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

## Challenge

Build a **Receipt Analyzer** that extracts items, prices, totals, and categorizes expenses from receipt images.

See `demo.py`, `challenge.py`, `solution.py`, `images/`, and `outputs/` for examples.

## Resources
- [Llama 3.2 Vision](https://ollama.com/library/llama3.2-vision)
- [Multimodal RAG](https://python.langchain.com/docs/use_cases/multimodal/)
