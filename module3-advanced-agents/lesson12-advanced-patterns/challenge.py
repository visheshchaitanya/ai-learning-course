"""
Lesson 12 Challenge: Code Review Agent

Build an agent that generates code, critiques it, and revises it iteratively
until quality threshold is met.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.chat_models import ChatOllama
import ast


class CodeReviewState(TypedDict):
    """State for code review agent"""
    description: str  # What code to generate
    code: str  # Generated code
    critique: str  # Critique of the code
    revision_count: int  # Number of revisions
    quality_score: float  # Quality score 0-1
    issues: list[str]  # List of identified issues


def generate_code(state: CodeReviewState) -> CodeReviewState:
    """
    Generate Python code from description.
    
    TODO: Implement code generation
    - Use LLM to generate code from description
    - Initialize revision_count to 0
    - Set initial quality_score to 0.0
    """
    print(f"\n🎯 Generating code for: {state['description']}")
    
    # TODO: Initialize LLM
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # TODO: Create prompt for code generation
    prompt = f"""Generate a Python function based on this description:

{state['description']}

Provide ONLY the Python code, no explanations."""
    
    # TODO: Generate code
    state["code"] = llm.invoke(prompt).content
    state["revision_count"] = 0
    state["quality_score"] = 0.0
    state["issues"] = []
    
    print(f"✅ Generated code ({len(state['code'])} chars)")
    return state


def critique_code(state: CodeReviewState) -> CodeReviewState:
    """
    Critique the generated code.
    
    TODO: Implement code critique
    - Check for syntax errors using ast.parse()
    - Evaluate code quality (style, efficiency, correctness)
    - Assign quality score 0.0-1.0
    - List specific issues
    """
    print(f"\n🔍 Critiquing code (revision #{state['revision_count']})...")
    
    issues = []
    
    # TODO: Check syntax
    try:
        ast.parse(state["code"])
        print("✅ Syntax valid")
    except SyntaxError as e:
        issues.append(f"Syntax error: {e}")
        print(f"❌ Syntax error: {e}")
    
    # TODO: Use LLM to critique code quality
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    # TODO: Create critique prompt
    prompt = f"""Review this Python code and provide:

1. Quality Score (0.0-1.0)
2. Strengths
3. Issues (style, efficiency, correctness, edge cases)

Code:
```python
{state['code']}
```

Be specific and actionable."""
    
    # TODO: Get critique
    critique = llm.invoke(prompt).content
    state["critique"] = critique
    
    # TODO: Extract quality score from critique
    # Extract from critique
    import re
    try:
        lines = critique.split('\n')
        in_issues_section = False
        
        for line in lines:
            # Extract quality score
            if 'score' in line.lower() or 'quality' in line.lower():
                # Look for number between 0 and 1
                numbers = re.findall(r'0\.\d+|1\.0|0|1', line)
                if numbers:
                    state["quality_score"] = float(numbers[0])
                    break
        
        # Extract issues from the critique
        for line in lines:
            line_lower = line.lower()
            # Check if we're entering the issues section
            if 'issue' in line_lower or 'problem' in line_lower or 'improve' in line_lower:
                in_issues_section = True
            
            # Extract bullet points or numbered items as issues
            if in_issues_section and (line.strip().startswith(('-', '*', '•')) or 
                                     re.match(r'^\d+\.', line.strip())):
                issue_text = re.sub(r'^[-*•\d.]+\s*', '', line.strip())
                if issue_text and len(issue_text) > 10:  # Filter out very short lines
                    issues.append(issue_text)
    except Exception as e:
        print(f"⚠️  Error parsing critique: {e}")
        state["quality_score"] = 0.5
    
    # TODO: Extract issues
    state["issues"] = issues
    
    print(f"📊 Quality Score: {state['quality_score']}")
    print(f"🐛 Issues found: {len(state['issues'])}")
    
    return state


def revise_code(state: CodeReviewState) -> CodeReviewState:
    """
    Revise code based on critique.
    
    TODO: Implement code revision
    - Use critique to improve code
    - Increment revision_count
    - Address identified issues
    """
    print(f"\n✏️  Revising code...")
    
    # TODO: Initialize LLM
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # TODO: Create revision prompt
    prompt = f"""Revise this Python code based on the critique:

Original Code:
```python
{state['code']}
```

Critique:
{state['critique']}

Issues to fix:
{chr(10).join(f"- {issue}" for issue in state['issues'])}

Provide improved code (code only, no explanations):"""
    
    # TODO: Generate revised code
    state["code"] = llm.invoke(prompt).content
    state["revision_count"] += 1
    
    print(f"✅ Revision #{state['revision_count']} complete")
    return state


def check_quality(state: CodeReviewState) -> CodeReviewState:
    """
    Final quality check.
    
    TODO: Implement final validation
    - Verify syntax is valid
    - Check that quality score meets threshold
    """
    print(f"\n✔️  Final quality check...")
    
    # TODO: Validate syntax one more time
    try:
        ast.parse(state["code"])
        print("✅ Final syntax check passed")
    except SyntaxError as e:
        print(f"❌ Final syntax check failed: {e}")
        state["quality_score"] = 0.0
        return state
    
    # Check that quality score meets threshold
    if state["quality_score"] < 0.8:
        print(f"❌ Quality score below threshold ({state['quality_score']} < 0.8)")
        return state
    
    print(f"✅ Final quality check passed ({state['quality_score']} >= 0.8)")
    return state


def should_revise(state: CodeReviewState) -> str:
    """
    Decide whether to continue revising.
    
    TODO: Implement decision logic
    - Return "done" if quality_score >= 0.8
    - Return "done" if revision_count >= 3
    - Return "revise" otherwise
    """
    # TODO: Implement decision logic
    if state["quality_score"] >= 0.8:
        print(f"✅ Quality threshold met ({state['quality_score']} >= 0.8)")
        return "done"
    
    if state["revision_count"] >= 3:
        print(f"⏹️  Max revisions reached ({state['revision_count']})")
        return "done"
    
    return "revise"


def create_code_review_agent():
    """
    Create the code review agent workflow.
    
    TODO: Build LangGraph workflow
    - Add nodes: generate, critique, revise, check
    - Set entry point to generate
    - Add conditional edges based on should_revise
    - Compile and return
    """
    # TODO: Create StateGraph
    workflow = StateGraph(CodeReviewState)
    
    # TODO: Add nodes
    workflow.add_node("generate", generate_code)
    workflow.add_node("critique", critique_code)
    workflow.add_node("revise", revise_code)
    workflow.add_node("check", check_quality)
    
    # TODO: Set entry point
    workflow.set_entry_point("generate")
    
    # TODO: Add edges
    workflow.add_edge("generate", "critique")
    workflow.add_conditional_edges(
        "critique",
        should_revise,
        {
            "revise": "revise",
            "done": "check"
        }
    )
    workflow.add_edge("revise", "critique")
    workflow.add_edge("check", END)
    return workflow.compile()


def main():
    """Test the code review agent"""
    print("=" * 70)
    print("Code Review Agent Challenge")
    print("=" * 70)
    
    # TODO: Create agent
    agent = create_code_review_agent()
    
    if agent is None:
        print("\n❌ Agent not implemented yet!")
        print("\nTODO:")
        print("1. Implement generate_code()")
        print("2. Implement critique_code()")
        print("3. Implement revise_code()")
        print("4. Implement check_quality()")
        print("5. Implement should_revise()")
        print("6. Build workflow in create_code_review_agent()")
        print("\nSee solution.py for reference implementation")
        return
    
    # Test cases
    test_cases = [
        "Write a function to calculate factorial of a number",
        "Write a function to check if a string is a palindrome",
        "Write a function to find the nth Fibonacci number"
    ]
    
    for description in test_cases:
        print("\n" + "=" * 70)
        print(f"Test: {description}")
        print("=" * 70)
        
        try:
            result = agent.invoke({
                "description": description,
                "code": "",
                "critique": "",
                "revision_count": 0,
                "quality_score": 0.0,
                "issues": []
            })
            
            print("\n" + "=" * 70)
            print("Final Code:")
            print("=" * 70)
            print(result["code"])
            print(f"\nRevisions: {result['revision_count']}")
            print(f"Quality Score: {result['quality_score']}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
