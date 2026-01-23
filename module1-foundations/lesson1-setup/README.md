# Lesson 1: Environment Setup & First LLM Call

## Theory

### What are LLMs?
Large Language Models (LLMs) are neural networks trained on massive amounts of text data. They predict the next token (word/subword) based on context, enabling them to:
- Generate human-like text
- Answer questions
- Translate languages
- Write code
- Reason through problems

### Open-source vs Proprietary Models
**Open-source (Llama, Mistral, Gemma):**
- Run locally, no API costs
- Full control over data privacy
- Can be fine-tuned
- Require local compute resources

**Proprietary (GPT-4, Claude):**
- Accessed via API
- Pay per token
- Often more capable
- No local setup needed

### Ollama
Ollama simplifies running open-source LLMs locally:
- Easy model management (`ollama pull`, `ollama list`)
- REST API for integration
- Supports many popular models
- Handles model loading and GPU acceleration

## Demo

See `demo.py` for complete examples.

### Installation Steps

1. Install Ollama from https://ollama.com/download
2. Pull a model: `ollama pull llama3.2`
3. Install Python package: `pip install ollama`

### Basic Usage

```python
from ollama import chat

response = chat(model='llama3.2', messages=[
    {'role': 'user', 'content': 'Why is the sky blue?'}
])
print(response['message']['content'])
```

### Streaming Responses

```python
for chunk in chat(model='llama3.2', messages=[...], stream=True):
    print(chunk['message']['content'], end='', flush=True)
```

### Understanding Tokens
- Tokens are pieces of words (roughly 4 chars = 1 token)
- Context window: max tokens the model can process at once
- llama3.2: 128k token context window

## Challenge

Build a CLI chatbot that:
1. Maintains conversation history (last 5 messages)
2. Uses streaming responses
3. Allows user to type "quit" to exit
4. Shows token count for each response

**Starter code in `challenge.py`**

## Resources

- Ollama Docs: https://ollama.com/docs
- Ollama Python: https://github.com/ollama/ollama-python
- Model Library: https://ollama.com/library
