"""
Lesson 3 Challenge: Personality Chatbot with Persistent Memory

Build a chatbot that:
1. Has a personality (pirate, philosopher, comedian, etc.)
2. Remembers last 10 messages
3. Remembers user preferences across sessions
4. Saves/loads memory from JSON

Commands:
- /clear: Reset conversation history
- /prefs: Show user preferences
- /quit: Save and exit
"""

from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import json
import os


MEMORY_FILE = "chatbot_memory.json"


def load_memory():
    """Load memory from file if it exists"""
    # TODO: Implement loading logic
    # Return: (memory object, preferences dict)
    
    preferences = {}
    memory = ConversationBufferWindowMemory(k=10)
    
    if os.path.exists(MEMORY_FILE):
        # TODO: Load from file
        # Read JSON, extract messages and preferences
        # Restore messages to memory object
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            preferences = data.get("preferences", {})
            messages = data.get("messages", [])
            for msg in messages:
                if msg["type"] == "human":
                    memory.chat_memory.add_message(HumanMessage(content=msg["content"]))
                elif msg["type"] == "ai":
                    memory.chat_memory.add_message(AIMessage(content=msg["content"]))
        pass
    
    return memory, preferences


def save_memory(memory, preferences):
    """Save memory to file"""
    # TODO: Implement saving logic
    # Extract messages from memory
    # Combine with preferences
    # Save to JSON file
    messages = []
    for msg in memory.chat_memory.messages:
        messages.append({
            "type": msg.type,
            "content": msg.content
        })
    data = {
        "messages": messages,
        "preferences": preferences
    }
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Memory saved to {MEMORY_FILE}")


def extract_preferences(user_input: str, bot_response: str, preferences: dict):
    """Extract user preferences from conversation"""
    # TODO: Simple keyword-based extraction
    # Look for patterns like "My name is X", "I love X", etc.
    
    # Example patterns:
    # - "my name is X" -> preferences["name"] = X
    # - "I love X" -> preferences["interests"] = [X]
    # - "call me X" -> preferences["nickname"] = X
    
    user_lower = user_input.lower()
    
    # Name detection
    if "my name is" in user_lower:
        # TODO: Extract name
        preferences["name"] = user_input.split("my name is")[1].strip()
    
    if "call me" in user_lower:
        # TODO: Extract nickname
        preferences["nickname"] = user_input.split("call me")[1].strip()       
    
    # Interest detection
    if "i love" in user_lower or "i like" in user_lower:
        # TODO: Extract interest
        preferences["interests"] = user_input.split("i love")[1].strip()
    elif "i like" in user_lower:
        preferences["interests"] = user_input.split("i like")[1].strip()
    
    return preferences


def show_preferences(preferences):
    """Display user preferences"""
    print("\n" + "=" * 60)
    print("User Preferences:")
    if not preferences:
        print("  No preferences stored yet")
    else:
        for key, value in preferences.items():
            print(f"  {key.capitalize()}: {value}")
    print("=" * 60 + "\n")


def main():
    """Main chatbot loop"""
    print("=" * 60)
    print("Personality Chatbot")
    print("=" * 60)
    
    # Choose personality
    personalities = {
        "1": ("pirate", "You are a friendly pirate. Speak like a pirate with 'ahoy', 'matey', etc."),
        "2": ("philosopher", "You are a thoughtful philosopher. Respond with wisdom and deep questions."),
        "3": ("comedian", "You are a funny comedian. Make jokes and keep things light."),
        "4": ("scientist", "You are an enthusiastic scientist. Explain things with curiosity and precision.")
    }
    
    print("\nChoose a personality:")
    for key, (name, _) in personalities.items():
        print(f"  {key}. {name.capitalize()}")
    
    choice = input("\nEnter choice (1-4): ").strip()
    if choice not in personalities:
        choice = "1"
    
    personality_name, personality_prompt = personalities[choice]
    print(f"\nYou chose: {personality_name.capitalize()}")
    print("\nCommands: /clear, /prefs, /quit\n")
    print("=" * 60 + "\n")
    
    # TODO: Load memory and preferences
    memory, preferences = load_memory()
    
    if preferences:
        print(f"Welcome back! I remember you.\n")
    
    # TODO: Create LLM with personality
    llm = ChatOllama(model="llama3.2", temperature=0.8)
    
    # TODO: Create conversation chain with custom prompt
    # Include personality in system message
    
    # Simple approach: use ConversationChain with custom prompt
    prompt_template = PromptTemplate(
        input_variables=["history", "input"],
        template=f"""{personality_prompt}
        Current conversation:
        {{history}}
        Human: {{input}}
        Assistant:"""
    )
    
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt_template,
        verbose=False
    )
    
    # Main loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input == "/quit":
                # TODO: Save memory and exit
                print("\nSaving memory...")
                save_memory(memory, preferences)
                print("Goodbye!")
                break
            
            elif user_input == "/clear":
                # TODO: Clear conversation history
                memory.clear()
                print("\nConversation history cleared!\n")
                continue
            
            elif user_input == "/prefs":
                show_preferences(preferences)
                continue
            
            # TODO: Get bot response
            response = conversation.predict(input=user_input)
            
            print(f"Bot: {response}\n")
            
            # TODO: Extract and update preferences
            preferences = extract_preferences(user_input, response, preferences)
            
        except KeyboardInterrupt:
            print("\n\nSaving memory...")
            save_memory(memory, preferences)
            print("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
