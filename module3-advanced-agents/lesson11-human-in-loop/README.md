# Lesson 11: Human-in-the-Loop

## Theory

Human-in-the-loop systems pause execution to get human input, approval, or feedback.

### Use Cases

#### Approval Workflows
- **Financial transactions**: Require manager approval for expenses above threshold (e.g., >$5000)
- **Content publishing**: Review AI-generated blog posts, social media content, or marketing copy before publication
- **Contract signing**: Legal review of AI-drafted agreements or terms
- **Access control**: Admin approval for privilege escalations or sensitive resource access

#### Sensitive Operations
- **Data deletion**: Confirm before permanently removing customer data or critical records
- **Production deployments**: Human verification before pushing code to production environments
- **Email/message sending**: Review automated communications to customers, especially for complaints or refunds
- **API calls with side effects**: Approve before making irreversible external API calls (payments, bookings, cancellations)

#### Error Correction
- **Ambiguous inputs**: Ask user to clarify when agent encounters unclear instructions or multiple valid interpretations
- **Missing information**: Request additional context when agent lacks data to complete task
- **Confidence thresholds**: Pause when AI confidence score falls below acceptable level
- **Validation failures**: Human intervention when automated checks fail (e.g., invalid addresses, conflicting data)

#### Quality Assurance
- **Output review**: Verify AI-generated code, reports, or analyses before delivery
- **Edge case handling**: Human judgment for unusual scenarios not covered in training data
- **Compliance checks**: Ensure outputs meet regulatory requirements (GDPR, HIPAA, SOC2)
- **Brand consistency**: Review content for tone, style, and alignment with company values

#### Training and Feedback
- **Active learning**: Collect human labels for uncertain predictions to improve model
- **Preference learning**: Gather feedback on agent decisions to refine behavior (RLHF-style)
- **Error analysis**: Capture human corrections to identify systematic weaknesses
- **A/B testing**: Compare agent outputs with human choices to measure performance gaps

### Implementation with LangGraph

Use interrupts and checkpointing to pause and resume workflows.

```python
from langgraph.checkpoint import MemorySaver

workflow.add_node("human_approval", approval_node)
app = workflow.compile(checkpointer=MemorySaver(), interrupt_before=["human_approval"])
```

## Challenge

Build an **Expense Approval System** where agents categorize expenses, flag suspicious ones, and require human approval for high amounts.

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Human-in-the-Loop Guide](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/)
