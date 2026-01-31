"""
Lesson 11 Demo: Human-in-the-Loop

This demo shows how to pause agent execution for human approval.
"""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict
from langchain_community.chat_models import ChatOllama
import uuid


# Demo 1: Simple Approval Workflow
class ApprovalState(TypedDict):
    request: str
    analysis: str
    approved: bool
    response: str


def analyze_request(state: ApprovalState) -> ApprovalState:
    """Analyze the request before approval"""
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    prompt = f"Analyze this request and identify any risks: {state['request']}"
    state["analysis"] = llm.invoke(prompt).content
    print(f"\n🔍 Analysis: {state['analysis']}")
    return state


def human_approval(state: ApprovalState) -> ApprovalState:
    """This node pauses for human input"""
    print("\n⏸️  Paused for human approval...")
    print(f"Request: {state['request']}")
    print(f"Analysis: {state['analysis']}")
    # The workflow will pause here when interrupt_before=["human_approval"]
    return state


def execute_action(state: ApprovalState) -> ApprovalState:
    """Execute the action after approval"""
    if state.get("approved", False):
        llm = ChatOllama(model="llama3.2", temperature=0.7)
        prompt = f"Execute this approved request: {state['request']}"
        state["response"] = llm.invoke(prompt).content
        print(f"\n✅ Executed: {state['response']}")
    else:
        state["response"] = "Request denied"
        print(f"\n❌ Denied: {state['response']}")
    return state


def demo_simple_approval():
    """Demo 1: Basic approval workflow with interrupt"""
    print("\n" + "=" * 60)
    print("Demo 1: Simple Approval Workflow")
    print("=" * 60)
    
    workflow = StateGraph(ApprovalState)
    
    workflow.add_node("analyze", analyze_request)
    workflow.add_node("human_approval", human_approval)
    workflow.add_node("execute", execute_action)
    
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "human_approval")
    workflow.add_edge("human_approval", "execute")
    workflow.add_edge("execute", END)
    
    # Compile with checkpointer and interrupt
    memory = MemorySaver()
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["human_approval"]
    )
    
    # Create a thread for this conversation
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Step 1: Run until interrupt
    print("\n📤 Submitting request...")
    initial_state = {
        "request": "Delete all user data older than 90 days",
        "analysis": "",
        "approved": False,
        "response": ""
    }
    
    result = app.invoke(initial_state, config)
    print(f"\n⏸️  Workflow paused. Current state: {result}")
    
    # Step 2: Resume with approval
    print("\n" + "-" * 60)
    print("Human provides approval...")
    print("-" * 60)
    
    # Update state with approval
    result["approved"] = True
    
    # Resume execution
    final_result = app.invoke(None, config)
    print(f"\n✅ Final result: {final_result['response']}")


# Demo 2: Multiple Approval Points
class MultiApprovalState(TypedDict):
    task: str
    step: str
    step1_approved: bool
    step2_approved: bool
    result: str


def step1_check(state: MultiApprovalState) -> MultiApprovalState:
    """First checkpoint"""
    state["step"] = "step1"
    print(f"\n📋 Step 1: Preparing to {state['task']}")
    return state


def step2_check(state: MultiApprovalState) -> MultiApprovalState:
    """Second checkpoint"""
    state["step"] = "step2"
    print(f"\n📋 Step 2: Executing {state['task']}")
    return state


def final_execution(state: MultiApprovalState) -> MultiApprovalState:
    """Final execution after all approvals"""
    state["result"] = f"Completed: {state['task']}"
    print(f"\n✅ {state['result']}")
    return state


def demo_multiple_approvals():
    """Demo 2: Multiple approval points in workflow"""
    print("\n" + "=" * 60)
    print("Demo 2: Multiple Approval Points")
    print("=" * 60)
    
    workflow = StateGraph(MultiApprovalState)
    
    workflow.add_node("step1", step1_check)
    workflow.add_node("step2", step2_check)
    workflow.add_node("execute", final_execution)
    
    workflow.set_entry_point("step1")
    workflow.add_edge("step1", "step2")
    workflow.add_edge("step2", "execute")
    workflow.add_edge("execute", END)
    
    # Interrupt at both checkpoints
    memory = MemorySaver()
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["step1", "step2"]
    )
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial invocation
    print("\n📤 Starting multi-step process...")
    state = {
        "task": "Deploy to production",
        "step": "",
        "step1_approved": False,
        "step2_approved": False,
        "result": ""
    }
    
    # First pause
    result = app.invoke(state, config)
    print(f"\n⏸️  Paused at: {result['step']}")
    
    # Approve step 1
    result["step1_approved"] = True
    result = app.invoke(None, config)
    print(f"\n⏸️  Paused at: {result['step']}")
    
    # Approve step 2
    result["step2_approved"] = True
    final = app.invoke(None, config)
    print(f"\n✅ Final: {final['result']}")


def main():
    print("\n" + "=" * 60)
    print("Human-in-the-Loop Demo")
    print("=" * 60)
    
    demo_simple_approval()
    demo_multiple_approvals()
    
    print("\n" + "=" * 60)
    print("Key Concepts:")
    print("- interrupt_before: Pause workflow at specific nodes")
    print("- MemorySaver: Checkpoint state for resume")
    print("- thread_id: Track conversation/workflow instance")
    print("- State updates: Modify state during pause")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running: ollama serve")
        print("And llama3.2 is installed: ollama pull llama3.2")
