"""
Lesson 10 Demo: Multi-Agent Systems

This demo shows how multiple agents can collaborate using LangGraph.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.chat_models import ChatOllama


# Demo 1: Basic Sequential Multi-Agent System
class SimpleState(TypedDict):
    task: str
    research: str
    draft: str
    final: str


def researcher_agent(state: SimpleState) -> SimpleState:
    """Agent that researches a topic"""
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    prompt = f"Research this topic briefly (2-3 sentences): {state['task']}"
    state["research"] = llm.invoke(prompt).content
    print(f"\n🔍 Researcher: Completed research")
    return state


def writer_agent(state: SimpleState) -> SimpleState:
    """Agent that writes based on research"""
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    prompt = f"Write a short article based on this research: {state['research']}"
    state["draft"] = llm.invoke(prompt).content
    print(f"\n✍️ Writer: Completed draft")
    return state


def editor_agent(state: SimpleState) -> SimpleState:
    """Agent that edits the draft"""
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    prompt = f"Edit and improve this draft: {state['draft']}"
    state["final"] = llm.invoke(prompt).content
    print(f"\n📝 Editor: Completed editing")
    return state


def demo_sequential():
    """Demo 1: Sequential pipeline of agents"""
    print("\n" + "=" * 60)
    print("Demo 1: Sequential Multi-Agent Pipeline")
    print("Pattern: Researcher → Writer → Editor")
    print("=" * 60)
    
    workflow = StateGraph(SimpleState)
    
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("editor", editor_agent)
    
    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "editor")
    workflow.add_edge("editor", END)
    
    app = workflow.compile()
    
    result = app.invoke({
        "task": "Benefits of multi-agent systems in AI",
        "research": "",
        "draft": "",
        "final": ""
    })
    
    print("\n📄 Final Article:")
    print(result["final"])


# Demo 2: Supervisor Pattern
class SupervisorState(TypedDict):
    query: str
    next_agent: str
    math_result: str
    code_result: str
    iterations: int


def supervisor(state: SupervisorState) -> SupervisorState:
    """Supervisor decides which agent to call"""
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    if state["iterations"] >= 2:
        state["next_agent"] = "END"
        return state
    
    prompt = f"""Given this query: "{state['query']}"
    
Which agent should handle it? Reply with ONLY one word:
- MATH (for calculations)
- CODE (for programming)

Agent:"""
    
    response = llm.invoke(prompt).content.strip().upper()
    
    if "MATH" in response:
        state["next_agent"] = "math"
    elif "CODE" in response:
        state["next_agent"] = "code"
    else:
        state["next_agent"] = "END"
    
    print(f"\n🎯 Supervisor: Routing to {state['next_agent']} agent")
    return state


def math_agent(state: SupervisorState) -> SupervisorState:
    """Agent specialized in math"""
    llm = ChatOllama(model="llama3.2", temperature=0)
    prompt = f"Solve this math problem: {state['query']}"
    state["math_result"] = llm.invoke(prompt).content
    state["iterations"] += 1
    print(f"\n🔢 Math Agent: Solved problem")
    return state


def code_agent(state: SupervisorState) -> SupervisorState:
    """Agent specialized in coding"""
    llm = ChatOllama(model="llama3.2", temperature=0)
    prompt = f"Write code for: {state['query']}"
    state["code_result"] = llm.invoke(prompt).content
    state["iterations"] += 1
    print(f"\n💻 Code Agent: Generated code")
    return state


def route_after_supervisor(state: SupervisorState) -> str:
    """Router function after supervisor"""
    if state["next_agent"] == "END" or state["iterations"] >= 2:
        return "end"
    return state["next_agent"]


def demo_supervisor():
    """Demo 2: Supervisor pattern with specialized workers"""
    print("\n" + "=" * 60)
    print("Demo 2: Supervisor Pattern")
    print("Pattern: Supervisor → Math/Code Worker Agents")
    print("=" * 60)
    
    workflow = StateGraph(SupervisorState)
    
    workflow.add_node("supervisor", supervisor)
    workflow.add_node("math", math_agent)
    workflow.add_node("code", code_agent)
    
    workflow.set_entry_point("supervisor")
    
    workflow.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "math": "math",
            "code": "code",
            "end": END
        }
    )
    
    workflow.add_edge("math", END)
    workflow.add_edge("code", END)
    
    app = workflow.compile()
    
    # Test with a math query
    print("\n📋 Query: Calculate 15% of 240")
    result = app.invoke({
        "query": "Calculate 15% of 240",
        "next_agent": "",
        "math_result": "",
        "code_result": "",
        "iterations": 0
    })
    
    if result["math_result"]:
        print(f"\n✅ Math Result: {result['math_result']}")
    if result["code_result"]:
        print(f"\n✅ Code Result: {result['code_result']}")


def main():
    print("\n" + "=" * 60)
    print("Multi-Agent Systems Demo")
    print("=" * 60)
    
    # Run both demos
    demo_sequential()
    demo_supervisor()
    
    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("- Sequential: Agents pass work in a pipeline")
    print("- Supervisor: Central agent routes to specialized workers")
    print("- State: Shared memory for agent communication")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running: ollama serve")
        print("And llama3.2 is installed: ollama pull llama3.2")
