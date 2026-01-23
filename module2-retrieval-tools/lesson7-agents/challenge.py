"""
Lesson 7 Challenge: Research Agent

Build an agent that can:
1. Search Wikipedia
2. Perform calculations
3. Write findings to files
"""

from langchain_community.chat_models import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


# TODO: Implement Wikipedia search tool
@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    # TODO: Implement Wikipedia search
    # You can use wikipedia-api library or web scraping
    # For now, return mock data
    return f"Mock Wikipedia result for: {query}"


# TODO: Implement calculator tool
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    # TODO: Implement safe calculation
    pass


# TODO: Implement file writer tool
@tool
def write_to_file(filename: str, content: str) -> str:
    """Write content to a text file."""
    # TODO: Implement file writing
    pass


def create_research_agent():
    """Create the research agent"""
    # TODO: Setup LLM
    # llm = ChatOllama(model="llama3.2", temperature=0)
    
    # TODO: Define tools list
    # tools = [search_wikipedia, calculator, write_to_file]
    
    # TODO: Create ReAct prompt
    # Use the standard ReAct format
    
    # TODO: Create agent and executor
    
    pass


def main():
    """Main research agent interface"""
    print("=" * 60)
    print("Research Agent")
    print("=" * 60 + "\n")
    
    # TODO: Create agent
    # agent_executor = create_research_agent()
    
    print("Example queries:")
    print("  - How old is the Eiffel Tower? Calculate how many decades.")
    print("  - Search for Python language and write summary to file.")
    print("  - What's the population of Tokyo? Calculate 2% growth over 10 years.\n")
    
    while True:
        try:
            query = input("\nQuery (or 'quit'): ").strip()
            
            if query.lower() == 'quit':
                break
            
            if not query:
                continue
            
            # TODO: Execute agent
            # result = agent_executor.invoke({"input": query})
            # print(f"\nAnswer: {result['output']}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
