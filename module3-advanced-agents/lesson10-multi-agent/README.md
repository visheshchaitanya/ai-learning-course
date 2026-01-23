# Lesson 10: Multi-Agent Systems

## Theory

Multi-agent systems involve multiple AI agents working together to solve complex problems.

### Patterns

**1. Supervisor Pattern**: One agent coordinates workers
**2. Hierarchical**: Agents in layers
**3. Collaborative**: Agents work as peers
**4. Sequential**: Agents pass work in sequence

### Implementation

Use LangGraph to orchestrate multiple agents with shared state and communication.

### Key Concepts
- Agent roles and specialization
- Inter-agent communication
- State sharing
- Handoff protocols
- Conflict resolution

## Challenge

Build a **Software Team Simulator** with PM, Developer, and QA agents that collaborate to plan and "implement" a feature.

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Multi-Agent Systems](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
