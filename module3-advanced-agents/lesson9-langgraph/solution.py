"""
Lesson 9 Solution: Content Moderation Pipeline
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict
from enum import Enum
import json
from datetime import datetime


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


def detect_language(state: ModerationState) -> ModerationState:
    """Detect content language"""
    # Simple detection (in production, use a library)
    state["language"] = "en"
    state["checks"] += 1
    return state


def check_toxicity(state: ModerationState) -> ModerationState:
    """Check if content is toxic"""
    toxic_words = ["spam", "hate", "abuse", "scam", "fraud"]
    state["is_toxic"] = any(word in state["content"].lower() for word in toxic_words)
    state["checks"] += 1
    return state


def analyze_sentiment(state: ModerationState) -> ModerationState:
    """Analyze sentiment"""
    positive_words = ["great", "awesome", "love", "excellent", "amazing"]
    negative_words = ["bad", "hate", "terrible", "awful", "worst"]
    
    content_lower = state["content"].lower()
    pos_count = sum(1 for word in positive_words if word in content_lower)
    neg_count = sum(1 for word in negative_words if word in content_lower)
    
    if pos_count > neg_count:
        state["sentiment"] = "positive"
    elif neg_count > pos_count:
        state["sentiment"] = "negative"
    else:
        state["sentiment"] = "neutral"
    
    state["checks"] += 1
    return state


def make_decision(state: ModerationState) -> ModerationState:
    """Make moderation decision"""
    if state["is_toxic"]:
        state["decision"] = Decision.REJECT
        state["reason"] = "Toxic content detected"
    elif state["sentiment"] == "positive" and not state["is_toxic"]:
        state["decision"] = Decision.APPROVE
        state["reason"] = "Clean and positive content"
    else:
        state["decision"] = Decision.REVIEW
        state["reason"] = "Neutral content requires human review"
    
    return state


def log_decision(state: ModerationState) -> ModerationState:
    """Log the decision"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "content": state["content"][:50] + "...",
        "decision": state["decision"],
        "reason": state["reason"],
        "sentiment": state["sentiment"],
        "is_toxic": state["is_toxic"],
        "checks": state["checks"]
    }
    
    # Append to log file
    try:
        with open("moderation_log.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass
    
    return state


def create_moderation_pipeline():
    """Create the moderation graph"""
    workflow = StateGraph(ModerationState)
    
    # Add nodes
    workflow.add_node("detect_language", detect_language)
    workflow.add_node("check_toxicity", check_toxicity)
    workflow.add_node("analyze_sentiment", analyze_sentiment)
    workflow.add_node("make_decision", make_decision)
    workflow.add_node("log_decision", log_decision)
    
    # Add edges
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
        "This is spam and abuse, total scam",
        "This is okay, nothing special",
        "Excellent service, highly recommend!",
        "Terrible experience, worst ever"
    ]
    
    print("=" * 60)
    print("Content Moderation Pipeline")
    print("=" * 60 + "\n")
    
    app = create_moderation_pipeline()
    
    for i, content in enumerate(test_content, 1):
        print(f"\n[{i}] Content: \"{content}\"")
        print("-" * 60)
        
        result = app.invoke({
            "content": content,
            "language": "",
            "is_toxic": False,
            "sentiment": "",
            "decision": "",
            "reason": "",
            "checks": 0
        })
        
        # Display results
        print(f"Language: {result['language']}")
        print(f"Toxic: {result['is_toxic']}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Decision: {result['decision'].upper()}")
        print(f"Reason: {result['reason']}")
        print(f"Checks: {result['checks']}")
    
    print("\n" + "=" * 60)
    print("\n✅ Moderation complete! Check moderation_log.jsonl for logs.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure langgraph is installed:")
        print("  pip install langgraph")
