# Lesson 7: Agents

## Theory

### What are Agents?

Agents are systems that use LLMs to decide which actions to take. Unlike chains (predefined steps), agents dynamically choose tools based on the input.

**Chain**: A → B → C (fixed path)  
**Agent**: Decides between tools A, B, C, D based on the task

### Agent Loop

```
1. Receive user input
2. Think: What tool should I use?
3. Act: Execute the tool
4. Observe: See the result
5. Think: Do I need another tool, or can I answer?
6. Repeat or finish
```

### ReAct Pattern

**Re**asoning + **Act**ing

The agent alternates between:
- **Thought**: Reasoning about what to do
- **Action**: Choosing and using a tool
- **Observation**: Seeing the tool's output

**Example:**
```
Question: What's 25 * 4 + 10?

Thought: I need to calculate 25 * 4 first
Action: calculator("25 * 4")
Observation: 100

Thought: Now I need to add 10
Action: calculator("100 + 10")
Observation: 110

Thought: I have the final answer
Answer: 110
```

### Agent Types

**1. ReAct Agent**
- Uses reasoning traces
- Good for complex multi-step tasks
- Transparent decision-making

**2. Function Calling Agent**
- Uses native function calling (GPT-4, Claude)
- More reliable tool selection
- Faster execution

**3. Structured Chat Agent**
- For conversational tasks
- Maintains context better

### Creating Agents in LangChain

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Get ReAct prompt
prompt = hub.pull("hwchase17/react")

# Create agent
agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10
)

# Run
result = agent_executor.invoke({"input": "What's 25 * 4 + 10?"})
```

### Agent Components

**1. LLM**: The reasoning engine  
**2. Tools**: Actions the agent can take  
**3. Prompt**: Instructions for the agent  
**4. Memory** (optional): Conversation history  
**5. Executor**: Runs the agent loop

### Agent Prompts

The prompt tells the agent:
- What tools are available
- How to format its thoughts
- When to stop and give an answer

**Key sections:**
- Tool descriptions
- Output format instructions
- Examples (few-shot)

### Error Handling

Agents can fail in several ways:
- **Max iterations**: Stuck in a loop
- **Tool errors**: Tool returns an error
- **Parsing errors**: Can't parse agent output
- **Invalid tool**: Tries to use non-existent tool

**Solutions:**
- Set `max_iterations`
- Use `handle_parsing_errors=True`
- Add error handling in tools
- Improve prompts

### Agent Memory

Add conversation history:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)
```

### Debugging Agents

Enable verbose mode to see:
- Agent's thoughts
- Tool selections
- Tool outputs
- Final answer

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # Show reasoning
)
```

## Demo

See `demo.py` for examples:
1. Basic ReAct agent with calculator
2. Agent with multiple tools
3. Agent with memory
4. Agent error handling
5. Custom agent prompts
6. Debugging agent reasoning

### Quick Example

```python
from langchain_community.chat_models import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub

@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions."""
    return str(eval(expression))

llm = ChatOllama(model="llama3.2")
tools = [calculator]
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({"input": "What's 15 * 7?"})
print(result["output"])
```

## Challenge

Build a **Research Agent** that can:

1. Search Wikipedia for information
2. Perform calculations
3. Write findings to a file
4. Answer complex questions requiring multiple steps

**Requirements:**
- Use at least 3 tools (Wikipedia, calculator, file writer)
- Handle multi-step queries
- Maintain conversation history
- Show reasoning process (verbose mode)
- Handle errors gracefully
- Add a custom tool of your choice

**Example Queries:**
- "How old is the Eiffel Tower? Calculate how many decades that is."
- "Search for Python programming language, then write a summary to python_summary.txt"
- "What's the population of Tokyo? If it grows by 2% annually, what will it be in 10 years?"

**Bonus:**
- Add a web scraping tool
- Implement tool usage statistics
- Add a "plan" tool that outlines steps before executing
- Create a specialized agent for a specific domain

**Starter code in `challenge.py`**

## Resources

- [Agents Documentation](https://python.langchain.com/docs/modules/agents/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Agent Types](https://python.langchain.com/docs/modules/agents/agent_types/)
- [LangChain Hub](https://smith.langchain.com/hub)
