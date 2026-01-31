# Lesson 12: Advanced Agent Patterns

## Theory

Advanced patterns for building robust, self-improving agents that can reflect on their outputs, plan complex tasks, and gracefully handle failures.

### Patterns Overview

**1. Self-Reflection**: Agent critiques its own output and iteratively improves
**2. Plan-and-Execute**: Plan first, then execute steps systematically
**3. Tree of Thoughts**: Explore multiple reasoning paths in parallel
**4. Retry with Feedback**: Learn from failures and adapt approach
**5. Fallback Chains**: Graceful degradation when primary methods fail

---

## 1. Self-Reflection Pattern

The agent generates output, critiques it, and revises based on feedback. This creates a feedback loop for continuous improvement.

### Workflow

```
Input → Generate → Critique → Should Revise?
                        ↓           ↓ No
                    Revise ←——— Done
                        ↓
                    (repeat)
```

### Implementation

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ReflectionState(TypedDict):
    input: str
    output: str
    critique: str
    revision_count: int
    quality_score: float

def generate(state: ReflectionState) -> ReflectionState:
    """Generate initial output"""
    llm = ChatOllama(model="llama3.2")
    state["output"] = llm.invoke(state["input"]).content
    state["revision_count"] = 0
    return state

def critique(state: ReflectionState) -> ReflectionState:
    """Critique the output and assign quality score"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Critique this output and rate quality 0-1:
Output: {state['output']}

Provide:
1. Quality score (0-1)
2. Specific improvements needed"""
    
    critique = llm.invoke(prompt).content
    state["critique"] = critique
    
    # Extract score (simplified)
    try:
        score = float([line for line in critique.split('\n') if 'score' in line.lower()][0].split(':')[1].strip())
        state["quality_score"] = score
    except:
        state["quality_score"] = 0.5
    
    return state

def revise(state: ReflectionState) -> ReflectionState:
    """Revise based on critique"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Revise this output based on critique:

Original: {state['output']}
Critique: {state['critique']}

Provide improved version:"""
    
    state["output"] = llm.invoke(prompt).content
    state["revision_count"] += 1
    return state

def should_continue(state: ReflectionState) -> str:
    """Decide whether to continue revising"""
    if state["quality_score"] >= 0.8:
        return "done"
    if state["revision_count"] >= 3:
        return "done"
    return "revise"

# Build graph
workflow = StateGraph(ReflectionState)
workflow.add_node("generate", generate)
workflow.add_node("critique", critique)
workflow.add_node("revise", revise)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "critique")
workflow.add_conditional_edges("critique", should_continue, {
    "revise": "revise",
    "done": END
})
workflow.add_edge("revise", "critique")

app = workflow.compile()
```

### Use Cases
- Code generation with quality checks
- Content writing with editorial review
- Data analysis with validation
- Report generation with fact-checking

---

## 2. Plan-and-Execute Pattern

Break complex tasks into steps, plan the approach, then execute each step systematically. Based on ReWOO (Reasoning WithOut Observation).

### Workflow

```
Task → Plan → Execute Step 1 → Execute Step 2 → ... → Synthesize
         ↓
    [Step 1, Step 2, Step 3, ...]
```

### Implementation

```python
class PlanExecuteState(TypedDict):
    task: str
    plan: list[str]
    results: dict[str, str]
    current_step: int
    final_output: str

def plan(state: PlanExecuteState) -> PlanExecuteState:
    """Create execution plan"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Break this task into 3-5 concrete steps:
Task: {state['task']}

Return numbered list of steps."""
    
    plan_text = llm.invoke(prompt).content
    steps = [line.strip() for line in plan_text.split('\n') if line.strip() and line[0].isdigit()]
    state["plan"] = steps
    state["results"] = {}
    state["current_step"] = 0
    return state

def execute_step(state: PlanExecuteState) -> PlanExecuteState:
    """Execute current step"""
    if state["current_step"] >= len(state["plan"]):
        return state
    
    llm = ChatOllama(model="llama3.2")
    step = state["plan"][state["current_step"]]
    
    # Use previous results as context
    context = "\n".join([f"Step {i}: {result}" for i, result in state["results"].items()])
    
    prompt = f"""Execute this step:
{step}

Previous results:
{context}

Provide result:"""
    
    result = llm.invoke(prompt).content
    state["results"][state["current_step"]] = result
    state["current_step"] += 1
    return state

def should_continue_execution(state: PlanExecuteState) -> str:
    """Check if more steps remain"""
    return "execute" if state["current_step"] < len(state["plan"]) else "synthesize"

def synthesize(state: PlanExecuteState) -> PlanExecuteState:
    """Combine results into final output"""
    llm = ChatOllama(model="llama3.2")
    results_text = "\n".join([f"{i+1}. {result}" for i, result in state["results"].items()])
    
    prompt = f"""Synthesize these results into final answer:
Task: {state['task']}

Results:
{results_text}

Final answer:"""
    
    state["final_output"] = llm.invoke(prompt).content
    return state
```

### Use Cases
- Research tasks requiring multiple sources
- Multi-step calculations or data processing
- Complex decision-making workflows
- Project planning and execution

---

## 3. Retry with Feedback Pattern

When operations fail, capture the error, analyze it, and retry with adjusted approach.

### Implementation

```python
class RetryState(TypedDict):
    task: str
    attempt: int
    max_attempts: int
    last_error: str
    strategy: str
    result: str
    success: bool

def execute_with_retry(state: RetryState) -> RetryState:
    """Execute task with current strategy"""
    try:
        # Attempt execution
        result = execute_task(state["task"], state["strategy"])
        state["result"] = result
        state["success"] = True
    except Exception as e:
        state["last_error"] = str(e)
        state["success"] = False
        state["attempt"] += 1
    return state

def analyze_failure(state: RetryState) -> RetryState:
    """Analyze error and adjust strategy"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""This approach failed:
Strategy: {state['strategy']}
Error: {state['last_error']}

Suggest alternative approach:"""
    
    state["strategy"] = llm.invoke(prompt).content
    return state

def should_retry(state: RetryState) -> str:
    """Decide whether to retry"""
    if state["success"]:
        return "done"
    if state["attempt"] >= state["max_attempts"]:
        return "failed"
    return "retry"
```

### Use Cases
- API calls with transient failures
- Tool execution with fallback strategies
- Data parsing with multiple formats
- Network operations with retry logic

---

## 4. Fallback Chains Pattern

Define multiple strategies in priority order, falling back to simpler/more reliable methods when primary fails.

### Implementation

```python
class FallbackState(TypedDict):
    query: str
    strategies: list[str]
    current_strategy_idx: int
    result: str
    success: bool

def try_strategy(state: FallbackState) -> FallbackState:
    """Try current strategy"""
    strategy = state["strategies"][state["current_strategy_idx"]]
    
    try:
        if strategy == "primary":
            result = complex_but_accurate_method(state["query"])
        elif strategy == "secondary":
            result = simpler_method(state["query"])
        elif strategy == "tertiary":
            result = basic_fallback(state["query"])
        
        state["result"] = result
        state["success"] = True
    except Exception as e:
        state["success"] = False
        state["current_strategy_idx"] += 1
    
    return state

def should_fallback(state: FallbackState) -> str:
    """Check if fallback needed"""
    if state["success"]:
        return "done"
    if state["current_strategy_idx"] >= len(state["strategies"]):
        return "all_failed"
    return "try_next"
```

### Use Cases
- Search with multiple sources (vector → keyword → web)
- Model selection (GPT-4 → GPT-3.5 → local model)
- Data sources (database → cache → default values)
- Tool execution (specialized → general → manual)

---

## 5. Tree of Thoughts Pattern

Explore multiple reasoning paths in parallel, evaluate each, and select the best.

### Implementation

```python
class TreeState(TypedDict):
    problem: str
    thoughts: list[str]
    evaluations: list[float]
    best_thought: str
    final_answer: str

def generate_thoughts(state: TreeState) -> TreeState:
    """Generate multiple reasoning paths"""
    llm = ChatOllama(model="llama3.2")
    thoughts = []
    
    for i in range(3):  # Generate 3 different approaches
        prompt = f"""Approach {i+1} to solve:
{state['problem']}

Provide unique reasoning path:"""
        thought = llm.invoke(prompt).content
        thoughts.append(thought)
    
    state["thoughts"] = thoughts
    return state

def evaluate_thoughts(state: TreeState) -> TreeState:
    """Evaluate each thought"""
    llm = ChatOllama(model="llama3.2")
    evaluations = []
    
    for thought in state["thoughts"]:
        prompt = f"""Rate this reasoning (0-1):
{thought}

Score:"""
        score_text = llm.invoke(prompt).content
        try:
            score = float(score_text.strip())
        except:
            score = 0.5
        evaluations.append(score)
    
    state["evaluations"] = evaluations
    best_idx = evaluations.index(max(evaluations))
    state["best_thought"] = state["thoughts"][best_idx]
    return state
```

### Use Cases
- Complex problem-solving with multiple approaches
- Creative tasks requiring diverse perspectives
- Decision-making with trade-offs
- Optimization problems with multiple solutions

---

## Challenge

Build a **Code Review Agent** that:
1. Generates Python code from a description
2. Critiques the code for quality, style, and correctness
3. Revises the code based on critique
4. Repeats until quality threshold (0.8) or max iterations (3) reached

**Requirements:**
- Use self-reflection pattern with LangGraph
- Track revision count and quality scores
- Provide specific, actionable critiques
- Handle edge cases gracefully

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [ReWOO Paper](https://arxiv.org/abs/2305.18323) - Plan-and-Execute
- [Reflexion Paper](https://arxiv.org/abs/2303.11366) - Self-Reflection
- [Tree of Thoughts Paper](https://arxiv.org/abs/2305.10601)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
