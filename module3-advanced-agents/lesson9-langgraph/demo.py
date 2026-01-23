"""
Lesson 9 Demo: LangGraph Basics
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator


# Simple state
class SimpleState(TypedDict):
    text: str
    count: int


def simple_linear_graph():
    """Basic linear graph"""
    print("=== Simple Linear Graph ===\n")
    
    def uppercase(state: SimpleState) -> SimpleState:
        state["text"] = state["text"].upper()
        state["count"] += 1
        return state
    
    def add_exclamation(state: SimpleState) -> SimpleState:
        state["text"] += "!"
        state["count"] += 1
        return state
    
    workflow = StateGraph(SimpleState)
    workflow.add_node("uppercase", uppercase)
    workflow.add_node("exclaim", add_exclamation)
    workflow.add_edge("uppercase", "exclaim")
    workflow.add_edge("exclaim", END)
    workflow.set_entry_point("uppercase")
    
    app = workflow.compile()
    result = app.invoke({"text": "hello world", "count": 0})
    
    print(f"Result: {result}")
    print(f"Text: {result['text']}, Steps: {result['count']}\n")


def conditional_routing_graph():
    """Graph with conditional edges"""
    print("=== Conditional Routing ===\n")
    
    class RouterState(TypedDict):
        number: int
        result: str
    
    def check_number(state: RouterState) -> RouterState:
        return state
    
    def positive_path(state: RouterState) -> RouterState:
        state["result"] = f"{state['number']} is positive"
        return state
    
    def negative_path(state: RouterState) -> RouterState:
        state["result"] = f"{state['number']} is negative"
        return state
    
    def zero_path(state: RouterState) -> RouterState:
        state["result"] = "Number is zero"
        return state
    
    def router(state: RouterState) -> str:
        if state["number"] > 0:
            return "positive"
        elif state["number"] < 0:
            return "negative"
        else:
            return "zero"
    
    workflow = StateGraph(RouterState)
    workflow.add_node("check", check_number)
    workflow.add_node("positive", positive_path)
    workflow.add_node("negative", negative_path)
    workflow.add_node("zero", zero_path)
    
    workflow.set_entry_point("check")
    workflow.add_conditional_edges(
        "check",
        router,
        {
            "positive": "positive",
            "negative": "negative",
            "zero": "zero"
        }
    )
    workflow.add_edge("positive", END)
    workflow.add_edge("negative", END)
    workflow.add_edge("zero", END)
    
    app = workflow.compile()
    
    for num in [5, -3, 0]:
        result = app.invoke({"number": num, "result": ""})
        print(f"Input: {num} → {result['result']}")
    
    print()


def cyclic_graph():
    """Graph with cycles (loops)"""
    print("=== Cyclic Graph ===\n")
    
    class LoopState(TypedDict):
        value: int
        iterations: int
        max_iterations: int
    
    def increment(state: LoopState) -> LoopState:
        state["value"] += 1
        state["iterations"] += 1
        print(f"  Iteration {state['iterations']}: value = {state['value']}")
        return state
    
    def should_continue(state: LoopState) -> str:
        if state["iterations"] < state["max_iterations"]:
            return "continue"
        return "end"
    
    workflow = StateGraph(LoopState)
    workflow.add_node("increment", increment)
    workflow.set_entry_point("increment")
    workflow.add_conditional_edges(
        "increment",
        should_continue,
        {
            "continue": "increment",
            "end": END
        }
    )
    
    app = workflow.compile()
    result = app.invoke({"value": 0, "iterations": 0, "max_iterations": 5})
    
    print(f"\nFinal value: {result['value']}\n")


def state_accumulation():
    """Accumulate state across nodes"""
    print("=== State Accumulation ===\n")
    
    class AccumulateState(TypedDict):
        messages: Annotated[list, operator.add]
    
    def node1(state: AccumulateState) -> AccumulateState:
        return {"messages": ["Message from node1"]}
    
    def node2(state: AccumulateState) -> AccumulateState:
        return {"messages": ["Message from node2"]}
    
    def node3(state: AccumulateState) -> AccumulateState:
        return {"messages": ["Message from node3"]}
    
    workflow = StateGraph(AccumulateState)
    workflow.add_node("n1", node1)
    workflow.add_node("n2", node2)
    workflow.add_node("n3", node3)
    workflow.set_entry_point("n1")
    workflow.add_edge("n1", "n2")
    workflow.add_edge("n2", "n3")
    workflow.add_edge("n3", END)
    
    app = workflow.compile()
    result = app.invoke({"messages": []})
    
    print("Accumulated messages:")
    for msg in result["messages"]:
        print(f"  - {msg}")
    print()


if __name__ == "__main__":
    print("LangGraph Demo\n")
    print("=" * 60 + "\n")
    
    try:
        simple_linear_graph()
        conditional_routing_graph()
        cyclic_graph()
        state_accumulation()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure langgraph is installed:")
        print("  pip install langgraph")
