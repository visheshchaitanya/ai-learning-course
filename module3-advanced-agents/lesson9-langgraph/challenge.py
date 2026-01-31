"""
Lesson 9 Challenge: Content Moderation Pipeline

Build a graph-based content moderation system.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from enum import Enum
import traceback


class Decision(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REVIEW = "review"


class ModerationState(TypedDict):
    content: str
    language: str
    is_toxic: bool
    sentiment: str
    decision: str
    reason: str
    checks: int


# TODO: Implement nodes
def detect_language(state: ModerationState) -> ModerationState:
    """Detect content language"""
    # TODO: Implement language detection
    # For now, assume English
    state["language"] = "en"
    state["checks"] += 1
    return state


def check_toxicity(state: ModerationState) -> ModerationState:
    """Check if content is toxic"""
    # TODO: Implement toxicity check
    # Simple keyword-based for demo
    toxic_words = ["spam", "hate", "abuse"]
    state["is_toxic"] = any(word in state["content"].lower() for word in toxic_words)
    state["checks"] += 1
    return state


def analyze_sentiment(state: ModerationState) -> ModerationState:
    """Analyze sentiment"""
    # TODO: Implement sentiment analysis
    # Simple keyword-based
    positive_words = ["great", "awesome", "love"]
    negative_words = ["bad", "hate", "terrible"]
    
    content_lower = state["content"].lower()
    if any(word in content_lower for word in positive_words):
        state["sentiment"] = "positive"
    elif any(word in content_lower for word in negative_words):
        state["sentiment"] = "negative"
    else:
        state["sentiment"] = "neutral"
    
    state["checks"] += 1
    return state


def make_decision(state: ModerationState) -> ModerationState:
    """Make moderation decision"""
    # TODO: Implement decision logic
    if state["is_toxic"] or state["sentiment"] == "negative":
        state["decision"] = Decision.REJECT
        state["reason"] = "Toxic content detected or negative sentiment"
    elif state["sentiment"] == "positive":
        state["decision"] = Decision.APPROVE
        state["reason"] = "Clean and positive"
    else:
        state["decision"] = Decision.REVIEW
        state["reason"] = "Requires human review"
    
    return state


def log_decision(state: ModerationState) -> ModerationState:
    """Log the decision"""
    # TODO: Log to file
    with open("moderation_log.txt", "a") as f:
        f.write(f"{state['content']}\n{state['decision']}\n{state['reason']}\n{state['checks']}\n\n")
    return state


# TODO: Build the graph
def create_moderation_pipeline():
    """Create the moderation graph"""
    # TODO: Create StateGraph
    # TODO: Add nodes
    # TODO: Add edges (including conditional)
    # TODO: Compile and return
    workflow = StateGraph(ModerationState)
    workflow.add_node("detect_language", detect_language)
    workflow.add_node("check_toxicity", check_toxicity)
    workflow.add_node("analyze_sentiment", analyze_sentiment)
    workflow.add_node("make_decision", make_decision)
    workflow.add_node("log_decision", log_decision)
    workflow.set_entry_point("detect_language")
    workflow.add_edge("detect_language", "check_toxicity")
    workflow.add_edge("check_toxicity", "analyze_sentiment")
    workflow.add_edge("analyze_sentiment", "make_decision")
    workflow.add_edge("make_decision", "log_decision")
    workflow.add_edge("log_decision", END)
    return workflow.compile()


def main():
    """Test moderation pipeline"""
    test_content = [
        "This is a great product! Love it!",
        "This is spam and abuse",
        "This is okay, nothing special"
    ]
    
    print("=" * 60)
    print("Content Moderation Pipeline")
    print("=" * 60 + "\n")
    
    # TODO: Create pipeline
    app = create_moderation_pipeline()
    
    for content in test_content:
        print(f"Content: {content}")
        # TODO: Run moderation
        try:
            result = app.invoke({
                "content": content,
                "language": "",
                "is_toxic": False,
                "sentiment": "",
                "decision": "",
                "reason": "",
                "checks": 0
            })
        except Exception as e:
            print(f"Error: {e}")
            print(traceback.format_exc())
            continue
        
        print(f"Decision: {result['decision']}")
        print(f"Reason: {result['reason']}")
        print(f"Checks: {result['checks']}")
        print()   


if __name__ == "__main__":
    main()
