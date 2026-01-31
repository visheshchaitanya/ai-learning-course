"""
Lesson 19: Advanced RAG Techniques Implementation

Complete implementations of advanced RAG techniques.
"""

from langchain_community.chat_models import ChatOllama
from typing import List

# Query Transformation
def transform_query(query: str) -> List[str]:
    """Generate multiple query variations"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Generate 3 different ways to ask this question:
    
Original: {query}

Return only the 3 variations, one per line."""
    
    response = llm.invoke(prompt).content
    variations = [line.strip() for line in response.split('\n') if line.strip()]
    return variations[:3]


# HyDE (Hypothetical Document Embeddings)
def generate_hypothetical_answer(query: str) -> str:
    """Generate hypothetical answer for better retrieval"""
    llm = ChatOllama(model="llama3.2")
    prompt = f"""Generate a hypothetical answer to this question:
    
Question: {query}

Answer (be specific and detailed):"""
    
    return llm.invoke(prompt).content


# Multi-Query Retrieval
def multi_query_retrieve(query: str, vectorstore, k: int = 5) -> List:
    """Retrieve using multiple query variations"""
    queries = transform_query(query)
    queries.append(query)  # Include original
    
    all_docs = []
    seen_ids = set()
    
    for q in queries:
        docs = vectorstore.similarity_search(q, k=k)
        for doc in docs:
            doc_id = hash(doc.page_content)
            if doc_id not in seen_ids:
                all_docs.append(doc)
                seen_ids.add(doc_id)
    
    return all_docs


# Re-ranking (simplified)
def rerank_documents(query: str, documents: List, top_k: int = 3) -> List:
    """Re-rank documents by relevance"""
    llm = ChatOllama(model="llama3.2")
    
    scored_docs = []
    for doc in documents:
        prompt = f"""Rate relevance of this document to the query (0-10):
        
Query: {query}
Document: {doc.page_content[:200]}...

Score (0-10):"""
        
        try:
            score_text = llm.invoke(prompt).content
            score = float(score_text.strip().split()[0])
        except:
            score = 5.0
        
        scored_docs.append((score, doc))
    
    # Sort by score
    scored_docs.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in scored_docs[:top_k]]


print("Advanced RAG Techniques Module")
print("=" * 70)
print("\nAvailable functions:")
print("  - transform_query(): Generate query variations")
print("  - generate_hypothetical_answer(): HyDE technique")
print("  - multi_query_retrieve(): Multi-query retrieval")
print("  - rerank_documents(): Re-rank by relevance")
print("\nSee demo.py for usage examples")
