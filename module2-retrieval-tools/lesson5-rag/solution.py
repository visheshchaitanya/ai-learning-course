"""
Lesson 5 Solution: Document Q&A System
"""

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
import os


def load_documents(directory: str):
    """Load all PDF documents from directory"""
    # Try PDF first, fall back to text files
    try:
        loader = DirectoryLoader(
            directory,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        documents = loader.load()
        if documents:
            return documents
    except:
        pass
    
    # Fallback to text files
    loader = DirectoryLoader(
        directory,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    return loader.load()


def chunk_documents(documents, chunk_size=1000, overlap=200):
    """Split documents into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    return splitter.split_documents(documents)


def create_vectorstore(chunks, persist_dir="./rag_db"):
    """Create or load vector store"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    if os.path.exists(persist_dir):
        print("Loading existing vector store...")
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
    else:
        print("Building new vector store...")
        vectorstore = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=persist_dir
        )
    
    return vectorstore


def format_docs(docs):
    """Format documents for context"""
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = os.path.basename(doc.metadata.get('source', 'Unknown'))
        page = doc.metadata.get('page', 'N/A')
        formatted.append(
            f"[Source {i}: {source}, page {page}]\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


def create_rag_chain(vectorstore, llm):
    """Create RAG chain with LCEL"""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    prompt = ChatPromptTemplate.from_template("""
Answer the question based on the following context. If the answer is not in the context, say "I don't have enough information to answer that question."

Cite sources by mentioning [Source 1], [Source 2], etc.

Context:
{context}

Question: {question}

Answer:""")
    
    rag_chain = (
        {"context": retriever | format_docs, "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever


def display_sources(docs):
    """Display source documents nicely"""
    if not docs:
        return
    
    print("\nSources:")
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        print(f"  📄 {os.path.basename(source)} (page {page})")
        excerpt = doc.page_content[:150].replace('\n', ' ')
        print(f"     \"{excerpt}...\"\n")


def create_sample_documents():
    """Create sample documents if none exist"""
    docs_dir = "documents"
    os.makedirs(docs_dir, exist_ok=True)
    
    sample_file = os.path.join(docs_dir, "sample.txt")
    if not os.path.exists(sample_file):
        with open(sample_file, "w") as f:
            f.write("""
# AI and Machine Learning Guide

## Introduction
Artificial Intelligence (AI) is the simulation of human intelligence by machines. Machine Learning (ML) is a subset of AI that enables systems to learn from data.

## Key Concepts
- Supervised Learning: Learning from labeled data
- Unsupervised Learning: Finding patterns in unlabeled data
- Deep Learning: Neural networks with multiple layers
- Natural Language Processing: Understanding human language

## Applications
AI and ML are used in:
- Healthcare: Disease diagnosis and drug discovery
- Finance: Fraud detection and algorithmic trading
- Transportation: Self-driving cars
- Entertainment: Recommendation systems

## Future Trends
The future of AI includes more advanced natural language understanding, better computer vision, and more ethical AI systems.
""")
        print(f"Created sample document: {sample_file}")


def main():
    """Main Q&A system"""
    print("=" * 60)
    print("Document Q&A System")
    print("=" * 60 + "\n")
    
    docs_dir = "documents"
    
    # Create sample if needed
    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        print("No documents found. Creating sample document...\n")
        create_sample_documents()
    
    # Load documents
    print("Loading documents...")
    try:
        documents = load_documents(docs_dir)
        print(f"Loaded {len(documents)} document(s)\n")
    except Exception as e:
        print(f"Error loading documents: {e}")
        return
    
    # Chunk documents
    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks\n")
    
    # Create vector store
    print("Creating vector store...")
    vectorstore = create_vectorstore(chunks)
    print("✅ Vector store ready!\n")
    
    # Create LLM and chain
    llm = ChatOllama(model="llama3.2", temperature=0)
    rag_chain, retriever = create_rag_chain(vectorstore, llm)
    
    # Setup conversation memory
    memory = ConversationBufferWindowMemory(k=3, return_messages=True)
    
    print("=" * 60)
    print("Ask questions about your documents")
    print("Commands: /quit, /clear (clear history)\n")
    
    while True:
        try:
            query = input("Ask a question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['/quit', 'quit']:
                print("Goodbye!")
                break
            
            if query.lower() == '/clear':
                memory.clear()
                print("✓ Conversation history cleared\n")
                continue
            
            # Get answer
            print("\nThinking...\n")
            answer = rag_chain.invoke(query)
            
            # Get source documents
            source_docs = retriever.get_relevant_documents(query)
            
            # Display answer
            print(f"Answer:\n{answer}\n")
            
            # Display sources
            display_sources(source_docs)
            
            # Update memory
            memory.save_context({"input": query}, {"output": answer})
            
            print("=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure to:")
        print("  1. Run: ollama pull nomic-embed-text")
        print("  2. Run: ollama pull llama3.2")
        print("  3. Ensure Ollama is running")
