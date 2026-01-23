# Lesson 2: LangChain Basics

## Theory

### What is LangChain?

LangChain is a framework for building applications powered by language models. It provides:
- **Abstractions** for working with LLMs (prompts, chains, agents)
- **Composability** to build complex workflows from simple components
- **Integrations** with many LLM providers, vector stores, and tools
- **Production-ready** patterns for memory, callbacks, and error handling

### Core Concepts

#### 1. PromptTemplates
Templates that format inputs into prompts for LLMs:
```python
from langchain.prompts import PromptTemplate

template = PromptTemplate.from_template("Tell me a joke about {topic}")
prompt = template.format(topic="programming")
```

#### 2. Chat Models
LangChain wrappers around LLMs that handle message formatting:
```python
from langchain_community.chat_models import ChatOllama

llm = ChatOllama(model="llama3.2")
response = llm.invoke("Hello!")
```

#### 3. Chains (Legacy)
Sequential operations that pass outputs to inputs:
- **LLMChain**: Prompt → LLM → Output
- **SequentialChain**: Chain multiple operations
- Being replaced by LCEL (LangChain Expression Language)

#### 4. LCEL (LangChain Expression Language)
Modern way to compose chains using the `|` operator:
```python
chain = prompt | llm | output_parser
result = chain.invoke({"topic": "AI"})
```

**Understanding the Flow:**
- **Prompt**: A template that formats input variables into the actual prompt sent to the LLM
  - Example: `"Tell me about {topic}"` → `"Tell me about AI"`
- **LLM**: The model itself that takes the formatted prompt and generates a response
- **Output Parser**: Transforms raw LLM text into structured format (string, JSON, Pydantic object, etc.)

**Why Use LCEL?**
- **Cleaner syntax**: `prompt | llm | parser` instead of verbose class instantiation
- **Automatic features**: Streaming, async, parallel execution, retries work out of the box
- **Composability**: Easily chain/combine components without boilerplate
- **Type safety**: Better IDE support and error checking

**Benefits of LCEL:**
- Automatic streaming support
- Async by default
- Parallel execution
- Built-in retries and fallbacks
- Better type safety

#### 5. Output Parsers
Convert LLM text output into structured data:
- **StrOutputParser**: Returns plain string
- **JsonOutputParser**: Parses JSON
- **PydanticOutputParser**: Validates with Pydantic models

### LCEL Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `\|` | Pipe output to next component | `prompt \| llm` |
| `RunnableParallel` | Run multiple chains in parallel | `{"a": chain1, "b": chain2}` |
| `RunnableLambda` | Custom Python function | `RunnableLambda(lambda x: x.upper())` |
| `RunnablePassthrough` | Pass input unchanged | Used for routing |

#### Chaining Chains: itemgetter with Named Parameters

When using `RunnableParallel` with named parameters, you often need to **chain chains** to extract/transform data before passing it to your existing chain:

```python
from operator import itemgetter

# Your existing chain
answer_chain = prompt | llm | parser

# Parallel execution with data extraction
parallel_chain = RunnableParallel(
    answer0=itemgetter("q0") | answer_chain,  # Extract q0, then run chain
    answer1=itemgetter("q1") | answer_chain,  # Extract q1, then run chain
)

# Input: {"q0": "What is AI?", "q1": "What is ML?"}
# itemgetter("q0") extracts "What is AI?" → passes to answer_chain
# itemgetter("q1") extracts "What is ML?" → passes to answer_chain
```

**Why needed:**
- `RunnableParallel` passes the entire input dict to each named parameter
- `itemgetter("key")` extracts just the value you need
- The `|` creates a mini-chain: extract → process
- Without it, your chain receives `{"q0": "...", "q1": "..."}` instead of just the string it expects

## Demo

See `demo.py` for complete examples covering:
1. Basic prompt templates with variables
2. Chat models with Ollama
3. Output parsers (string, JSON)
4. Legacy chain composition
5. LCEL syntax and composition
6. Streaming with LCEL
7. Parallel execution

### Quick Example

```python
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Define components
llm = ChatOllama(model="llama3.2")
prompt = ChatPromptTemplate.from_template("Write a haiku about {topic}")
parser = StrOutputParser()

# Compose with LCEL
chain = prompt | llm | parser

# Invoke
result = chain.invoke({"topic": "coding"})
print(result)

# Stream
for chunk in chain.stream({"topic": "coding"}):
    print(chunk, end="", flush=True)
```

## Challenge

Build a **Multi-Step Research Assistant** that:

1. Takes a research topic as input
2. Generates 3 specific research questions about the topic
3. Answers each question individually
4. Synthesizes all answers into a final summary

**Requirements:**
- Use LCEL to compose the chain
- Parse the 3 questions into a list (use string parsing or JSON)
- Use parallel execution to answer all 3 questions simultaneously
- Combine results into a final synthesis
- Add streaming output for the final summary

**Starter code in `challenge.py`**

**Example Output:**
```
Topic: Quantum Computing

Questions:
1. What are the fundamental principles of quantum computing?
2. What are the current limitations of quantum computers?
3. What are the most promising applications?

[Answers generated in parallel...]

Final Summary:
Quantum computing leverages superposition and entanglement...
```

## Resources

- [LangChain Docs](https://python.langchain.com/)
- [LCEL Guide](https://python.langchain.com/docs/expression_language/)
- [Prompt Templates](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Output Parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/)
