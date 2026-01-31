"""
Lesson 10 Challenge: Software Team Simulator

Build a multi-agent system with PM, Developer, and QA agents.

Requirements:
1. PM Agent: Creates a plan for the feature
2. Developer Agent: Describes implementation approach
3. QA Agent: Reviews and provides feedback
4. Use LangGraph to orchestrate the workflow
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.chat_models import ChatOllama
import traceback
from langchain_core.prompts import ChatPromptTemplate


class TeamState(TypedDict):
    """Shared state for all agents"""
    feature_request: str
    plan: str
    implementation: str
    qa_report: str
    status: str


def pm_agent(state: TeamState) -> TeamState:
    """PM creates a plan for the feature"""
    # TODO: Initialize ChatOllama model
    # TODO: Create a prompt asking PM to plan the feature
    # TODO: Update state["plan"] with the response
    # TODO: Print a status message
    llm = ChatOllama(model="llama3.2", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Create a plan for the feature: {feature_request}"
    )
    chain = prompt | llm
    result = chain.invoke({"feature_request": state["feature_request"]})
    state["plan"] = result
    state["status"] = "feature_planned"
    print(f"👔 PM: Planning feature... {result}")
    return state


def dev_agent(state: TeamState) -> TeamState:
    """Developer implements the feature"""
    # TODO: Initialize ChatOllama model
    # TODO: Create a prompt asking developer to implement based on the plan
    # TODO: Update state["implementation"] with the response
    # TODO: Print a status message
    llm = ChatOllama(model="llama3.2", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Implement the feature: {plan}"
    )
    chain = prompt | llm
    result = chain.invoke({"plan": state["plan"]})
    state["implementation"] = result
    state["status"] = "feature_implemented"
    print(f"💻 Developer: Implementing feature... {result}")
    return state


def qa_agent(state: TeamState) -> TeamState:
    """QA reviews the implementation"""
    # TODO: Initialize ChatOllama model
    # TODO: Create a prompt asking QA to review the implementation
    # TODO: Update state["qa_report"] with the response
    # TODO: Update state["status"] to "completed"
    # TODO: Print a status message
    llm = ChatOllama(model="llama3.2", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Review the implementation: {implementation}"
    )
    chain = prompt | llm
    result = chain.invoke({"implementation": state["implementation"]})
    state["qa_report"] = result
    state["status"] = "completed"
    print(f"🧪 QA: Reviewing implementation... {result}")
    return state


def create_team():
    """Create the multi-agent workflow"""
    # TODO: Create StateGraph with TeamState
    # TODO: Add nodes for pm, dev, and qa agents
    # TODO: Set entry point to "pm"
    # TODO: Add edges: pm -> dev -> qa -> END
    # TODO: Compile and return the workflow
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
    print("Software Team Simulator Challenge")
    print("=" * 60)
    
    # TODO: Create the team workflow
    # TODO: Define a feature request
    # TODO: Initialize the state with empty values
    # TODO: Invoke the workflow with the initial state
    # TODO: Print the final results (plan, implementation, qa_report)
    try:    
        workflow = create_team()
        feature = "Add user authentication with email and password"
        result = workflow.invoke({
            "feature_request": feature,
            "plan": "",
            "implementation": "",
            "qa_report": "",
            "status": "pending"
        })
        print(f"\n📋 Feature Request: {feature}")
        print(f"\nPlan:\n{result['plan']}")
        print(f"\nImplementation:\n{result['implementation']}")
        print(f"\nQA Report:\n{result['qa_report']}")
        print(f"\nStatus: {result['status']}")
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nHint: Make sure Ollama is running and llama3.2 is installed")
        print("See solution.py for reference implementation")
