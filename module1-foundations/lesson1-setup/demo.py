"""
Lesson 1 Demo: First LLM Calls with Ollama
"""

from ollama import chat, list as list_models
import time


def basic_chat():
    """Simple chat example"""
    print("=== Basic Chat ===\n")
    
    response = chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': 'Explain quantum computing in one sentence.'}
        ]
    )
    
    print(f"Response: {response['message']['content']}\n")
    print(f"Model: {response['model']}")
    print(f"Total duration: {response.get('total_duration', 0) / 1e9:.2f}s\n")


def streaming_chat():
    """Streaming response example"""
    print("=== Streaming Chat ===\n")
    
    print("Assistant: ", end='', flush=True)
    
    start_time = time.time()
    for chunk in chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': 'Write a haiku about coding.'}
        ],
        stream=True
    ):
        print(chunk['message']['content'], end='', flush=True)
    
    elapsed = time.time() - start_time
    print(f"\n\nStreaming completed in {elapsed:.2f}s\n")


def conversation_with_history():
    """Multi-turn conversation"""
    print("=== Conversation with History ===\n")
    
    messages = [
        {'role': 'user', 'content': 'My name is Alice and I love Python.'},
    ]
    
    response = chat(model='llama3.2', messages=messages)
    print(f"User: {messages[0]['content']}")
    print(f"Assistant: {response['message']['content']}\n")
    
    # Add assistant response to history
    messages.append(response['message'])
    
    # Ask follow-up question
    messages.append({'role': 'user', 'content': 'What is my name and favorite language?'})
    
    response = chat(model='llama3.2', messages=messages)
    print(f"User: {messages[-1]['content']}")
    print(f"Assistant: {response['message']['content']}\n")


def list_available_models():
    """List all downloaded models"""
    print("=== Available Models ===\n")
    
    models = list_models()
    for model in models['models']:
        print(f"- {model['name']}")
        print(f"  Size: {model['size'] / 1e9:.2f} GB")
        print(f"  Modified: {model['modified_at']}\n")


def compare_temperatures():
    """Show effect of temperature parameter"""
    print("=== Temperature Comparison ===\n")
    
    prompt = "Complete this story in one sentence: The robot walked into the bar and"
    
    for temp in [0.0, 0.5, 1.0]:
        print(f"Temperature: {temp}")
        response = chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': temp}
        )
        print(f"Response: {response['message']['content']}\n")


if __name__ == "__main__":
    print("Ollama Demo - Make sure Ollama is running and llama3.2 is pulled!\n")
    print("Run: ollama pull llama3.2\n")
    print("=" * 60 + "\n")
    
    try:
        basic_chat()
        streaming_chat()
        conversation_with_history()
        list_available_models()
        compare_temperatures()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running: ollama serve")
