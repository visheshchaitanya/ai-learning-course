"""
Lesson 3 Solution: Personality Chatbot with Persistent Memory
"""

from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import json
import os
import re


MEMORY_FILE = "chatbot_memory.json"


def load_memory():
    """Load memory from file if it exists"""
    preferences = {}
    memory = ConversationBufferWindowMemory(k=10)
    
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
            
            preferences = data.get("preferences", {})
            messages = data.get("messages", [])
            
            # Restore messages to memory
            for msg in messages:
                if msg["type"] == "human":
                    memory.chat_memory.add_message(HumanMessage(content=msg["content"]))
                elif msg["type"] == "ai":
                    memory.chat_memory.add_message(AIMessage(content=msg["content"]))
            
            print(f"Loaded memory from {MEMORY_FILE}")
        except Exception as e:
            print(f"Could not load memory: {e}")
    
    return memory, preferences


def save_memory(memory, preferences):
    """Save memory to file"""
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
    user_lower = user_input.lower()
    
    # Name detection
    name_patterns = [
        r"my name is (\w+)",
        r"i'm (\w+)",
        r"i am (\w+)",
        r"call me (\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, user_lower)
        if match:
            name = match.group(1).capitalize()
            if name not in ["a", "an", "the"]:  # Filter common words
                preferences["name"] = name
                break
    
    # Interest detection
    interest_patterns = [
        r"i love (.+?)(?:\.|$|,)",
        r"i like (.+?)(?:\.|$|,)",
        r"i enjoy (.+?)(?:\.|$|,)",
        r"i'm interested in (.+?)(?:\.|$|,)"
    ]
    
    for pattern in interest_patterns:
        match = re.search(pattern, user_lower)
        if match:
            interest = match.group(1).strip()
            if "interests" not in preferences:
                preferences["interests"] = []
            if interest not in preferences["interests"]:
                preferences["interests"].append(interest)
            break
    
    return preferences


def show_preferences(preferences):
    """Display user preferences"""
    print("\n" + "=" * 60)
    print("User Preferences:")
    if not preferences:
        print("  No preferences stored yet")
    else:
        for key, value in preferences.items():
            if isinstance(value, list):
                print(f"  {key.capitalize()}: {', '.join(value)}")
            else:
                print(f"  {key.capitalize()}: {value}")
    print("=" * 60 + "\n")


def main():
    """Main chatbot loop"""
    print("=" * 60)
    print("Personality Chatbot")
    print("=" * 60)
    
    # Choose personality
    personalities = {
        "1": ("pirate", "You are a friendly pirate. Speak like a pirate with 'ahoy', 'matey', 'arr', etc. Be enthusiastic and adventurous."),
        "2": ("philosopher", "You are a thoughtful philosopher. Respond with wisdom, ask deep questions, and ponder the meaning of things."),
        "3": ("comedian", "You are a funny comedian. Make jokes, use humor, and keep things light and entertaining."),
        "4": ("scientist", "You are an enthusiastic scientist. Explain things with curiosity, precision, and wonder about how things work.")
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
    
    # Load memory and preferences
    memory, preferences = load_memory()
    
    if preferences:
        name = preferences.get("name", "friend")
        print(f"Welcome back, {name}! I remember you.\n")
    
    # Create LLM
    llm = ChatOllama(model="llama3.2", temperature=0.8)
    
    # Create conversation chain with personality
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
                print("\nSaving memory...")
                save_memory(memory, preferences)
                print("Goodbye!")
                break
            
            elif user_input == "/clear":
                memory.clear()
                print("\nConversation history cleared!\n")
                continue
            
            elif user_input == "/prefs":
                show_preferences(preferences)
                continue
            
            # Get bot response
            response = conversation.predict(input=user_input)
            print(f"Bot: {response}\n")
            
            # Extract and update preferences
            preferences = extract_preferences(user_input, response, preferences)
            
        except KeyboardInterrupt:
            print("\n\nSaving memory...")
            save_memory(memory, preferences)
            print("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
