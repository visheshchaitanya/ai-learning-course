"""
Lesson 5 Challenge: Document Q&A System

Build a system that:
1. Loads PDFs from documents/ folder
2. Chunks and embeds them
3. Answers questions with source citations
4. Maintains conversation history
"""

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
import os


def load_documents(directory: str):
    """Load all PDF documents from directory"""
    # TODO: Implement PDF loading
    # Use DirectoryLoader with PyPDFLoader
    # loader = DirectoryLoader(directory, glob="**/*.pdf", loader_cls=PyPDFLoader)
    # documents = loader.load()
    try:
        loader = DirectoryLoader(directory, glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        if documents:
            return documents
    except:
        pass
    return []


def chunk_documents(documents, chunk_size=1000, overlap=200):
    """Split documents into chunks"""
    # TODO: Implement chunking
    # Use RecursiveCharacterTextSplitter
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len
    )
    chunks = recursive_splitter.split_documents(documents)
    return chunks


def create_vectorstore(chunks, persist_dir="./rag_db"):
    """Create or load vector store"""
    # TODO: Create vector store with persistence if not already created
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    if not os.path.exists(persist_dir): 
        print("Building new vector store...")
        vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
    else:
        print("Loading existing vector store...")
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectorstore


def format_docs_with_metadata(docs):
    """Format documents with source information"""
    # TODO: Format each doc showing source and page number
    formatted_docs = []
    for doc in docs:
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        formatted_docs.append(f"Source: {source}, Page: {page}\n{doc.page_content}")
    return formatted_docs


def create_rag_chain(vectorstore, llm):
    """Create RAG chain with LCEL"""
    # TODO: Build RAG chain using LCEL
    # Include source citations in prompt
    # Use retriever with k=3
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based on the following context. If the answer is not in the context, say "I don't have enough information to answer that question."
    Cite sources by mentioning [Source 1], [Source 2], etc.
    Context: {context}
    Question: {question}
    Answer:""")
    rag_chain = (
        {"context": retriever | format_docs_with_metadata, "question": RunnablePassthrough()}
        | prompt 
        | llm
        | StrOutputParser())
    return rag_chain, retriever

def display_sources(docs):
    """Display source documents nicely"""
    # TODO: Print sources with document name and page
    print("\nSources:")
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        print(f"  📄 {os.path.basename(source)} (page {page})")
        print(f"     {doc.page_content[:100]}...\n")


def main():
    """Main Q&A system"""
    print("=" * 60)
    print("Document Q&A System")
    print("=" * 60 + "\n")
    
    docs_dir = "documents"
    
    # TODO: Check if documents directory exists
    if not os.path.exists(docs_dir):
        print(f"Error: {docs_dir}/ directory not found!")
        print("Create it and add some PDF files.")
        return
    
    # TODO: Load documents
    print("Loading documents...")
    documents = load_documents(docs_dir)
    print(f"Loaded {len(documents)} pages\n")
    
    # TODO: Chunk documents
    print("Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks\n")
    
    # TODO: Create vector store
    print("Creating vector store...")
    vectorstore = create_vectorstore(chunks)
    print("✅ Vector store ready!\n")
    
    # TODO: Create LLM and chain
    llm = ChatOllama(model="llama3.2", temperature=0)
    rag_chain = create_rag_chain(vectorstore, llm)[0]
    retriever = create_rag_chain(vectorstore, llm)[1]
    
    # TODO: Setup conversation memory
    memory = ConversationBufferWindowMemory(k=3)
    
    print("=" * 60)
    print("Ask questions about your documents (type 'quit' to exit)\n")
    
    while True:
        try:
            query = input("Ask a question: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'quit':
                print("Goodbye!")
                break
            
            # TODO: Get answer from RAG chain
            chunks = []
            for chunk in rag_chain.stream(query):
                chunks.append(chunk)
                print(chunk, end="", flush=True)
            print()
            
            # TODO: Get source documents    
            source_docs = retriever.invoke(query)
            
            # TODO: Display answer
            print()
            
            # TODO: Display sources
            display_sources(source_docs)
            
            # TODO: Update conversation memory
            memory.save_context({"input": query}, {"output": "".join(chunks)})
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(traceback.format_exc())
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
