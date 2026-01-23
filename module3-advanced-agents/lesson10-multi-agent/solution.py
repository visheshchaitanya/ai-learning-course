"""
Lesson 10 Solution: Software Team Simulator

Multi-agent system with PM, Developer, and QA agents.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_community.chat_models import ChatOllama


class TeamState(TypedDict):
    feature_request: str
    plan: str
    implementation: str
    qa_report: str
    status: str


def pm_agent(state: TeamState) -> TeamState:
    """PM creates a plan"""
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    prompt = f"As a PM, create a brief plan for: {state['feature_request']}"
    state["plan"] = llm.invoke(prompt).content
    print(f"\n👔 PM: Created plan")
    return state


def dev_agent(state: TeamState) -> TeamState:
    """Developer implements"""
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    prompt = f"As a developer, describe implementation for: {state['plan']}"
    state["implementation"] = llm.invoke(prompt).content
    print(f"\n💻 Developer: Implemented feature")
    return state


def qa_agent(state: TeamState) -> TeamState:
    """QA reviews"""
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    prompt = f"As QA, review this implementation: {state['implementation']}"
    state["qa_report"] = llm.invoke(prompt).content
    state["status"] = "completed"
    print(f"\n🧪 QA: Completed review")
    return state


def create_team():
    """Create multi-agent team"""
    workflow = StateGraph(TeamState)
    
    workflow.add_node("pm", pm_agent)
    workflow.add_node("dev", dev_agent)
    workflow.add_node("qa", qa_agent)
    
    workflow.set_entry_point("pm")
    workflow.add_edge("pm", "dev")
    workflow.add_edge("dev", "qa")
    workflow.add_edge("qa", END)
    
    return workflow.compile()


def main():
    print("=" * 60)
    print("Software Team Simulator")
    print("=" * 60)
    
    app = create_team()
    
    feature = "Add user authentication with email and password"
    
    result = app.invoke({
        "feature_request": feature,
        "plan": "",
        "implementation": "",
        "qa_report": "",
        "status": "pending"
    })
    
    print("\n" + "=" * 60)
    print("\n📋 Final Report:")
    print(f"\nFeature: {feature}")
    print(f"\nPlan:\n{result['plan']}")
    print(f"\nImplementation:\n{result['implementation']}")
    print(f"\nQA Report:\n{result['qa_report']}")
    print(f"\nStatus: {result['status']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running and llama3.2 is pulled")
