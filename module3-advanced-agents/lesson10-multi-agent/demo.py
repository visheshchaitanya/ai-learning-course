"""
Lesson 10 Demo: Multi-Agent Systems

This demo shows how multiple agents can collaborate using LangGraph.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.chat_models import ChatOllama

print("""
Multi-Agent Systems Demo

This lesson demonstrates:
1. Supervisor pattern with worker agents
2. Agent communication via shared state
3. Task delegation and coordination

Run the solution.py for a complete multi-agent implementation.
""")
