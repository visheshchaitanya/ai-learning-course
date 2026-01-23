"""
Lesson 4 Solution: Semantic FAQ System
"""

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json
import os


SIMILARITY_THRESHOLD = 0.5  # Minimum similarity (distance threshold)


def load_faqs(filepath: str) -> list[dict]:
    """Load FAQ data from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def create_vectorstore(faqs: list[dict], persist_dir: str = "./faq_db"):
    """Create vector store from FAQs"""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Convert FAQs to documents
    documents = []
    for faq in faqs:
        doc = Document(
            page_content=faq['question'],
            metadata={
                'answer': faq['answer'],
                'category': faq['category'],
                'tags': ','.join(faq['tags'])
            }
        )
        documents.append(doc)
    
    # Create and persist vector store
    vectorstore = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=persist_dir
    )
    
    return vectorstore


def search_faq(vectorstore, query: str, category: str = None, k: int = 3):
    """Search for similar FAQs"""
    # Build filter if category provided
    filter_dict = {"category": category} if category else None
    
    # Search with scores
    results = vectorstore.similarity_search_with_score(
        query,
        k=k,
        filter=filter_dict
    )
    
    # Filter by threshold (ChromaDB uses distance, lower is better)
    filtered_results = [(doc, score) for doc, score in results if score < SIMILARITY_THRESHOLD]
    
    return filtered_results


def display_results(query: str, results: list):
    """Display search results nicely"""
    print("\n" + "=" * 60)
    print(f"Query: {query}")
    print("=" * 60 + "\n")
    
    if not results:
        print("❌ No good matches found. Try rephrasing your question.\n")
        return
    
    # Display top result
    top_doc, top_score = results[0]
    similarity_pct = max(0, (1 - top_score) * 100)  # Convert distance to similarity
    
    print(f"🎯 Top Match ({similarity_pct:.0f}% similar):")
    print(f"Q: {top_doc.page_content}")
    print(f"A: {top_doc.metadata['answer']}")
    print(f"Category: {top_doc.metadata['category']}")
    
    # Display other matches
    if len(results) > 1:
        print("\n📋 Other similar questions:")
        for doc, score in results[1:]:
            similarity_pct = max(0, (1 - score) * 100)
            print(f"  • {doc.page_content} ({similarity_pct:.0f}%)")
    
    print()


def add_faq(vectorstore, question: str, answer: str, category: str, tags: list):
    """Add a new FAQ to the vector store"""
    doc = Document(
        page_content=question,
        metadata={
            'answer': answer,
            'category': category,
            'tags': ','.join(tags)
        }
    )
    
    vectorstore.add_documents([doc])


def list_categories(faqs: list[dict]) -> list[str]:
    """Get unique categories from FAQs"""
    categories = set()
    for faq in faqs:
        categories.add(faq['category'])
    return sorted(categories)


def main():
    """Main FAQ system"""
    print("=" * 60)
    print("Semantic FAQ System")
    print("=" * 60 + "\n")
    
    # Load FAQs
    faq_file = "data/faq.json"
    
    if not os.path.exists(faq_file):
        print(f"Error: {faq_file} not found!")
        print("Make sure you're running from the lesson4-embeddings directory")
        return
    
    print("Loading FAQs...")
    faqs = load_faqs(faq_file)
    print(f"Loaded {len(faqs)} FAQs\n")
    
    # Create or load vector store
    persist_dir = "./faq_vectorstore"
    
    print("Setting up vector store...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    if os.path.exists(persist_dir):
        print("Loading existing vector store...")
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
    else:
        print("Building new vector store (this may take a moment)...")
        vectorstore = create_vectorstore(faqs, persist_dir)
    
    print("✅ FAQ System Ready!\n")
    
    # Show available categories
    categories = list_categories(faqs)
    print(f"Categories: {', '.join(categories)}\n")
    
    print("Commands:")
    print("  /categories - Show all categories")
    print("  /filter <category> - Filter by category")
    print("  /clear - Clear filter")
    print("  /add - Add new FAQ")
    print("  /quit - Exit\n")
    print("=" * 60 + "\n")
    
    # Main loop
    active_filter = None
    
    while True:
        try:
            # Show active filter
            filter_text = f" [Filter: {active_filter}]" if active_filter else ""
            query = input(f"Ask a question{filter_text}: ").strip()
            
            if not query:
                continue
            
            if query == "/quit":
                print("Goodbye!")
                break
            
            elif query == "/categories":
                print(f"\nCategories: {', '.join(categories)}\n")
                continue
            
            elif query.startswith("/filter"):
                parts = query.split(maxsplit=1)
                if len(parts) > 1:
                    active_filter = parts[1]
                    if active_filter not in categories:
                        print(f"Warning: '{active_filter}' is not a known category")
                    print(f"✓ Filtering by category: {active_filter}\n")
                else:
                    print("Usage: /filter <category>\n")
                continue
            
            elif query == "/clear":
                active_filter = None
                print("✓ Filter cleared\n")
                continue
            
            elif query == "/add":
                print("\n📝 Add New FAQ:")
                new_q = input("Question: ").strip()
                new_a = input("Answer: ").strip()
                new_c = input("Category: ").strip()
                new_t = input("Tags (comma-separated): ").strip().split(',')
                new_t = [t.strip() for t in new_t if t.strip()]
                
                if new_q and new_a:
                    add_faq(vectorstore, new_q, new_a, new_c, new_t)
                    print("✅ FAQ added!\n")
                else:
                    print("❌ Question and answer are required\n")
                continue
            
            # Search and display results
            results = search_faq(vectorstore, query, active_filter, k=3)
            display_results(query, results)
            
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
        print("  2. Ensure Ollama is running: ollama serve")
        print("  3. Run from lesson4-embeddings directory")
