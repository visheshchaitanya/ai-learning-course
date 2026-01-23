# Lesson 9: LangGraph

## Theory

### What is LangGraph?

LangGraph is a library for building stateful, multi-actor applications with LLMs using graph-based workflows.

**Key Differences from Chains/Agents:**
- **Chains**: Linear A → B → C
- **Agents**: LLM decides tools dynamically
- **LangGraph**: Explicit graph with conditional routing, cycles, and state

### Core Concepts

**1. State**: Shared data passed between nodes
```python
from typing import TypedDict

class State(TypedDict):
    messages: list
    count: int
```

**2. Nodes**: Functions that process state
```python
def process_node(state: State) -> State:
    state["count"] += 1
    return state
```

**3. Edges**: Connections between nodes
- **Normal edges**: Always follow
- **Conditional edges**: Route based on logic

**4. Graph**: The workflow structure

### Building a Graph

```python
from langgraph.graph import StateGraph, END

# Define state
class State(TypedDict):
    input: str
    output: str

# Create graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("process", process_func)
workflow.add_node("validate", validate_func)

# Add edges
workflow.add_edge("process", "validate")
workflow.add_edge("validate", END)

# Set entry point
workflow.set_entry_point("process")

# Compile
app = workflow.compile()

# Run
result = app.invoke({"input": "test"})
```

### Conditional Routing

Route based on state:

```python
def router(state: State) -> str:
    if state["score"] > 0.8:
        return "approve"
    else:
        return "reject"

workflow.add_conditional_edges(
    "check",
    router,
    {
        "approve": "approved_node",
        "reject": "rejected_node"
    }
)
```

### Cycles and Loops

LangGraph supports cycles for iterative workflows:

```python
def should_continue(state: State) -> str:
    if state["iterations"] < 3:
        return "continue"
    return "end"

workflow.add_conditional_edges(
    "process",
    should_continue,
    {
        "continue": "process",  # Loop back
        "end": END
    }
)
```

### Checkpointing

Save and resume workflow state:

```python
from langgraph.checkpoint import MemorySaver

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# Run with thread_id
config = {"configurable": {"thread_id": "1"}}
result = app.invoke(input_data, config)

# Resume later
result2 = app.invoke(more_data, config)
```

### Visualization

```python
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```

## Demo

See `demo.py` for examples:
1. Simple linear graph
2. Conditional routing
3. Cyclic graph with max iterations
4. State management
5. Checkpointing
6. Multi-path workflow

### Quick Example

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    text: str
    count: int

def uppercase(state: State) -> State:
    state["text"] = state["text"].upper()
    state["count"] += 1
    return state

def add_exclamation(state: State) -> State:
    state["text"] += "!"
    state["count"] += 1
    return state

workflow = StateGraph(State)
workflow.add_node("uppercase", uppercase)
workflow.add_node("exclaim", add_exclamation)
workflow.add_edge("uppercase", "exclaim")
workflow.add_edge("exclaim", END)
workflow.set_entry_point("uppercase")

app = workflow.compile()
result = app.invoke({"text": "hello", "count": 0})
# {"text": "HELLO!", "count": 2}
```

## Challenge

Build a **Content Moderation Pipeline**:

1. **Detect Language** → Route to appropriate processor
2. **Check Toxicity** → Flag if toxic
3. **Analyze Sentiment** → Determine tone
4. **Route Decision**:
   - Clean + Positive → Auto-approve
   - Toxic → Auto-reject
   - Neutral → Human review
5. **Log Decision** → Record outcome

**Requirements:**
- Use LangGraph with state management
- Implement conditional routing
- Add cycle detection (max 3 checks)
- Save decisions to file
- Visualize the graph
- Handle multiple content types (text, comments)

**Bonus:**
- Add checkpointing for resume
- Implement appeal process (loop back)
- Add confidence scores
- Create dashboard of decisions

**Starter code in `challenge.py`**

## Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/tutorials/)
- [State Management](https://langchain-ai.github.io/langgraph/concepts/low_level/)
- [Checkpointing Guide](https://langchain-ai.github.io/langgraph/how-tos/persistence/)
