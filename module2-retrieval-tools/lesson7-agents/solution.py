"""
Lesson 7 Solution: Research Agent
"""

from langchain_community.chat_models import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    try:
        import wikipedia
        result = wikipedia.summary(query, sentences=3)
        return result
    except:
        # Fallback if wikipedia library not installed
        mock_data = {
            "eiffel tower": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It was completed in 1889 and named after engineer Gustave Eiffel.",
            "python": "Python is a high-level, interpreted programming language created by Guido van Rossum and first released in 1991. It emphasizes code readability and simplicity.",
            "tokyo": "Tokyo is the capital and most populous city of Japan. As of 2023, the city has an estimated population of approximately 14 million people."
        }
        query_lower = query.lower()
        for key in mock_data:
            if key in query_lower:
                return mock_data[key]
        return f"No information found for: {query}"


@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions like '2 + 2' or '10 * 5'."""
    try:
        # Basic safety check
        allowed = set('0123456789+-*/(). ')
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters"
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def write_to_file(filename: str, content: str) -> str:
    """Write content to a text file."""
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {filename}"
    except Exception as e:
        return f"Error: {str(e)}"


def create_research_agent():
    """Create the research agent"""
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    tools = [search_wikipedia, calculator, write_to_file]
    
    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
    
    prompt = PromptTemplate.from_template(template)
    
    memory = ConversationBufferMemory(memory_key="chat_history")
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    return agent_executor


def main():
    """Main research agent interface"""
    print("=" * 60)
    print("Research Agent")
    print("=" * 60 + "\n")
    
    print("Creating agent...")
    agent_executor = create_research_agent()
    print("✅ Agent ready!\n")
    
    print("Example queries:")
    print("  - How old is the Eiffel Tower? Calculate how many decades.")
    print("  - Search for Python language and write summary to file.")
    print("  - What's 25 * 4 plus 10?\n")
    print("Commands: 'quit' to exit\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if query.lower() == 'quit':
                print("Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n" + "=" * 60)
            result = agent_executor.invoke({"input": query})
            print("=" * 60)
            print(f"\n✅ Answer: {result['output']}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
        print("\nOptional: Install wikipedia library:")
        print("  pip install wikipedia-api")
