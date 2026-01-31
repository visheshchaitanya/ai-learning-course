"""
Lesson 12 Demo: Advanced Agent Patterns

Demonstrates self-reflection, plan-and-execute, retry with feedback, and fallback patterns.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_community.chat_models import ChatOllama
import operator


# ============================================================================
# Demo 1: Self-Reflection Pattern
# ============================================================================

class ReflectionState(TypedDict):
    input: str
    output: str
    critique: str
    revision_count: int
    quality_score: float


def generate_content(state: ReflectionState) -> ReflectionState:
    """Generate initial content"""
    print(f"\n🎯 Generating content for: {state['input']}")
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    state["output"] = llm.invoke(state["input"]).content
    state["revision_count"] = 0
    state["quality_score"] = 0.0
    print(f"✅ Generated: {state['output'][:100]}...")
    return state


def critique_content(state: ReflectionState) -> ReflectionState:
    """Critique the output and assign quality score"""
    print(f"\n🔍 Critiquing output (revision #{state['revision_count']})...")
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    prompt = f"""Critique this output and rate its quality from 0.0 to 1.0:

Output: {state['output']}

Provide:
1. Quality Score: [0.0-1.0]
2. Strengths: [what's good]
3. Improvements: [what needs work]

Be concise."""
    
    critique = llm.invoke(prompt).content
    state["critique"] = critique
    
    # Extract score
    try:
        for line in critique.split('\n'):
            if 'score' in line.lower() or 'quality' in line.lower():
                # Look for number between 0 and 1
                import re
                numbers = re.findall(r'0\.\d+|1\.0|0|1', line)
                if numbers:
                    state["quality_score"] = float(numbers[0])
                    break
    except:
        state["quality_score"] = 0.5
    
    print(f"📊 Quality Score: {state['quality_score']}")
    print(f"💬 Critique: {state['critique'][:150]}...")
    return state


def revise_content(state: ReflectionState) -> ReflectionState:
    """Revise based on critique"""
    print(f"\n✏️  Revising based on feedback...")
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    prompt = f"""Revise this output based on the critique:

Original Output: {state['output']}

Critique: {state['critique']}

Provide improved version:"""
    
    state["output"] = llm.invoke(prompt).content
    state["revision_count"] += 1
    print(f"✅ Revision #{state['revision_count']} complete")
    return state


def should_continue_reflection(state: ReflectionState) -> str:
    """Decide whether to continue revising"""
    if state["quality_score"] >= 0.8:
        print(f"\n✅ Quality threshold met ({state['quality_score']} >= 0.8)")
        return "done"
    if state["revision_count"] >= 3:
        print(f"\n⏹️  Max revisions reached ({state['revision_count']})")
        return "done"
    return "revise"


def demo_self_reflection():
    """Demo 1: Self-reflection agent"""
    print("\n" + "=" * 70)
    print("Demo 1: Self-Reflection Pattern")
    print("=" * 70)
    
    workflow = StateGraph(ReflectionState)
    
    workflow.add_node("generate", generate_content)
    workflow.add_node("critique", critique_content)
    workflow.add_node("revise", revise_content)
    
    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "critique")
    workflow.add_conditional_edges(
        "critique",
        should_continue_reflection,
        {
            "revise": "revise",
            "done": END
        }
    )
    workflow.add_edge("revise", "critique")
    
    app = workflow.compile()
    
    # Test
    result = app.invoke({
        "input": "Write a short explanation of quantum computing for beginners",
        "output": "",
        "critique": "",
        "revision_count": 0,
        "quality_score": 0.0
    })
    
    print("\n" + "=" * 70)
    print("Final Output:")
    print("=" * 70)
    print(result["output"])
    print(f"\nRevisions: {result['revision_count']}, Final Score: {result['quality_score']}")


# ============================================================================
# Demo 2: Plan-and-Execute Pattern
# ============================================================================

class PlanExecuteState(TypedDict):
    task: str
    plan: list[str]
    results: Annotated[list[str], operator.add]
    current_step: int
    final_output: str


def create_plan(state: PlanExecuteState) -> PlanExecuteState:
    """Create execution plan"""
    print(f"\n📋 Planning task: {state['task']}")
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    prompt = f"""Break this task into 3-4 concrete, actionable steps:

Task: {state['task']}

Return ONLY a numbered list of steps, nothing else."""
    
    plan_text = llm.invoke(prompt).content
    
    # Extract steps
    steps = []
    for line in plan_text.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove numbering
            step = line.lstrip('0123456789.-) ').strip()
            if step:
                steps.append(step)
    
    state["plan"] = steps
    state["current_step"] = 0
    
    print(f"✅ Created plan with {len(steps)} steps:")
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    
    return state


def execute_step(state: PlanExecuteState) -> PlanExecuteState:
    """Execute current step"""
    step_num = state["current_step"]
    step = state["plan"][step_num]
    
    print(f"\n⚙️  Executing Step {step_num + 1}: {step}")
    
    llm = ChatOllama(model="llama3.2", temperature=0.5)
    
    # Build context from previous results
    context = ""
    if state["results"]:
        context = "\n\nPrevious results:\n" + "\n".join([
            f"Step {i+1}: {result}" for i, result in enumerate(state["results"])
        ])
    
    prompt = f"""Execute this step:

Step: {step}
{context}

Provide the result:"""
    
    result = llm.invoke(prompt).content
    state["results"] = [result]  # Annotated with operator.add
    state["current_step"] += 1
    
    print(f"✅ Result: {result[:100]}...")
    
    return state


def should_continue_execution(state: PlanExecuteState) -> str:
    """Check if more steps remain"""
    if state["current_step"] < len(state["plan"]):
        return "execute"
    return "synthesize"


def synthesize_results(state: PlanExecuteState) -> PlanExecuteState:
    """Combine results into final output"""
    print(f"\n🔄 Synthesizing results...")
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    results_text = "\n".join([
        f"Step {i+1}: {result}" for i, result in enumerate(state["results"])
    ])
    
    prompt = f"""Synthesize these step results into a final answer:

Original Task: {state['task']}

Step Results:
{results_text}

Final Answer:"""
    
    state["final_output"] = llm.invoke(prompt).content
    print(f"✅ Synthesis complete")
    
    return state


def demo_plan_and_execute():
    """Demo 2: Plan-and-execute pattern"""
    print("\n" + "=" * 70)
    print("Demo 2: Plan-and-Execute Pattern")
    print("=" * 70)
    
    workflow = StateGraph(PlanExecuteState)
    
    workflow.add_node("plan", create_plan)
    workflow.add_node("execute", execute_step)
    workflow.add_node("synthesize", synthesize_results)
    
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "execute")
    workflow.add_conditional_edges(
        "execute",
        should_continue_execution,
        {
            "execute": "execute",
            "synthesize": "synthesize"
        }
    )
    workflow.add_edge("synthesize", END)
    
    app = workflow.compile()
    
    # Test
    result = app.invoke({
        "task": "Research the history of artificial intelligence and identify 3 key milestones",
        "plan": [],
        "results": [],
        "current_step": 0,
        "final_output": ""
    })
    
    print("\n" + "=" * 70)
    print("Final Output:")
    print("=" * 70)
    print(result["final_output"])


# ============================================================================
# Demo 3: Retry with Feedback Pattern
# ============================================================================

class RetryState(TypedDict):
    task: str
    attempt: int
    max_attempts: int
    last_error: str
    approach: str
    result: str
    success: bool


def execute_with_strategy(state: RetryState) -> RetryState:
    """Execute task with current approach"""
    print(f"\n🎯 Attempt {state['attempt'] + 1}/{state['max_attempts']}")
    print(f"📝 Approach: {state['approach']}")
    
    llm = ChatOllama(model="llama3.2", temperature=0.5)
    
    prompt = f"""Execute this task using the specified approach:

Task: {state['task']}
Approach: {state['approach']}

Provide result:"""
    
    try:
        result = llm.invoke(prompt).content
        
        # Simulate validation (check if result seems reasonable)
        if len(result) < 20:
            raise ValueError("Result too short, likely incomplete")
        
        state["result"] = result
        state["success"] = True
        print(f"✅ Success! Result: {result[:100]}...")
        
    except Exception as e:
        state["last_error"] = str(e)
        state["success"] = False
        state["attempt"] += 1
        print(f"❌ Failed: {state['last_error']}")
    
    return state


def adjust_approach(state: RetryState) -> RetryState:
    """Analyze failure and adjust approach"""
    print(f"\n🔄 Analyzing failure and adjusting approach...")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    prompt = f"""This approach failed:

Task: {state['task']}
Previous Approach: {state['approach']}
Error: {state['last_error']}

Suggest a different, simpler approach:"""
    
    state["approach"] = llm.invoke(prompt).content
    print(f"💡 New approach: {state['approach'][:100]}...")
    
    return state


def should_retry(state: RetryState) -> str:
    """Decide whether to retry"""
    if state["success"]:
        return "done"
    if state["attempt"] >= state["max_attempts"]:
        print(f"\n⏹️  Max attempts reached")
        return "failed"
    return "retry"


def demo_retry_with_feedback():
    """Demo 3: Retry with feedback"""
    print("\n" + "=" * 70)
    print("Demo 3: Retry with Feedback Pattern")
    print("=" * 70)
    
    workflow = StateGraph(RetryState)
    
    workflow.add_node("execute", execute_with_strategy)
    workflow.add_node("adjust", adjust_approach)
    
    workflow.set_entry_point("execute")
    workflow.add_conditional_edges(
        "execute",
        should_retry,
        {
            "retry": "adjust",
            "done": END,
            "failed": END
        }
    )
    workflow.add_edge("adjust", "execute")
    
    app = workflow.compile()
    
    # Test
    result = app.invoke({
        "task": "Explain the concept of recursion with a simple example",
        "attempt": 0,
        "max_attempts": 3,
        "last_error": "",
        "approach": "Use technical jargon and complex examples",
        "result": "",
        "success": False
    })
    
    if result["success"]:
        print("\n" + "=" * 70)
        print("Final Result:")
        print("=" * 70)
        print(result["result"])
    else:
        print("\n❌ All attempts failed")


# ============================================================================
# Demo 4: Fallback Chain Pattern
# ============================================================================

def demo_fallback_chain():
    """Demo 4: Fallback chain with multiple strategies"""
    print("\n" + "=" * 70)
    print("Demo 4: Fallback Chain Pattern")
    print("=" * 70)
    
    query = "What is the capital of France?"
    strategies = [
        ("Detailed Analysis", "Provide comprehensive historical context and detailed answer"),
        ("Standard Response", "Provide clear, direct answer with brief context"),
        ("Simple Answer", "Provide just the essential answer")
    ]
    
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    for i, (name, approach) in enumerate(strategies, 1):
        print(f"\n🎯 Strategy {i}: {name}")
        print(f"📝 Approach: {approach}")
        
        try:
            prompt = f"""{approach}

Question: {query}

Answer:"""
            
            result = llm.invoke(prompt).content
            
            # Simulate validation
            if len(result) > 10:  # Basic check
                print(f"✅ Success with {name}")
                print(f"📄 Result: {result}")
                break
            else:
                raise ValueError("Response too short")
                
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            if i < len(strategies):
                print(f"⤵️  Falling back to next strategy...")
            else:
                print(f"⏹️  All strategies exhausted")


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("Advanced Agent Patterns Demo")
    print("=" * 70)
    
    try:
        demo_self_reflection()
        demo_plan_and_execute()
        demo_retry_with_feedback()
        demo_fallback_chain()
        
        print("\n" + "=" * 70)
        print("All demos completed!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("1. Self-Reflection: Iterative improvement through critique")
        print("2. Plan-and-Execute: Break complex tasks into steps")
        print("3. Retry with Feedback: Learn from failures and adapt")
        print("4. Fallback Chains: Graceful degradation with multiple strategies")
        print("\nNow try the challenge.py!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")


if __name__ == "__main__":
    main()
