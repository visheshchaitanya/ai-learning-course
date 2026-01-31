"""
Lesson 11 Challenge: Expense Approval System

Build a system that:
1. Categorizes expenses (travel, meals, supplies, etc.)
2. Flags suspicious expenses (duplicates, unusual amounts)
3. Requires human approval for expenses above $1000
4. Auto-approves expenses below $1000 that pass validation

Your implementation should:
- Use LangGraph with StateGraph
- Implement interrupt_before for approval node
- Use MemorySaver for checkpointing
- Handle both auto-approval and manual approval flows
"""

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, List
from langchain_community.chat_models import ChatOllama
import uuid
from langchain_core.prompts import ChatPromptTemplate
import json


class ExpenseState(TypedDict):
    expense_id: str
    amount: float
    description: str
    category: str
    is_suspicious: bool
    requires_approval: bool
    approved: bool
    rejection_reason: str
    final_status: str


def categorize_expense(state: ExpenseState) -> ExpenseState:
    """
    TODO: Use LLM to categorize the expense based on description
    Categories: travel, meals, supplies, software, other
    Update state["category"]
    """
    # Your code here
    llm = ChatOllama(model="llama3.2", temperature=0)
    prompt = f"""Categorize this expense: {state['description']}
    
Categories: travel, meals, supplies, software, other

Return ONLY the category name, nothing else."""
    
    result = llm.invoke(prompt)
    state["category"] = result.content.strip().lower()
    return state


def validate_expense(state: ExpenseState) -> ExpenseState:
    """
    TODO: Check for suspicious patterns:
    - Amount over $10,000 (flag as suspicious)
    - Unusual descriptions (use LLM to detect)
    - Round numbers over $5000 (might be estimates)
    
    Update state["is_suspicious"] and state["requires_approval"]
    Rules:
    - Amount > $1000 OR is_suspicious = True → requires_approval = True
    - Otherwise → auto-approve
    """
    # Your code here
    amount = state["amount"]
    description = state["description"]
    
    # Check basic rules
    is_suspicious = False
    
    if amount > 10000:
        is_suspicious = True
    elif amount > 5000 and amount % 1000 == 0:
        is_suspicious = True
    else:
        # Use LLM to check for unusual descriptions
        llm = ChatOllama(model="llama3.2", temperature=0)
        prompt = f"""Is this expense description suspicious or unusual? Answer only 'yes' or 'no'.
        
Description: {description}
Amount: ${amount}"""
        
        result = llm.invoke(prompt)
        if "yes" in result.content.lower():
            is_suspicious = True
    
    state["is_suspicious"] = is_suspicious
    state["requires_approval"] = amount > 1000 or is_suspicious
    return state

def human_approval_node(state: ExpenseState) -> ExpenseState:
    """
    TODO: This node should pause for human input
    Print expense details for human review
    The workflow will pause here when interrupt_before=["human_approval"]
    """
    """Display info, node does nothing - just a marker for interrupt"""
    print(f"\n{'='*60}")
    print(f"APPROVAL REQUIRED")
    print(f"{'='*60}")
    print(f"Expense ID: {state['expense_id']}")
    print(f"Amount: ${state['amount']:.2f}")
    print(f"Description: {state['description']}")
    print(f"Category: {state['category']}")
    print(f"Suspicious: {state['is_suspicious']}")
    print(f"{'='*60}")
    return state


def finalize_expense(state: ExpenseState) -> ExpenseState:
    """
    TODO: Set final status based on approval
    Update state["final_status"]:
    - "APPROVED" if approved
    - "REJECTED" if not approved
    - Include rejection reason if rejected
    """
    # Your code here
    if state["approved"]:
        state["final_status"] = "APPROVED"
    else:
        state["final_status"] = "REJECTED"
    return state


def route_after_validation(state: ExpenseState) -> str:
    """
    TODO: Route to approval or auto-approve based on state
    Return:
    - "human_approval" if requires_approval is True
    - "finalize" if auto-approved
    """
    # Your code here
    if state["requires_approval"]:
        return "human_approval"
    else:
        return "finalize"


def build_expense_workflow():
    """
    TODO: Build the complete workflow
    
    Nodes:
    1. categorize - Categorize the expense
    2. validate - Check if approval needed
    3. human_approval - Pause for human input
    4. finalize - Set final status
    
    Edges:
    - categorize → validate
    - validate → (conditional) → human_approval OR finalize
    - human_approval → finalize
    - finalize → END
    
    Return compiled app with:
    - checkpointer=MemorySaver()
    - interrupt_before=["human_approval"]
    """
    # Your code here
    workflow = StateGraph(ExpenseState)
    workflow.add_node("categorize", categorize_expense)
    workflow.add_node("validate", validate_expense)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("finalize", finalize_expense)
    
    workflow.set_entry_point("categorize")
    workflow.add_edge("categorize", "validate")
    workflow.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "human_approval": "human_approval",
            "finalize": "finalize"
        }
    )
    workflow.add_edge("human_approval", "finalize")
    workflow.add_edge("finalize", END)
    
    # Key: checkpointer + interrupt_before
    return workflow.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["human_approval"]
    )
    


def test_expense_system():
    """Test the expense approval system"""
    
    app = build_expense_workflow()
    print("\n" + "=" * 60)
    print("Test 2: High Amount Expense (Requires Approval)")
    print("=" * 60)
    
    thread2 = str(uuid.uuid4())
    config2 = {"configurable": {"thread_id": thread2}}
    
    expense2 = {
        "expense_id": "EXP002",
        "amount": 2500.00,
        "description": "New laptop for development",
        "category": "",
        "is_suspicious": False,
        "requires_approval": False,
        "approved": False,
        "rejection_reason": "",
        "final_status": ""
    }
    
    result = app.invoke(expense2, config2)
    # Workflow is now paused, result contains current state
    
    # Get actual human input
    print("\nOptions:")
    print("1. Approve")
    print("2. Reject")
    choice = input("\nYour decision (1/2): ")
    
    if choice == "1":
        # Update state with approval
        app.update_state(
            config2,
            {"approved": True}
        )
    else:
        reason = input("Rejection reason: ")
        app.update_state(
            config2,
            {"approved": False, "rejection_reason": reason}
        )
    
    # Resume - continues from human_approval node
    result2 = app.invoke(None, config2)
    print(f"\n✅ Result: {result2['final_status']}")
    


def main():
    print("\n" + "=" * 60)
    print("Expense Approval System Challenge")
    print("=" * 60)
    
    test_expense_system()
    
    print("\n" + "=" * 60)
    print("Challenge Complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you've implemented all the TODO functions!")
        print("Also check that Ollama is running: ollama serve")
