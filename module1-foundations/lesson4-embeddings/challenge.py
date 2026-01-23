"""
Lesson 4 Challenge: Semantic FAQ System

Build an FAQ system that:
1. Loads Q&A pairs from JSON
2. Embeds questions and stores in ChromaDB
3. Finds similar questions for user queries
4. Returns answers with similarity scores
5. Supports category filtering
"""
from typing import Any

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json
import os
import chromadb
from chromadb.config import Settings

# When creating your client, add:
client = chromadb.Client(Settings(anonymized_telemetry=False))
DISTANCE_THRESHOLD = 300  # Maximum distance to show result (lower = more similar)


def load_faqs(filepath: str) -> list[dict]:
    """Load FAQ data from JSON file"""
    # TODO: Load and return FAQ data
    with open(filepath, 'r') as f:
        return json.load(f)


def create_vectorstore(faqs: list[dict], persist_dir: str = "./faq_db"):
    """Create vector store from FAQs"""
    # TODO: Create embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # TODO: Convert FAQs to documents with metadata
    # Each document should have:
    # - page_content: the question
    # - metadata: answer, category, tags
    
    documents = []
    for faq in faqs:
        doc = Document(
            page_content=faq['question'],
            metadata={
             'answer': faq['answer'],
             'category': faq['category'],
             'tags': ','.join(faq['tags'])
        })
        documents.append(doc)
    
    # TODO: Create and persist vector store
    # vectorstore = Chroma.from_documents(...)
    vectorstore = Chroma.from_documents(documents, embeddings, persist_directory=persist_dir)
    return vectorstore


def search_faq(vectorstore, query: str, category: str = None, k: int = 3) -> list[tuple[Any, Any]]:
    """Search for similar FAQs"""
    # TODO: Perform similarity search with optional category filter
    
    # If category provided, use filter
    # results = vectorstore.similarity_search_with_score(...)
    if category:
        results = vectorstore.similarity_search_with_score(query, k=k, filter={"category": category})
    else:
        results = vectorstore.similarity_search_with_score(query, k=k)
    
    # TODO: Filter by similarity threshold
    # ChromaDB returns squared L2 distance (lower = more similar)
    # Filter out results with distance above threshold
    filtered_results = [(doc, distance) for doc, distance in results if distance <= DISTANCE_THRESHOLD]
    return filtered_results


def display_results(query: str, results: list):
    """Display search results nicely"""
    print("\n" + "=" * 60)
    print(f"Query: {query}")
    print("=" * 60 + "\n")
    
    if not results:
        print("❌ No good matches found. Try rephrasing your question.\n")
        return
    
    # TODO: Display top result prominently
    # Show question, answer, and similarity score
    top_doc, top_distance = results[0]
    # Convert distance to similarity percentage (lower distance = higher similarity)
    # Use exponential decay: similarity = e^(-distance/scale)
    import math
    scale = 100  # Adjust based on your distance range
    similarity_pct = math.exp(-top_distance / scale) * 100
    print(f"🎯 Top Match ({similarity_pct:.0f}% similar, distance: {top_distance:.1f}):")
    print(f"Q: {top_doc.page_content}")
    print(f"A: {top_doc.metadata['answer']}")
    print(f"Category: {top_doc.metadata['category']}")
    # TODO: Display other similar questions
    if len(results) > 1:
        print("\n📋 Other similar questions:")
        for doc, distance in results[1:]:
            similarity_pct = math.exp(-distance / scale) * 100
            print(f"  • {doc.page_content} ({similarity_pct:.0f}%, dist: {distance:.1f})")
    print()


def add_faq(vectorstore, question: str, answer: str, category: str, tags: list):
    """Add a new FAQ to the vector store"""
    # TODO: Create document and add to vectorstore
    # Note: ChromaDB supports adding documents dynamically
    doc = Document(
        page_content=question,
        metadata={'answer': answer, 'category': category, 'tags': tags}
    )
    vectorstore.add_documents([doc])


def list_categories(faqs: list[dict]) -> list[str]:
    """Get unique categories from FAQs"""
    # TODO: Extract unique categories
    categories = set()
    for faq in faqs:
        categories.add(faq['category'])
    return sorted(categories)


def main():
    """Main FAQ system"""
    print("=" * 60)
    print("Semantic FAQ System")
    print("=" * 60 + "\n")
    
    # TODO: Load FAQs
    faq_file = "data/faq.json"
    
    if not os.path.exists(faq_file):
        print(f"Error: {faq_file} not found!")
        return
    
    print("Loading FAQs...")
    faqs = load_faqs(faq_file)
    print(f"Loaded {len(faqs)} FAQs\n")
    
    # TODO: Create or load vector store
    persist_dir = "./faq_vectorstore"
    
    print("Creating vector store...")
    # Check if already exists
    if os.path.exists(persist_dir):
        print("Loading existing vector store...")
        # TODO: Load existing
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        print("Building new vector store...")
        # TODO: Create new
        vectorstore = create_vectorstore(faqs, persist_dir)
    
    print("✅ FAQ System Ready!\n")
    
    # TODO: Show available categories
    categories = list_categories(faqs)
    print(f"Categories: {', '.join(categories)}\n")
    
    print("Commands:")
    print("  /categories - Show all categories")
    print("  /filter <category> - Filter by category")
    print("  /add - Add new FAQ")
    print("  /quit - Exit\n")
    print("=" * 60 + "\n")
    
    # Main loop
    active_filter = None
    
    while True:
        try:
            query = input("Ask a question: ").strip()
            
            if not query:
                continue
            
            if query == "/quit":
                print("Goodbye!")
                break
            
            elif query == "/categories":
                print(f"\nCategories: {', '.join(categories)}\n")
                continue
            
            elif query.startswith("/filter"):
                # TODO: Set category filter
                parts = query.split(maxsplit=1)
                if len(parts) > 1:
                    active_filter = parts[1]
                    print(f"Filtering by category: {active_filter}\n")
                else:
                    active_filter = None
                    print("Filter cleared\n")
                continue
            
            elif query == "/add":
                # TODO: Add new FAQ interactively
                print("\nAdd New FAQ:")
                new_q = input("Question: ").strip()
                new_a = input("Answer: ").strip()
                new_c = input("Category: ").strip()
                new_t = input("Tags (comma-separated): ").strip().split(',')
                new_t = [t.strip() for t in new_t]
                
                add_faq(vectorstore, new_q, new_a, new_c, new_t)
                print("✅ FAQ added!\n")
                continue
            
            # TODO: Search and display results
            results = search_faq(vectorstore, query, active_filter)
            display_results(query, results)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
