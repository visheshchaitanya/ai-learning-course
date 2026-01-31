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
import traceback


# TODO: Implement Wikipedia search tool
@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about a topic."""
    # TODO: Implement Wikipedia search
    # Use wikipedia-api library or web scraping
    try:
        import wikipedia
        wikipedia.set_lang("en")
        result = wikipedia.summary(query, sentences=3, auto_suggest=True)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        # Return first option from disambiguation
        return wikipedia.summary(e.options[0], sentences=3)
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for: {query}"
    except Exception as e:
        return f"Wikipedia error: {str(e)}"


# TODO: Implement calculator tool
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    # TODO: Implement safe calculation
    try:
        allowed = set('0123456789+-*/(). ')
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters"
        result = eval(expression)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {str(e)}"


# TODO: Implement file writer tool
@tool
def write_to_file(filename: str, content: str) -> str:
    """Write content to a text file."""
    # TODO: Implement file writing
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {filename}"
    except Exception as e:
        return f"Error: {str(e)}"


def create_research_agent():
    """Create the research agent"""
    # TODO: Setup LLM
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # TODO: Define tools list
    tools = [search_wikipedia, calculator, write_to_file]
    
    # TODO: Create ReAct prompt
    # Use the standard ReAct format
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

IMPORTANT: After you receive an Observation, you MUST either:
1. Provide a Final Answer if you have enough information
2. Take another Action if you need more information

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
    prompt = PromptTemplate.from_template(template)
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
)
    # TODO: Create agent and executor
    return agent_executor


def main():
    """Main research agent interface"""
    print("=" * 60)
    print("Research Agent")
    print("=" * 60 + "\n")
    
    # TODO: Create agent
    agent_executor = create_research_agent()
    
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
            result = agent_executor.invoke({"input": query})
            print(f"\n✅ Answer: {result['output']}\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
