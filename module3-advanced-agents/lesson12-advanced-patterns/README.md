# Lesson 12: Advanced Agent Patterns

## Theory

Advanced patterns for building robust, self-improving agents.

### Patterns

**1. Self-Reflection**: Agent critiques its own output
**2. Plan-and-Execute**: Plan first, then execute steps
**3. Tree of Thoughts**: Explore multiple reasoning paths
**4. Retry with Feedback**: Learn from failures
**5. Fallback Chains**: Graceful degradation

### Self-Reflection

```python
def generate(state):
    state["output"] = llm.invoke(state["input"])
    return state

def critique(state):
    critique = llm.invoke(f"Critique this: {state['output']}")
    state["critique"] = critique
    return state

def should_revise(state):
    return "revise" if "improve" in state["critique"] else "done"
```

## Challenge

Build a **Code Review Agent** that writes code, critiques it, revises it, and repeats until quality threshold is met.

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [ReWOO Paper](https://arxiv.org/abs/2305.18323)
- [Reflexion Paper](https://arxiv.org/abs/2303.11366)
