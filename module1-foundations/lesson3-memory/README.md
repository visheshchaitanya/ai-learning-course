# Lesson 3: Memory

## Theory

### Why Memory Matters

LLMs are stateless—they don't remember previous interactions. For chatbots and conversational AI, we need to:
- Track conversation history
- Maintain context across turns
- Remember user preferences
- Manage token limits

### Memory Types in LangChain

#### 1. ConversationBufferMemory
Stores all messages in memory as-is.

**Pros:** Complete context, simple  
**Cons:** Grows unbounded, can exceed token limits

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context({"input": "Hi!"}, {"output": "Hello!"})
```

#### 2. ConversationBufferWindowMemory
Keeps only the last N messages.

**Pros:** Bounded size, recent context  
**Cons:** Loses older context

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=5)  # Last 5 exchanges
```

#### 3. ConversationSummaryMemory
Summarizes conversation history periodically.

**Pros:** Compact, preserves key info  
**Cons:** Loses details, requires LLM calls

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(llm=llm)
```

#### 4. ConversationSummaryBufferMemory
Hybrid: keeps recent messages + summary of older ones.

**Pros:** Best of both worlds  
**Cons:** More complex

### Message History

LangChain uses a standard message format:
```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="What's the weather?"),
    AIMessage(content="I don't have real-time data")
]
```

### Memory with Chains

Integrate memory into LCEL chains:
```python
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough

memory = ConversationBufferMemory(return_messages=True)

chain = (
    RunnablePassthrough.assign(
        history=lambda x: memory.load_memory_variables({})["history"]
    )
    | prompt
    | llm
)
```

### Persistent Memory

Save/load memory from files or databases:
```python
import json

# Save
with open("memory.json", "w") as f:
    json.dump(memory.chat_memory.messages, f)

# Load
with open("memory.json", "r") as f:
    messages = json.load(f)
```

## Demo

See `demo.py` for complete examples:
1. ConversationBufferMemory basics
2. ConversationBufferWindowMemory with limits
3. ConversationSummaryMemory with summarization
4. Memory with LCEL chains
5. Persistent memory (save/load from JSON)
6. Custom memory implementation

### Quick Example

```python
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOllama(model="llama3.2")
memory = ConversationBufferMemory()

conversation = ConversationChain(llm=llm, memory=memory)

# Chat with memory
response1 = conversation.predict(input="My name is Alice")
response2 = conversation.predict(input="What's my name?")
# Will correctly respond with "Alice"
```

## Challenge

Build a **Personality Chatbot** that:

1. Has a defined personality (e.g., pirate, philosopher, comedian)
2. Remembers conversation history (last 10 messages)
3. Remembers user preferences across sessions:
   - User's name
   - Favorite topics
   - Conversation style preference
4. Saves memory to JSON file on exit
5. Loads memory from JSON file on startup

**Requirements:**
- Use ConversationBufferWindowMemory for chat history
- Store user preferences in a separate dict
- Implement save/load functions for persistence
- Add commands: `/clear` (reset history), `/prefs` (show preferences), `/quit` (save and exit)
- Use LCEL for the conversation chain

**Starter code in `challenge.py`**

**Example Interaction:**
```
You: Hi, I'm Bob
Bot: Ahoy there, Bob! Welcome aboard!

You: I love discussing philosophy
Bot: Philosophy, eh? A fine pursuit for a curious mind!

You: /prefs
Preferences:
  Name: Bob
  Interests: philosophy

You: /quit
[Memory saved to memory.json]

# Next session:
[Memory loaded from memory.json]
Bot: Welcome back, Bob! Ready to discuss philosophy?
```

## Resources

- [Memory Guide](https://python.langchain.com/docs/modules/memory/)
- [Message Types](https://python.langchain.com/docs/modules/model_io/chat/message_types/)
- [Conversation Chains](https://python.langchain.com/docs/modules/chains/)
