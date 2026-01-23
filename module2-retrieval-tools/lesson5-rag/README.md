# Lesson 5: RAG (Retrieval Augmented Generation)

## Theory

### What is RAG?

RAG combines retrieval (finding relevant documents) with generation (LLM responses). Instead of relying solely on the LLM's training data, we:

1. **Retrieve** relevant documents from a knowledge base
2. **Augment** the prompt with retrieved context
3. **Generate** a response using both the context and the query

**Benefits:**
- Access to current/private information
- Reduced hallucinations
- Citable sources
- No model retraining needed

### RAG Architecture

```
User Query
    ↓
Embed Query
    ↓
Vector Search → Retrieve Top-K Documents
    ↓
Format Context
    ↓
LLM (Query + Context) → Generate Answer
    ↓
Response (with sources)
```

### RAG Pipeline Components

#### 1. Document Loaders
Load documents from various sources:
- **TextLoader**: Plain text files
- **PyPDFLoader**: PDF documents
- **WebBaseLoader**: Web pages
- **DirectoryLoader**: Batch load from folder
- **CSVLoader**, **JSONLoader**, etc.

#### 2. Text Splitters
Break documents into chunks:
- **RecursiveCharacterTextSplitter**: Best for most use cases
- **CharacterTextSplitter**: Simple splitting
- **TokenTextSplitter**: Split by tokens
- **MarkdownTextSplitter**: Preserves markdown structure

**Key Parameters:**
- `chunk_size`: Target chunk size (characters/tokens)
- `chunk_overlap`: Overlap between chunks (for context)
- `separators`: How to split (paragraphs, sentences, etc.)

#### 3. Vector Store
Store and search embeddings (covered in Lesson 4)

#### 4. Retriever
Interface for fetching relevant documents:
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
docs = retriever.get_relevant_documents("query")
```

#### 5. RAG Chain
Combine retrieval + generation:
```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)
```

### RAG with LCEL

Modern approach using LangChain Expression Language:

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is quantum computing?")
```

### Retrieval Strategies

**Similarity Search**: Default, finds most similar vectors
```python
docs = vectorstore.similarity_search(query, k=3)
```

**MMR (Maximal Marginal Relevance)**: Balances relevance and diversity
```python
docs = vectorstore.max_marginal_relevance_search(query, k=3)
```

**Similarity Score Threshold**: Only return above threshold
```python
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.5, "k": 3}
)
```

### Source Citations

Track where information came from:
```python
result = qa_chain({"query": "What is AI?"})
answer = result["result"]
sources = result["source_documents"]

for doc in sources:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:100]}...")
```

## Demo

See `demo.py` for complete examples:
1. Load documents (TXT, PDF, web)
2. Split documents with different strategies
3. Create vector store from documents
4. Build basic RAG chain
5. RAG with LCEL
6. RAG with source citations
7. Streaming RAG responses

### Quick Example

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

# Load and split
loader = TextLoader("document.txt")
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Create vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(chunks, embeddings)

# Create RAG chain
llm = ChatOllama(model="llama3.2")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Query
result = qa_chain({"query": "What is the main topic?"})
print(result["result"])
```

## Challenge

Build a **Document Q&A System** that:

1. Ingests multiple PDF documents from a folder
2. Chunks them appropriately
3. Creates a persistent vector store
4. Answers questions with source citations
5. Supports follow-up questions with conversation history
6. Shows relevant document excerpts

**Requirements:**
- Load all PDFs from `documents/` folder
- Use RecursiveCharacterTextSplitter (chunk_size=1000, overlap=200)
- Store in persistent ChromaDB
- Return top 3 most relevant chunks
- Show source document and page number for each citation
- Implement conversation memory for follow-ups
- Add streaming responses
- Handle "I don't know" when context doesn't contain answer

**Starter code in `challenge.py`**

**Example Interaction:**
```
Document Q&A System
Loaded 5 documents (127 chunks)

Ask a question: What are the key findings?

Answer:
The key findings indicate that machine learning models
perform better with larger datasets...

Sources:
  📄 research_paper.pdf (page 3)
     "Our experiments show that model accuracy improves..."
  
  📄 analysis.pdf (page 7)
     "The data suggests a strong correlation between..."

Ask a question: Can you elaborate on the first finding?
[Uses conversation history to understand "first finding"]
```

**Bonus:**
- Add metadata filtering (by document, date, author)
- Implement MMR retrieval for diverse results
- Add document upload functionality
- Export Q&A history to markdown

## Resources

- [RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
- [Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [Retrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/)
- [RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
