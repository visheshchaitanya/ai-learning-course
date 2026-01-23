# Lesson 4: Embeddings & Vector Search

## Theory

### What are Embeddings?

Embeddings are numerical representations of text (or other data) as vectors in high-dimensional space. Similar concepts are close together in this space.

**Example:**
```
"dog" → [0.2, 0.8, 0.1, ...]  (768 dimensions)
"cat" → [0.3, 0.7, 0.2, ...]  (close to "dog")
"car" → [0.9, 0.1, 0.8, ...]  (far from "dog")
```

### Why Embeddings Matter

1. **Semantic Search**: Find similar meaning, not just keywords
2. **RAG**: Retrieve relevant documents for LLM context
3. **Clustering**: Group similar items
4. **Recommendations**: Find similar content

### How Embeddings Work

1. Text → Embedding Model → Vector
2. Store vectors in database
3. Query → Vector
4. Find nearest neighbors (similarity search)

### Similarity Metrics

**Cosine Similarity**: Measures angle between vectors (most common)
```python
similarity = dot(A, B) / (||A|| * ||B||)
# Range: -1 to 1 (1 = identical, 0 = orthogonal, -1 = opposite)
```

**Euclidean Distance**: Straight-line distance
```python
distance = sqrt(sum((A[i] - B[i])^2))
# Lower = more similar
```

**Dot Product**: Raw similarity (not normalized)

### Vector Databases

Store and search embeddings efficiently:

**ChromaDB**:
- Simple, embedded database
- Great for prototyping
- Persistent storage
- Built-in filtering

**FAISS** (Facebook AI Similarity Search):
- Extremely fast
- Handles millions of vectors
- Multiple index types
- In-memory by default

**Others**: Pinecone, Weaviate, Qdrant, Milvus

### Chunking Strategies

Breaking documents into smaller pieces for efficient retrieval.

#### Why Chunking?

**Problem 1: Context Window Limits**
- LLMs have finite context windows (e.g., 128k tokens for GPT-4)
- Large documents (500-page manuals) won't fit in one prompt
- Chunking breaks content into manageable pieces

**Problem 2: Retrieval Precision & Cost**
- **Relevance**: Smaller chunks = more precise retrieval
  - Query: "How do I reset my password?"
  - Better: 200-token chunk about password reset
  - Worse: 10k-token chunk about entire user management system
- **Cost**: Fewer tokens in context = cheaper API calls
- **Quality**: Too much irrelevant context confuses the model (needle-in-haystack)

**Example Workflow:**
```
Large Document → Chunk → Embed Each → Store in Vector DB
                                            ↓
User Query → Embed → Find Similar Chunks → Send ONLY relevant chunks to LLM
```

**Without chunking**: 100-page manual → embed as one → retrieve entire 50k tokens
**With chunking**: 100-page manual → 200 chunks → retrieve 3-5 relevant chunks (2.5k tokens)

#### Chunking Methods

**Fixed Size**: Split every N characters/tokens
```python
chunks = [text[i:i+500] for i in range(0, len(text), 500)]
```

**Sentence-based**: Split on sentence boundaries
```python
chunks = text.split('. ')
```

**Recursive**: Split by paragraphs, then sentences, then words
- Best for maintaining context
- LangChain's RecursiveCharacterTextSplitter

**Semantic**: Split based on topic changes (advanced)

**Best Practices**:
- Chunk size: 200-1000 tokens
  - Too small (50 tokens): Loses context, breaks mid-sentence
  - Too large (5k tokens): Less precise retrieval, more noise
- Overlap: 10-20% for context continuity
- Preserve structure (paragraphs, sections)

#### What About Long Queries?

**Don't chunk queries** - it breaks semantic coherence. Instead:

1. **Embed the full query** (most common)
   - Queries are typically short (<500 tokens)
   - Modern embedding models handle complex multi-faceted queries well

2. **Query Decomposition** (for complex queries)
   ```python
   # Long query: "I'm building a Flask app with PostgreSQL on AWS Lambda..."
   # LLM decomposes into:
   sub_queries = [
       "Flask PostgreSQL integration patterns",
       "AWS Lambda with Flask best practices",
       "S3 file upload handling in serverless"
   ]
   # Retrieve for each, combine results
   ```

3. **Hypothetical Document Embeddings (HyDE)**
   ```python
   query → LLM generates hypothetical answer → embed answer → retrieve
   # Works because answers are semantically closer to documents than questions
   ```

**Key Insight**: Document chunking is necessary; query chunking is counterproductive.

### Embedding Models

**Ollama Embeddings**:
- `nomic-embed-text`: 768 dimensions, great quality
- `mxbai-embed-large`: 1024 dimensions, high performance
- Run locally, no API costs

**OpenAI Embeddings**:
- `text-embedding-3-small`: Fast, cheap
- `text-embedding-3-large`: Best quality

## Demo

See `demo.py` for complete examples:
1. Generate embeddings with Ollama
2. Calculate cosine similarity
3. Store embeddings in ChromaDB
4. Semantic search with ChromaDB
5. FAISS for fast search
6. Document chunking strategies
7. Metadata filtering

### Quick Example

```python
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Sample documents
docs = ["Dogs are great pets", "Cats are independent", "Cars need fuel"]

# Create vector store
vectorstore = Chroma.from_texts(docs, embeddings)

# Search
results = vectorstore.similarity_search("puppies", k=1)
print(results[0].page_content)  # "Dogs are great pets"
```

## Challenge

Build a **Semantic FAQ System** that:

1. Loads Q&A pairs from a JSON file
2. Embeds all questions
3. Stores in a vector database (ChromaDB)
4. Takes user queries
5. Finds the most similar question
6. Returns the corresponding answer
7. Shows similarity score

**Requirements:**
- Load at least 10 FAQ pairs from `data/faq.json`
- Use Ollama embeddings (`nomic-embed-text`)
- Store in ChromaDB with persistence
- Return top 3 similar questions with scores
- Add metadata (category, tags) to FAQs
- Support filtering by category
- Handle queries that don't match well (threshold)

**Starter code in `challenge.py`**

**Example Interaction:**
```
FAQ System Ready! (10 questions loaded)

Query: How do I reset my password?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top Match (95% similar):
Q: What is the process to reset my password?
A: Click 'Forgot Password' on the login page...

Other similar questions:
  • How do I change my password? (78%)
  • I can't log in, what should I do? (65%)
```

**Bonus:**
- Add new FAQs dynamically
- Export/import vector database
- Highlight why questions matched (show query terms)

## Resources

- [Embeddings Guide](https://python.langchain.com/docs/modules/data_connection/text_embedding/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [FAISS Docs](https://github.com/facebookresearch/faiss)
- [Ollama Embeddings](https://ollama.com/blog/embedding-models)
- [Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
