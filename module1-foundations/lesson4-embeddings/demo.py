"""
Lesson 4 Demo: Embeddings and Vector Search
"""

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import numpy as np


def basic_embeddings():
    """Generate embeddings with Ollama"""
    print("=== Basic Embeddings ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Embed a single text
    text = "Machine learning is fascinating"
    vector = embeddings.embed_query(text)
    
    print(f"Text: {text}")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")
    print()


def cosine_similarity_demo():
    """Calculate similarity between texts"""
    print("=== Cosine Similarity ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Embed multiple texts
    texts = [
        "I love dogs",
        "Puppies are adorable",
        "Cars are fast"
    ]
    
    vectors = [embeddings.embed_query(text) for text in texts]
    
    # Calculate cosine similarity
    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    print("Similarity scores:")
    print(f"'{texts[0]}' vs '{texts[1]}': {cosine_sim(vectors[0], vectors[1]):.3f}")
    print(f"'{texts[0]}' vs '{texts[2]}': {cosine_sim(vectors[0], vectors[2]):.3f}")
    print(f"'{texts[1]}' vs '{texts[2]}': {cosine_sim(vectors[1], vectors[2]):.3f}")
    print()


def chromadb_basics():
    """Store and search with ChromaDB"""
    print("=== ChromaDB Basics ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Sample documents
    texts = [
        "Python is a programming language",
        "JavaScript is used for web development",
        "Machine learning uses algorithms to learn from data",
        "Deep learning is a subset of machine learning",
        "Cats are independent animals",
        "Dogs are loyal companions"
    ]
    
    # Create vector store
    vectorstore = Chroma.from_texts(texts, embeddings)
    
    # Search
    query = "Tell me about AI"
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"Query: {query}\n")
    print("Top 3 results:")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content}")
    print()


def chromadb_with_scores():
    """Search with similarity scores"""
    print("=== ChromaDB with Scores ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    texts = [
        "The weather is sunny today",
        "It's raining outside",
        "Python programming is fun",
        "I enjoy coding in Python"
    ]
    
    vectorstore = Chroma.from_texts(texts, embeddings)
    
    query = "programming languages"
    results = vectorstore.similarity_search_with_score(query, k=4)
    
    print(f"Query: {query}\n")
    print("Results with scores (lower = more similar):")
    for doc, score in results:
        print(f"Score: {score:.3f} | {doc.page_content}")
    print()


def chromadb_with_metadata():
    """Use metadata for filtering"""
    print("=== ChromaDB with Metadata ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Documents with metadata
    documents = [
        Document(page_content="Python is great for data science", metadata={"category": "programming", "language": "python"}),
        Document(page_content="JavaScript powers the web", metadata={"category": "programming", "language": "javascript"}),
        Document(page_content="Dogs are loyal pets", metadata={"category": "animals", "type": "mammal"}),
        Document(page_content="Cats are independent", metadata={"category": "animals", "type": "mammal"}),
    ]
    
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    # Search with filter
    query = "pets"
    results = vectorstore.similarity_search(
        query,
        k=2,
        filter={"category": "animals"}
    )
    
    print(f"Query: {query} (filtered by category='animals')\n")
    for doc in results:
        print(f"- {doc.page_content}")
        print(f"  Metadata: {doc.metadata}")
    print()


def persistent_chromadb():
    """Persist ChromaDB to disk"""
    print("=== Persistent ChromaDB ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    persist_dir = "./chroma_demo_db"
    
    # Create and persist
    texts = ["First document", "Second document", "Third document"]
    vectorstore = Chroma.from_texts(
        texts,
        embeddings,
        persist_directory=persist_dir
    )
    
    print(f"Created vector store with {len(texts)} documents")
    print(f"Persisted to: {persist_dir}")
    
    # Load existing
    loaded_vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    
    results = loaded_vectorstore.similarity_search("document", k=1)
    print(f"Loaded and searched: {results[0].page_content}")
    
    # Cleanup
    import shutil
    shutil.rmtree(persist_dir)
    print(f"Cleaned up {persist_dir}\n")


def faiss_demo():
    """Fast similarity search with FAISS"""
    print("=== FAISS Demo ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    texts = [
        "Artificial intelligence is transforming industries",
        "Machine learning models need training data",
        "Neural networks mimic the human brain",
        "Pizza is a popular food",
        "Pasta comes from Italy"
    ]
    
    # Create FAISS index
    vectorstore = FAISS.from_texts(texts, embeddings)
    
    query = "AI and ML"
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"Query: {query}\n")
    print("Top 3 results:")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content}")
    print()


def chunking_strategies():
    """Different text splitting approaches"""
    print("=== Chunking Strategies ===\n")
    
    # Sample long text
    text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals.
    
    Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.
    
    Deep learning is a subset of machine learning that uses neural networks with multiple layers to progressively extract higher-level features from raw input.
    
    Natural language processing (NLP) is a branch of AI that helps computers understand, interpret and manipulate human language.
    """
    
    # Recursive splitter (recommended)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len
    )
    
    chunks = splitter.split_text(text)
    
    print(f"Original text length: {len(text)} characters")
    print(f"Number of chunks: {len(chunks)}\n")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} ({len(chunk)} chars):")
        print(chunk.strip()[:80] + "...")
        print()


def semantic_search_example():
    """Complete semantic search workflow"""
    print("=== Complete Semantic Search ===\n")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Knowledge base
    knowledge = [
        "The Eiffel Tower is located in Paris, France",
        "The Great Wall of China is over 13,000 miles long",
        "The Taj Mahal was built in the 17th century in India",
        "Machu Picchu is an ancient Incan city in Peru",
        "The Colosseum is an ancient amphitheater in Rome"
    ]
    
    # Create vector store
    vectorstore = Chroma.from_texts(knowledge, embeddings)
    
    # Multiple queries
    queries = [
        "Where is the Eiffel Tower?",
        "Tell me about ancient structures",
        "What's in South America?"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        results = vectorstore.similarity_search(query, k=2)
        print("Answers:")
        for doc in results:
            print(f"  • {doc.page_content}")
        print()


if __name__ == "__main__":
    print("Embeddings Demo\n")
    print("=" * 60 + "\n")
    
    try:
        # Pull embedding model first
        print("Note: Make sure to pull the embedding model first:")
        print("  ollama pull nomic-embed-text\n")
        print("=" * 60 + "\n")
        
        basic_embeddings()
        cosine_similarity_demo()
        chromadb_basics()
        chromadb_with_scores()
        chromadb_with_metadata()
        persistent_chromadb()
        faiss_demo()
        chunking_strategies()
        semantic_search_example()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to:")
        print("  1. Run: ollama pull nomic-embed-text")
        print("  2. Ensure Ollama is running: ollama serve")
