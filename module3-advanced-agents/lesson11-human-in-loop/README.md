# Lesson 11: Human-in-the-Loop

## Theory

Human-in-the-loop systems pause execution to get human input, approval, or feedback.

### Use Cases
- Approval workflows
- Sensitive operations
- Error correction
- Quality assurance
- Training and feedback

### Implementation with LangGraph

Use interrupts and checkpointing to pause and resume workflows.

```python
from langgraph.checkpoint import MemorySaver

workflow.add_node("human_approval", approval_node)
app = workflow.compile(checkpointer=MemorySaver(), interrupt_before=["human_approval"])
```

## Challenge

Build an **Expense Approval System** where agents categorize expenses, flag suspicious ones, and require human approval for high amounts.

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Human-in-the-Loop Guide](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/)
