"""
Lesson 19 Demo: Advanced RAG Techniques

Demonstrates query transformation, HyDE, multi-query, and re-ranking.
"""

from advanced_techniques import (
    transform_query,
    generate_hypothetical_answer,
    multi_query_retrieve,
    rerank_documents
)

print("Advanced RAG Demo")
print("=" * 70)

# Demo 1: Query Transformation
print("\n📋 Demo 1: Query Transformation")
query = "What is machine learning?"
print(f"Original: {query}")
variations = transform_query(query)
print("Variations:")
for i, var in enumerate(variations, 1):
    print(f"  {i}. {var}")

# Demo 2: HyDE
print("\n📋 Demo 2: HyDE (Hypothetical Document Embeddings)")
print(f"Query: {query}")
hyp_answer = generate_hypothetical_answer(query)
print(f"Hypothetical answer:\n{hyp_answer[:200]}...")

print("\n" + "=" * 70)
print("See advanced_techniques.py for implementations")
print("See challenge.py and solution.py for complete system")
