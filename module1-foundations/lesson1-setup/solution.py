"""
Lesson 1 Challenge Solution: CLI Chatbot with History
"""

from ollama import chat


def estimate_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters)"""
    return len(text) // 4


def main():
    """Main chatbot loop"""
    print("=" * 60)
    print("CLI Chatbot - Type 'quit' to exit, '/clear' to reset")
    print("=" * 60 + "\n")
    
    messages = []
    total_tokens = 0
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print(f"\nTotal tokens used: ~{total_tokens}")
            print("Goodbye!")
            break
        
        if user_input.lower() == '/clear':
            messages = []
            total_tokens = 0
            print("History cleared!\n")
            continue
        
        # Add user message
        messages.append({'role': 'user', 'content': user_input})
        
        # Keep only last 10 messages (5 user + 5 assistant)
        if len(messages) > 10:
            messages = messages[-10:]
        
        # Stream response
        print("Assistant: ", end='', flush=True)
        full_response = ""
        
        try:
            for chunk in chat(model='llama3.2', messages=messages, stream=True):
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
        except Exception as e:
            print(f"\nError: {e}")
            messages.pop()  # Remove failed user message
            continue
        
        # Add assistant response to history
        messages.append({'role': 'assistant', 'content': full_response})
        
        # Calculate tokens
        response_tokens = estimate_tokens(full_response)
        total_tokens += response_tokens
        print(f"\n[~{response_tokens} tokens]\n")


if __name__ == "__main__":
    main()
