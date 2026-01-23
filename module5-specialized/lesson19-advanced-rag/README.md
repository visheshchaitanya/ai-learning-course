# Lesson 19: Advanced RAG

## Theory

Advanced techniques for improving RAG system quality and performance.

### Techniques

**1. Query Transformation**
- Rewrite queries for better retrieval
- Generate multiple query variations
- Extract key terms

**2. HyDE (Hypothetical Document Embeddings)**
- Generate hypothetical answer
- Embed and search with it
- Better semantic matching

**3. Multi-Query Retrieval**
- Generate multiple queries
- Retrieve for each
- Combine results

**4. Re-ranking**
- Initial retrieval (fast, broad)
- Re-rank with cross-encoder (slow, accurate)
- Return top results

**5. Parent-Child Chunking**
- Store small chunks for retrieval
- Return larger parent chunks for context

**6. Metadata Filtering**
- Filter by date, author, type
- Combine with semantic search

**7. Hybrid Search**
- Combine keyword (BM25) + semantic
- Best of both worlds

### Implementation Example

```python
# Query transformation
queries = generate_multi_query(original_query)

# Retrieve for all queries
all_docs = []
for q in queries:
    docs = vectorstore.similarity_search(q)
    all_docs.extend(docs)

# Re-rank
reranked = reranker.rerank(original_query, all_docs)

# Generate answer
answer = llm.invoke(format_context(reranked[:3]))
```

## Challenge

Build an **Advanced RAG System** with query transformation, multi-query retrieval, re-ranking, and answer synthesis.

See `demo.py`, `challenge.py`, `solution.py`, and `advanced_techniques.py` for examples.

## Resources
- [Advanced RAG](https://python.langchain.com/docs/use_cases/question_answering/advanced/)
- [HyDE Paper](https://arxiv.org/abs/2212.10496)
- [Query Transformation](https://python.langchain.com/docs/use_cases/query_analysis/)
