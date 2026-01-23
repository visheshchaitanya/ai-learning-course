"""
Lesson 3 Demo: Memory in LangChain
"""

from langchain_community.chat_models import ChatOllama
from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationSummaryMemory
)
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import json


def buffer_memory_demo():
    """ConversationBufferMemory - stores all messages"""
    print("=== ConversationBufferMemory ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    memory = ConversationBufferMemory()
    
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
    
    # First exchange
    response1 = conversation.predict(input="My favorite color is blue")
    print(f"User: My favorite color is blue")
    print(f"Bot: {response1}\n")
    
    # Second exchange - bot should remember
    response2 = conversation.predict(input="What's my favorite color?")
    print(f"User: What's my favorite color?")
    print(f"Bot: {response2}\n")
    
    # Show memory contents
    print("Memory contents:")
    print(memory.load_memory_variables({})['history'])
    print()


def window_memory_demo():
    """ConversationBufferWindowMemory - keeps last k messages"""
    print("=== ConversationBufferWindowMemory ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    memory = ConversationBufferWindowMemory(k=3)  # Only last 3 exchanges
    
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
    
    # Multiple exchanges
    exchanges = [
        "My name is Alice",
        "I live in Paris",
        "I love Python programming",
        "What's my name?"  # Should remember (recent)
    ]
    
    for user_input in exchanges:
        response = conversation.predict(input=user_input)
        print(f"User: {user_input}")
        print(f"Bot: {response}\n")
    
    # Now ask about something from beginning (should forget)
    response = conversation.predict(input="Where do I live?")
    print(f"User: Where do I live?")
    print(f"Bot: {response}")
    print("(May not remember Paris - outside the window)\n")


def summary_memory_demo():
    """ConversationSummaryMemory - summarizes history"""
    print("=== ConversationSummaryMemory ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    memory = ConversationSummaryMemory(llm=llm)
    
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
    
    # Have a conversation
    exchanges = [
        "I'm planning a trip to Japan",
        "I want to visit Tokyo and Kyoto",
        "I'm interested in temples and food"
    ]
    
    for user_input in exchanges:
        response = conversation.predict(input=user_input)
        print(f"User: {user_input}")
        print(f"Bot: {response}\n")
    
    # Check the summary
    print("Summary of conversation:")
    print(memory.load_memory_variables({})['history'])
    print()


def memory_with_lcel():
    """Using memory with LCEL chains"""
    print("=== Memory with LCEL ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # Create prompt with message placeholder
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Manual memory management
    from langchain_core.messages import HumanMessage, AIMessage
    
    history = []
    
    chain = prompt | llm | StrOutputParser()
    
    # First message
    response1 = chain.invoke({"history": history, "input": "My name is Bob"})
    print(f"User: My name is Bob")
    print(f"Bot: {response1}\n")
    
    # Add to history
    history.append(HumanMessage(content="My name is Bob"))
    history.append(AIMessage(content=response1))
    
    # Second message
    response2 = chain.invoke({"history": history, "input": "What's my name?"})
    print(f"User: What's my name?")
    print(f"Bot: {response2}\n")


def persistent_memory_demo():
    """Save and load memory from file"""
    print("=== Persistent Memory ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # Create and use memory
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory, verbose=False)
    
    response = conversation.predict(input="Remember that I like pizza")
    print(f"User: Remember that I like pizza")
    print(f"Bot: {response}\n")
    
    # Save memory to file
    memory_file = "demo_memory.json"
    
    # Extract messages
    messages = []
    for msg in memory.chat_memory.messages:
        messages.append({
            "type": msg.type,
            "content": msg.content
        })
    
    with open(memory_file, "w") as f:
        json.dump(messages, f, indent=2)
    
    print(f"Memory saved to {memory_file}\n")
    
    # Load memory from file
    with open(memory_file, "r") as f:
        loaded_messages = json.load(f)
    
    print(f"Memory loaded from {memory_file}")
    print(f"Loaded {len(loaded_messages)} messages\n")
    
    # Create new conversation with loaded memory
    from langchain_core.messages import HumanMessage, AIMessage
    
    new_memory = ConversationBufferMemory()
    for msg in loaded_messages:
        if msg["type"] == "human":
            new_memory.chat_memory.add_message(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            new_memory.chat_memory.add_message(AIMessage(content=msg["content"]))
    
    new_conversation = ConversationChain(llm=llm, memory=new_memory, verbose=False)
    
    response = new_conversation.predict(input="What do I like?")
    print(f"User: What do I like?")
    print(f"Bot: {response}\n")
    
    # Cleanup
    import os
    os.remove(memory_file)


def custom_memory_implementation():
    """Custom memory with user preferences"""
    print("=== Custom Memory Implementation ===\n")
    
    class UserMemory:
        def __init__(self, window_size=5):
            self.messages = []
            self.window_size = window_size
            self.preferences = {}
        
        def add_exchange(self, user_msg: str, bot_msg: str):
            self.messages.append({"user": user_msg, "bot": bot_msg})
            # Keep only last N exchanges
            if len(self.messages) > self.window_size:
                self.messages = self.messages[-self.window_size:]
        
        def set_preference(self, key: str, value: str):
            self.preferences[key] = value
        
        def get_history_text(self) -> str:
            history = []
            for msg in self.messages:
                history.append(f"User: {msg['user']}")
                history.append(f"Assistant: {msg['bot']}")
            return "\n".join(history)
        
        def save(self, filename: str):
            data = {
                "messages": self.messages,
                "preferences": self.preferences
            }
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
        
        def load(self, filename: str):
            with open(filename, "r") as f:
                data = json.load(f)
            self.messages = data.get("messages", [])
            self.preferences = data.get("preferences", {})
    
    # Use custom memory
    memory = UserMemory(window_size=3)
    memory.set_preference("name", "Alice")
    memory.set_preference("topic", "AI")
    
    memory.add_exchange("Hi, I'm Alice", "Hello Alice!")
    memory.add_exchange("I love AI", "That's great!")
    
    print("Preferences:", memory.preferences)
    print("\nHistory:")
    print(memory.get_history_text())
    print()


if __name__ == "__main__":
    print("Memory Demo\n")
    print("=" * 60 + "\n")
    
    try:
        buffer_memory_demo()
        window_memory_demo()
        summary_memory_demo()
        memory_with_lcel()
        persistent_memory_demo()
        custom_memory_implementation()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
