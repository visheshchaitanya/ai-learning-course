"""
Lesson 2 Demo: LangChain Basics
"""

from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
import json


def basic_prompt_template():
    """Simple prompt template with variables"""
    print("=== Basic Prompt Template ===\n")
    
    template = PromptTemplate.from_template(
        "You are a {profession}. Give advice about {topic} in one sentence."
    )
    
    prompt = template.format(profession="chef", topic="knife skills")
    print(f"Formatted prompt:\n{prompt}\n")


def chat_model_basics():
    """Using ChatOllama with LangChain"""
    print("=== Chat Model Basics ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0.7)
    
    # Direct invoke
    response = llm.invoke("Explain LangChain in one sentence.")
    print(f"Response: {response.content}\n")


def output_parsers_demo():
    """Different output parser types"""
    print("=== Output Parsers ===\n")
    
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # String parser
    prompt = ChatPromptTemplate.from_template("What is {concept}?")
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({"concept": "machine learning"})
    print(f"String output:\n{result}\n")
    
    # JSON parser
    json_prompt = ChatPromptTemplate.from_template(
        "Return a JSON object with 'name' and 'age' for a person named {name}. "
        "Only return valid JSON, nothing else."
    )
    json_chain = json_prompt | llm | JsonOutputParser()
    
    result = json_chain.invoke({"name": "Alice"})
    print(f"JSON output:\n{result}\n")


def lcel_basic_chain():
    """Basic LCEL chain composition"""
    print("=== LCEL Basic Chain ===\n")
    
    llm = ChatOllama(model="llama3.2")
    prompt = ChatPromptTemplate.from_template("Write a tagline for a {product}")
    parser = StrOutputParser()
    
    # Compose with | operator
    chain = prompt | llm | parser
    
    result = chain.invoke({"product": "AI-powered coffee maker"})
    print(f"Tagline: {result}\n")


def lcel_with_multiple_inputs():
    """LCEL chain with multiple input variables"""
    print("=== LCEL Multiple Inputs ===\n")
    
    llm = ChatOllama(model="llama3.2")
    prompt = ChatPromptTemplate.from_template(
        "Write a {length} {style} story about {topic}"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({
        "length": "short",
        "style": "sci-fi",
        "topic": "a robot learning to paint"
    })
    print(f"Story:\n{result}\n")


def streaming_with_lcel():
    """Streaming responses with LCEL"""
    print("=== Streaming with LCEL ===\n")
    
    llm = ChatOllama(model="llama3.2")
    prompt = ChatPromptTemplate.from_template("Explain {topic} in simple terms")
    
    chain = prompt | llm | StrOutputParser()
    
    print("Streaming response: ", end="", flush=True)
    for chunk in chain.stream({"topic": "neural networks"}):
        print(chunk, end="", flush=True)
    print("\n")


def parallel_execution():
    """Execute multiple chains in parallel"""
    print("=== Parallel Execution ===\n")
    
    llm = ChatOllama(model="llama3.2")
    
    # Create multiple chains
    joke_chain = (
        ChatPromptTemplate.from_template("Tell a joke about {topic}") 
        | llm 
        | StrOutputParser()
    )
    
    fact_chain = (
        ChatPromptTemplate.from_template("Give an interesting fact about {topic}") 
        | llm 
        | StrOutputParser()
    )
    
    # Run in parallel
    parallel_chain = RunnableParallel(
        joke=joke_chain,
        fact=fact_chain
    )
    
    result = parallel_chain.invoke({"topic": "Python programming"})
    print(f"Joke: {result['joke']}\n")
    print(f"Fact: {result['fact']}\n")


def custom_functions_in_chain():
    """Using custom Python functions in LCEL chains"""
    print("=== Custom Functions in Chain ===\n")
    
    llm = ChatOllama(model="llama3.2")
    
    # Custom function to uppercase
    def uppercase(text: str) -> str:
        return text.upper()
    
    # Custom function to add prefix
    def add_prefix(text: str) -> str:
        return f"🎯 RESULT: {text}"
    
    prompt = ChatPromptTemplate.from_template("Give a one-word answer: {question}")
    
    chain = (
        prompt 
        | llm 
        | StrOutputParser() 
        | RunnableLambda(uppercase)
        | RunnableLambda(add_prefix)
    )
    
    result = chain.invoke({"question": "What color is the sky?"})
    print(f"{result}\n")


def sequential_chain_example():
    """Multi-step chain where output feeds into next step"""
    print("=== Sequential Chain ===\n")
    
    llm = ChatOllama(model="llama3.2")
    
    # Step 1: Generate a topic
    topic_chain = (
        ChatPromptTemplate.from_template("Suggest one interesting {category} topic") 
        | llm 
        | StrOutputParser()
    )
    
    # Step 2: Write about the topic
    writing_chain = (
        ChatPromptTemplate.from_template("Write one sentence about: {topic}") 
        | llm 
        | StrOutputParser()
    )
    
    # Combine: generate topic, then write about it
    def run_sequential(category: str) -> str:
        topic = topic_chain.invoke({"category": category})
        print(f"Generated topic: {topic}")
        result = writing_chain.invoke({"topic": topic})
        return result
    
    result = run_sequential("science")
    print(f"Final output: {result}\n")


if __name__ == "__main__":
    print("LangChain Basics Demo\n")
    print("=" * 60 + "\n")
    
    try:
        basic_prompt_template()
        chat_model_basics()
        output_parsers_demo()
        lcel_basic_chain()
        lcel_with_multiple_inputs()
        streaming_with_lcel()
        parallel_execution()
        custom_functions_in_chain()
        sequential_chain_example()
        
        print("=" * 60)
        print("\nDemo completed! Now try the challenge.py")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Ollama is running and llama3.2 is pulled:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
