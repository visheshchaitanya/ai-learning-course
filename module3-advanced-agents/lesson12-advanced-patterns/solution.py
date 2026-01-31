"""
Lesson 12 Solution: Self-Reflecting Code Review Agent

Complete implementation of code review agent with self-reflection pattern.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.chat_models import ChatOllama
import ast
import re


class CodeReviewState(TypedDict):
    """State for code review agent"""
    description: str
    code: str
    critique: str
    revision_count: int
    quality_score: float
    issues: list[str]


def generate_code(state: CodeReviewState) -> CodeReviewState:
    """Generate Python code from description"""
    print(f"\n🎯 Generating code for: {state['description']}")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    prompt = f"""Generate a Python function based on this description:

{state['description']}

Requirements:
- Include docstring
- Add type hints
- Handle edge cases
- Use clear variable names

Provide ONLY the Python code, no explanations or markdown:"""
    
    code = llm.invoke(prompt).content
    
    # Clean up code (remove markdown if present)
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    state["code"] = code
    state["revision_count"] = 0
    state["quality_score"] = 0.0
    state["issues"] = []
    
    print(f"✅ Generated code ({len(code)} chars)")
    return state


def critique_code(state: CodeReviewState) -> CodeReviewState:
    """Critique the generated code"""
    print(f"\n🔍 Critiquing code (revision #{state['revision_count']})...")
    
    issues = []
    
    # Check syntax
    try:
        ast.parse(state["code"])
        print("✅ Syntax valid")
    except SyntaxError as e:
        issues.append(f"Syntax error: {e}")
        print(f"❌ Syntax error: {e}")
        state["quality_score"] = 0.0
        state["issues"] = issues
        state["critique"] = f"Syntax error: {e}"
        return state
    
    # LLM-based critique
    llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    prompt = f"""Review this Python code and provide detailed critique:

Code:
```python
{state['code']}
```

Original requirement: {state['description']}

Provide:
1. Quality Score: [0.0-1.0] (be critical, only give >0.8 for excellent code)
2. Strengths: What's done well
3. Issues: Specific problems with:
   - Correctness (does it work?)
   - Edge cases (what's missing?)
   - Style (PEP 8, naming)
   - Efficiency (can it be better?)
   - Documentation (docstring quality)

Format:
Quality Score: X.X
Strengths:
- ...
Issues:
- ..."""
    
    critique = llm.invoke(prompt).content
    state["critique"] = critique
    
    # Extract quality score
    score = 0.5  # Default
    try:
        for line in critique.split('\n'):
            if 'quality score' in line.lower() or 'score:' in line.lower():
                # Find float between 0 and 1
                numbers = re.findall(r'0\.\d+|1\.0|^1$|^0$', line)
                if numbers:
                    score = float(numbers[0])
                    break
    except Exception as e:
        print(f"⚠️  Could not extract score: {e}")
    
    state["quality_score"] = score
    
    # Extract issues
    in_issues_section = False
    for line in critique.split('\n'):
        line = line.strip()
        if 'issues:' in line.lower():
            in_issues_section = True
            continue
        if in_issues_section and line.startswith('-'):
            issues.append(line.lstrip('- ').strip())
    
    state["issues"] = issues
    
    print(f"📊 Quality Score: {state['quality_score']:.2f}")
    print(f"🐛 Issues found: {len(state['issues'])}")
    if state["issues"]:
        for issue in state["issues"][:3]:  # Show first 3
            print(f"   - {issue[:80]}...")
    
    return state


def revise_code(state: CodeReviewState) -> CodeReviewState:
    """Revise code based on critique"""
    print(f"\n✏️  Revising code based on feedback...")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    issues_text = "\n".join(f"- {issue}" for issue in state["issues"]) if state["issues"] else "General improvements needed"
    
    prompt = f"""Revise this Python code to address the critique:

Original Code:
```python
{state['code']}
```

Critique:
{state['critique']}

Key Issues to Fix:
{issues_text}

Provide improved code that:
- Fixes all identified issues
- Maintains functionality
- Improves quality

Return ONLY the Python code, no explanations or markdown:"""
    
    code = llm.invoke(prompt).content
    
    # Clean up code
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()
    
    state["code"] = code
    state["revision_count"] += 1
    
    print(f"✅ Revision #{state['revision_count']} complete")
    return state


def check_quality(state: CodeReviewState) -> CodeReviewState:
    """Final quality check"""
    print(f"\n✔️  Final quality check...")
    
    # Validate syntax one more time
    try:
        ast.parse(state["code"])
        print("✅ Final syntax check passed")
    except SyntaxError as e:
        print(f"❌ Final syntax check failed: {e}")
        state["quality_score"] = 0.0
        return state
    
    # Check for basic quality markers
    quality_markers = {
        "has_docstring": '"""' in state["code"] or "'''" in state["code"],
        "has_def": "def " in state["code"],
        "reasonable_length": 10 < len(state["code"].split('\n')) < 100,
        "has_return": "return" in state["code"]
    }
    
    passed = sum(quality_markers.values())
    print(f"📋 Quality markers: {passed}/{len(quality_markers)} passed")
    
    return state


def should_revise(state: CodeReviewState) -> str:
    """Decide whether to continue revising"""
    # Quality threshold met
    if state["quality_score"] >= 0.8:
        print(f"✅ Quality threshold met ({state['quality_score']:.2f} >= 0.8)")
        return "done"
    
    # Max revisions reached
    if state["revision_count"] >= 3:
        print(f"⏹️  Max revisions reached ({state['revision_count']})")
        return "done"
    
    # Continue revising
    print(f"🔄 Continuing revision (score: {state['quality_score']:.2f}, attempt: {state['revision_count']})")
    return "revise"


def create_code_review_agent():
    """Create the code review agent workflow"""
    workflow = StateGraph(CodeReviewState)
    
    # Add nodes
    workflow.add_node("generate", generate_code)
    workflow.add_node("critique", critique_code)
    workflow.add_node("revise", revise_code)
    workflow.add_node("check", check_quality)
    
    # Set entry point
    workflow.set_entry_point("generate")
    
    # Add edges
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
    
    # Compile
    app = workflow.compile()
    return app


def main():
    """Test the code review agent"""
    print("=" * 70)
    print("Code Review Agent Solution")
    print("=" * 70)
    
    agent = create_code_review_agent()
    
    # Test cases
    test_cases = [
        "Write a function to calculate factorial of a number",
        "Write a function to check if a string is a palindrome",
        "Write a function to find the nth Fibonacci number using memoization"
    ]
    
    for i, description in enumerate(test_cases, 1):
        print("\n" + "=" * 70)
        print(f"Test {i}/{len(test_cases)}: {description}")
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
            print("\n" + "=" * 70)
            print(f"📊 Revisions: {result['revision_count']}")
            print(f"📊 Final Quality Score: {result['quality_score']:.2f}")
            print("=" * 70)
            
            # Test the code
            print("\n🧪 Testing generated code...")
            try:
                # Create a safe namespace for execution
                namespace = {}
                exec(result["code"], namespace)
                print("✅ Code executes without errors")
                
                # Try to find and call the function
                for name, obj in namespace.items():
                    if callable(obj) and not name.startswith('_'):
                        print(f"✅ Found function: {name}()")
                        break
                        
            except Exception as e:
                print(f"⚠️  Execution test failed: {e}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("✅ Self-reflection with quality scoring")
    print("✅ Iterative improvement through critique")
    print("✅ Syntax validation with ast.parse()")
    print("✅ Quality threshold and max iteration limits")
    print("✅ Detailed, actionable feedback")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
