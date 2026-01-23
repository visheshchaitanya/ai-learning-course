"""
Lesson 5 Demo: RAG (Retrieval Augmented Generation)
"""

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document


def create_sample_documents():
    """Create sample documents for demo"""
    docs = [
        Document(
            page_content="Python is a high-level programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.",
            metadata={"source": "python_intro.txt", "topic": "programming"}
        ),
        Document(
            page_content="Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
            metadata={"source": "ml_basics.txt", "topic": "AI"}
        ),
        Document(
            page_content="LangChain is a framework for developing applications powered by language models. It provides tools for chains, agents, and memory management.",
            metadata={"source": "langchain_guide.txt", "topic": "AI"}
        ),
        Document(
            page_content="Vector databases store embeddings and enable semantic search. Popular options include ChromaDB, Pinecone, and Weaviate.",
            metadata={"source": "vector_db.txt", "topic": "databases"}
        ),
    ]
    return docs


def text_splitting_demo():
    """Demonstrate different text splitting strategies"""
    print("=== Text Splitting Strategies ===\n")
    
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.
    
    Machine learning (ML) is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves.
    
    Deep learning is a subset of machine learning that uses neural networks with multiple layers. These neural networks attempt to simulate the behavior of the human brain—albeit far from matching its ability—in order to "learn" from large amounts of data.
    """
    
    # Recursive splitter (recommended)
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        length_function=len
    )
    
    chunks = recursive_splitter.split_text(long_text)
    
    print(f"Original text: {len(long_text)} characters")
    print(f"Split into {len(chunks)} chunks\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} ({len(chunk)} chars):")
        print(chunk.strip()[:100] + "...\n")


def basic_rag_chain():
    """Basic RAG chain with RetrievalQA"""
    print("=== Basic RAG Chain ===\n")
    
    # Create documents
    documents = create_sample_documents()
    
    # Create vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    # Create LLM
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # Create RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True
    )
    
    # Query
    query = "What is LangChain?"
    result = qa_chain({"query": query})
    
    print(f"Query: {query}\n")
    print(f"Answer: {result['result']}\n")
    print("Sources:")
    for doc in result['source_documents']:
        print(f"  - {doc.metadata['source']}: {doc.page_content[:80]}...")
    print()


def rag_with_lcel():
    """RAG using LCEL (modern approach)"""
    print("=== RAG with LCEL ===\n")
    
    # Create documents
    documents = create_sample_documents()
    
    # Setup
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # Format documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context:
    
    {context}
    
    Question: {question}
    
    Answer:""")
    
    # Build chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Query
    query = "What is machine learning?"
    answer = rag_chain.invoke(query)
    
    print(f"Query: {query}\n")
    print(f"Answer: {answer}\n")


def rag_with_sources():
    """RAG that returns sources with answers"""
    print("=== RAG with Source Citations ===\n")
    
    documents = create_sample_documents()
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # Custom chain that preserves sources
    def format_docs_with_sources(docs):
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(f"Source {i} ({doc.metadata['source']}):\n{doc.page_content}")
        return "\n\n".join(formatted)
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based on the context below. Cite your sources by mentioning "Source 1", "Source 2", etc.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer (with citations):""")
    
    rag_chain = (
        {"context": retriever | format_docs_with_sources, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    query = "What programming languages and frameworks are mentioned?"
    answer = rag_chain.invoke(query)
    
    print(f"Query: {query}\n")
    print(f"Answer:\n{answer}\n")


def streaming_rag():
    """RAG with streaming responses"""
    print("=== Streaming RAG ===\n")
    
    documents = create_sample_documents()
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    prompt = ChatPromptTemplate.from_template("""
    Based on this context, answer the question:
    
    {context}
    
    Question: {question}
    Answer:""")
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    query = "Explain AI and machine learning"
    
    print(f"Query: {query}\n")
    print("Answer: ", end="", flush=True)
    
    for chunk in rag_chain.stream(query):
        print(chunk, end="", flush=True)
    
    print("\n")


def mmr_retrieval():
    """Maximum Marginal Relevance for diverse results"""
    print("=== MMR Retrieval (Diverse Results) ===\n")
    
    documents = create_sample_documents()
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    query = "programming"
    
    # Standard similarity search
    print("Standard Similarity Search:")
    similar_docs = vectorstore.similarity_search(query, k=3)
    for doc in similar_docs:
        print(f"  - {doc.metadata['source']}")
    
    # MMR search (more diverse)
    print("\nMMR Search (more diverse):")
    mmr_docs = vectorstore.max_marginal_relevance_search(query, k=3)
    for doc in mmr_docs:
        print(f"  - {doc.metadata['source']}")
    print()


def metadata_filtering():
    """Filter retrieval by metadata"""
    print("=== Metadata Filtering ===\n")
    
    documents = create_sample_documents()
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    # Retriever with filter
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2, "filter": {"topic": "AI"}}
    )
    
    query = "Tell me about technology"
    docs = retriever.get_relevant_documents(query)
    
    print(f"Query: {query}")
    print(f"Filter: topic='AI'\n")
    print("Results:")
    for doc in docs:
        print(f"  - {doc.metadata['source']} (topic: {doc.metadata['topic']})")
        print(f"    {doc.page_content[:80]}...\n")


if __name__ == "__main__":
    print("RAG Demo\n")
    print("=" * 60 + "\n")
    
    try:
        print("Make sure you have pulled the embedding model:")
        print("  ollama pull nomic-embed-text\n")
        print("=" * 60 + "\n")
        
        text_splitting_demo()
        basic_rag_chain()
        rag_with_lcel()
        rag_with_sources()
        streaming_rag()
        mmr_retrieval()
        metadata_filtering()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("  1. Run: ollama pull nomic-embed-text")
        print("  2. Run: ollama pull llama3.2")
        print("  3. Ensure Ollama is running: ollama serve")
