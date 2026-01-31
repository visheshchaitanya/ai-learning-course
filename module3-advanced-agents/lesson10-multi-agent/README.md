# Lesson 10: Multi-Agent Systems

## Theory

Multi-agent systems involve multiple AI agents working together to solve complex problems.

### Patterns

**1. Supervisor Pattern**: One agent coordinates workers
- Central coordinator routes tasks to specialized worker agents
- Supervisor decides which agent should act next based on task requirements
- Workers report results back to supervisor
- Example: PM agent delegates to dev/QA agents

**2. Hierarchical**: Agents in layers
- Multi-level organization with managers and sub-teams
- Each layer has different responsibilities and scope
- Information flows up/down the hierarchy
- Example: CTO → Team Leads → Engineers

**3. Collaborative**: Agents work as peers
- No central authority, agents negotiate and cooperate
- Shared decision-making through consensus or voting
- Agents can directly communicate with any other agent
- Example: Research team where all agents contribute equally

**4. Sequential**: Agents pass work in sequence
- Pipeline/assembly line approach
- Each agent processes and hands off to the next
- Linear workflow with clear handoff points
- Example: Writer → Editor → Publisher

### Implementation

Use LangGraph to orchestrate multiple agents with shared state and communication:

**Shared State**: All agents read/write to a common state graph
- State contains conversation history, task status, artifacts
- Each agent updates specific fields (e.g., dev writes code, QA writes test results)
- State acts as the "memory" and "workspace" for the team

**Communication**: Agents communicate through state updates and routing
- Agents add messages to shared message list
- Supervisor reads state and routes to appropriate next agent
- Agents can leave notes/context for other agents in state
- Conditional edges determine which agent runs next based on state

**Example Flow**:
```python
# State shared across all agents
state = {
    "messages": [...],
    "current_task": "build login",
    "code": "",
    "test_results": "",
    "next_agent": "developer"
}

# PM agent updates state
pm_agent(state) → state["next_agent"] = "developer"

# Developer reads state, writes code
dev_agent(state) → state["code"] = "...", state["next_agent"] = "qa"

# QA reads code from state, tests it
qa_agent(state) → state["test_results"] = "..."
```

### Key Concepts

**Agent Roles and Specialization**
- Each agent has a specific domain of expertise (PM, dev, QA, research, etc.)
- Agents have specialized prompts and tools for their role
- Division of labor makes complex tasks manageable

**Inter-Agent Communication**
- Direct: Agents explicitly message each other via shared state
- Indirect: Agents read artifacts left by previous agents
- Routing: Supervisor or conditional logic determines message flow

**State Sharing**
- Single source of truth accessible to all agents
- Prevents information silos and duplication
- Enables context awareness across the team

**Handoff Protocols**
- Clear rules for when/how agents pass control
- Agents signal completion and next steps
- Supervisor interprets signals and routes accordingly

**Conflict Resolution**
- What happens when agents disagree?
- Supervisor makes final decisions, or
- Voting/consensus mechanisms, or
- Priority/hierarchy rules

## Challenge

Build a **Software Team Simulator** with PM, Developer, and QA agents that collaborate to plan and "implement" a feature.

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Multi-Agent Systems](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
