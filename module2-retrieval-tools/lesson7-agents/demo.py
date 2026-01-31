"""
Lesson 7 Demo: Agents with ReAct
"""

from langchain_community.chat_models import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


# Define tools
@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions like '2 + 2' or '10 * 5'."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def word_counter(text: str) -> str:
    """Count the number of words in a text."""
    words = len(text.split())
    return f"Word count: {words}"


@tool
def text_reverser(text: str) -> str:
    """Reverse a given text string."""
    return f"Reversed: {text[::-1]}"


def basic_react_agent():
    """Basic ReAct agent with calculator"""
    print("=== Basic ReAct Agent ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [calculator]
    
    # ReAct prompt template
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
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    result = agent_executor.invoke({"input": "What is 25 * 4?"})
    print(f"\nFinal Answer: {result['output']}\n")


def multi_tool_agent():
    """Agent with multiple tools"""
    print("=== Multi-Tool Agent ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [calculator, word_counter, text_reverser]
    
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
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    result = agent_executor.invoke({
        "input": "How many words are in 'Hello world from LangChain'?"
    })
    print(f"\nFinal Answer: {result['output']}\n")


def agent_with_memory():
    """Agent that remembers conversation"""
    print("=== Agent with Memory ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [calculator]
    
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
    
    # First question
    result1 = agent_executor.invoke({"input": "What's 10 * 5?"})
    print(f"\nAnswer 1: {result1['output']}\n")
    
    # Follow-up question
    result2 = agent_executor.invoke({"input": "Now add 25 to that"})
    print(f"\nAnswer 2: {result2['output']}\n")


def error_handling_demo():
    """Demonstrate error handling"""
    print("=== Error Handling ===\n")
    
    @tool
    def divide(a: float, b: float) -> str:
        """Divide two numbers."""
        try:
            if b == 0:
                return "Error: Cannot divide by zero"
            return f"Result: {a / b}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    tools = [divide]
    
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
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
    
    # This will cause an error
    result = agent_executor.invoke({"input": "What is 10 divided by 0?"})
    print(f"\nFinal Answer: {result['output']}\n")


if __name__ == "__main__":
    print("Agents Demo\n")
    print("=" * 60 + "\n")
    
    try:
        print("Note: Agent execution can be slow with local models.\n")
        print("=" * 60 + "\n")
        
        basic_react_agent()
        multi_tool_agent()
        agent_with_memory()
        error_handling_demo()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
