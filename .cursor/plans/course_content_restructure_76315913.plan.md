---
name: Course Content Restructure
overview: Comprehensive restructuring of lessons 12-20 with expanded README.md files, full demo implementations (150-250 lines), challenge boilerplates, and complete solutions. Focus on production-ready patterns with proper error handling and documentation.
todos:
  - id: lesson12
    content: "Complete Lesson 12: Advanced Agent Patterns (README, demo, challenge, solution)"
    status: completed
  - id: lesson13
    content: "Complete Lesson 13: MCP Basics (README, demo, challenge, solution)"
    status: completed
  - id: lesson14
    content: "Complete Lesson 14: MCP Servers (README, server, demo, client_demo, challenge, solution)"
    status: completed
  - id: lesson15
    content: "Complete Lesson 15: MCP Integration (README, demo, challenge, solution)"
    status: completed
  - id: lesson16
    content: "Complete Lesson 16: Deployment (README, api, demo, test_api, challenge, solution)"
    status: completed
  - id: lesson17
    content: "Complete Lesson 17: Multimodal AI (README, demo, challenge, solution)"
    status: completed
  - id: lesson18
    content: "Complete Lesson 18: Code Generation (README, demo, challenge, solution)"
    status: completed
  - id: lesson19
    content: "Complete Lesson 19: Advanced RAG (README, advanced_techniques, demo, challenge, solution)"
    status: completed
  - id: lesson20
    content: "Complete Lesson 20: Final Project (README, project_ideas, evaluation_rubric, templates)"
    status: completed
  - id: dependencies
    content: Update requirements.txt with new dependencies (wikipedia, pillow)
    status: completed
  - id: validation
    content: Test all demo.py files and verify completeness of all materials
    status: completed
---

# Course Content Restructuring: Lessons 12-20

## Overview

Expand and complete content for lessons 12-20, transforming minimal placeholders into comprehensive learning materials with working code examples, challenges, and solutions.

## Lessons to Restructure

### Module 3: Advanced Agents

#### **Lesson 12: Advanced Agent Patterns** 

[`module3-advanced-agents/lesson12-advanced-patterns/`](module3-advanced-agents/lesson12-advanced-patterns/)

**README.md Enhancements:**

- Expand self-reflection pattern with detailed workflow diagrams
- Add plan-and-execute pattern with ReWOO implementation details
- Include tree-of-thoughts exploration examples
- Add retry-with-feedback pattern for error recovery
- Include fallback chains for graceful degradation

**demo.py (200+ lines):**

- Demo 1: Self-reflection agent that critiques and improves outputs
- Demo 2: Plan-and-execute pattern with task decomposition
- Demo 3: Retry with feedback loop
- Demo 4: Fallback chain with multiple strategies
- Full LangGraph implementation with state management

**challenge.py:**

- Boilerplate for Code Review Agent
- State schema with code, critique, revision_count, quality_score
- Placeholder functions: generate_code(), critique_code(), revise_code(), check_quality()
- TODOs for implementing self-reflection loop

**solution.py (150+ lines):**

- Complete Code Review Agent with self-reflection
- Quality threshold checking (e.g., score > 0.8)
- Max iterations limit (e.g., 3 revisions)
- Detailed critique with specific improvement suggestions
- Working example with Python function generation

---

### Module 4: Production

#### **Lesson 13: MCP Basics**

[`module4-production/lesson13-mcp-basics/`](module4-production/lesson13-mcp-basics/)

**README.md Enhancements:**

- Detailed MCP architecture diagrams (client-server-transport)
- Protocol specifications and message formats
- Comparison with other integration patterns
- Security considerations and best practices
- Real-world use cases (IDE integrations, data connectors)

**demo.py (150+ lines):**

- Demo 1: Basic MCP client connecting to stdio server
- Demo 2: Listing available tools and resources
- Demo 3: Calling MCP tools programmatically
- Demo 4: Handling MCP resources (reading data)
- Error handling and connection management

**challenge.py:**

- Boilerplate for MCP filesystem client
- Functions: connect_to_server(), list_tools(), call_tool()
- TODOs for implementing file operations via MCP

**solution.py (120+ lines):**

- Complete MCP client for filesystem operations
- Natural language to MCP tool calls
- File reading, writing, listing via MCP
- Error handling and graceful disconnection

---

#### **Lesson 14: MCP Servers**

[`module4-production/lesson14-mcp-servers/`](module4-production/lesson14-mcp-servers/)

**README.md Enhancements:**

- Server lifecycle and initialization
- Tool registration patterns
- Resource provider implementation
- Request/response handling
- Deployment strategies (stdio, HTTP, SSE)

**server.py (200+ lines):**

- Complete example MCP server with multiple tools
- Calculator, file operations, data retrieval tools
- Resource providers for configuration and data
- Proper error handling and logging
- stdio transport implementation

**demo.py (150+ lines):**

- Demo 1: Simple MCP server with one tool
- Demo 2: Server with multiple tools and resources
- Demo 3: Server with error handling
- Demo 4: Testing server with client

**client_demo.py (100+ lines):**

- Client that connects to the example server
- Demonstrates all server capabilities
- Interactive CLI for testing tools

**challenge.py:**

- Boilerplate for TODO list MCP server
- Functions: add_task(), list_tasks(), complete_task(), delete_task()
- In-memory storage structure
- TODOs for implementing server registration

**solution.py (180+ lines):**

- Complete TODO list MCP server
- Persistent storage (JSON file)
- Full CRUD operations
- Client example for testing

---

#### **Lesson 15: MCP Integration**

[`module4-production/lesson15-mcp-integration/`](module4-production/lesson15-mcp-integration/)

**README.md Enhancements:**

- LangChain MCP integration patterns
- LangGraph workflows with MCP tools
- Multi-server orchestration
- Dynamic tool discovery and registration
- Performance considerations

**demo.py (200+ lines):**

- Demo 1: LangChain agent with MCP tools
- Demo 2: LangGraph workflow with MCP integration
- Demo 3: Multiple MCP servers in one workflow
- Demo 4: Dynamic tool loading from MCP servers
- Complete data pipeline example

**challenge.py:**

- Boilerplate for multi-server agent
- Filesystem, database, and API server stubs
- State schema for data pipeline
- TODOs for orchestrating multiple servers

**solution.py (200+ lines):**

- Complete multi-server MCP integration
- Agent that uses filesystem, database, and API servers
- Data pipeline: fetch → process → store
- Error handling across multiple servers
- LangGraph state management

---

#### **Lesson 16: Deployment**

[`module4-production/lesson16-deployment/`](module4-production/lesson16-deployment/)

**README.md Enhancements:**

- FastAPI best practices for AI applications
- Docker multi-stage builds
- Environment configuration management
- Monitoring and observability (logging, metrics)
- Rate limiting and authentication strategies
- Production deployment checklist

**api.py (250+ lines):**

- Complete FastAPI RAG application
- Endpoints: /query, /health, /metrics
- Authentication with API keys
- Rate limiting middleware
- Async LLM calls
- Structured logging
- Error handling and validation

**demo.py (150+ lines):**

- Demo 1: Basic FastAPI setup
- Demo 2: Adding authentication
- Demo 3: Rate limiting implementation
- Demo 4: Monitoring and metrics
- Local testing examples

**test_api.py (150+ lines):**

- Comprehensive API tests
- Authentication tests
- Rate limiting tests
- Error handling tests
- Load testing examples

**challenge.py:**

- Boilerplate for production RAG API
- Endpoints defined but not implemented
- TODOs for authentication, rate limiting, monitoring

**solution.py:**

- Reference to api.py as the complete solution
- Additional deployment scripts
- Configuration examples

---

### Module 5: Specialized

#### **Lesson 17: Multimodal AI**

[`module5-specialized/lesson17-multimodal/`](module5-specialized/lesson17-multimodal/)

**README.md Enhancements:**

- Vision model capabilities and limitations
- Image preprocessing and optimization
- Prompt engineering for vision tasks
- Structured output from vision models
- Use cases: OCR, document analysis, visual QA

**demo.py (200+ lines):**

- Demo 1: Basic image description with llama3.2-vision
- Demo 2: Visual question answering
- Demo 3: OCR and text extraction
- Demo 4: Image comparison
- Demo 5: Chart/diagram understanding
- Sample images included or downloaded

**challenge.py:**

- Boilerplate for Receipt Analyzer
- Functions: extract_items(), calculate_total(), categorize_expenses()
- Image loading utilities
- TODOs for vision model integration

**solution.py (200+ lines):**

- Complete Receipt Analyzer
- Structured output with Pydantic models
- Item extraction with prices
- Category classification
- Total validation
- Export to JSON/CSV
- Sample receipt processing

---

#### **Lesson 18: Code Generation**

[`module5-specialized/lesson18-code-generation/`](module5-specialized/lesson18-code-generation/)

**README.md Enhancements:**

- CodeLlama capabilities and best practices
- Prompt patterns for code generation
- Code validation strategies (AST parsing, linting)
- Test generation patterns
- Security considerations for generated code

**demo.py (200+ lines):**

- Demo 1: Function generation from description
- Demo 2: Test generation for existing code
- Demo 3: Code explanation and documentation
- Demo 4: Refactoring suggestions
- Demo 5: Bug detection and fixing
- AST validation examples

**challenge.py:**

- Boilerplate for Code Generator
- Functions: generate_function(), generate_tests(), validate_code()
- TODOs for CodeLlama integration
- Validation pipeline structure

**solution.py (250+ lines):**

- Complete Code Generator
- Feature description → Python function
- Automatic test generation
- Syntax validation with ast.parse()
- Optional: pylint/mypy integration
- Documentation generation
- Working examples with multiple function types

---

#### **Lesson 19: Advanced RAG**

[`module5-specialized/lesson19-advanced-rag/`](module5-specialized/lesson19-advanced-rag/)

**README.md Enhancements:**

- Detailed explanation of each technique with diagrams
- Performance comparisons (retrieval quality metrics)
- When to use each technique
- Combining multiple techniques
- Evaluation strategies

**advanced_techniques.py (300+ lines):**

- Complete implementations of all techniques:
  - Query transformation with examples
  - HyDE implementation
  - Multi-query retrieval
  - Re-ranking with cross-encoder
  - Parent-child chunking
  - Metadata filtering
  - Hybrid search (BM25 + semantic)
- Utility functions for each technique
- Performance benchmarking code

**demo.py (200+ lines):**

- Demo 1: Query transformation
- Demo 2: HyDE vs standard retrieval
- Demo 3: Multi-query retrieval
- Demo 4: Re-ranking comparison
- Demo 5: Hybrid search
- Sample documents and queries

**challenge.py:**

- Boilerplate for Advanced RAG System
- Functions: transform_query(), multi_query_retrieve(), rerank(), synthesize_answer()
- TODOs for implementing each technique
- Evaluation framework structure

**solution.py (250+ lines):**

- Complete Advanced RAG System
- All techniques integrated
- Query → Transform → Retrieve → Rerank → Generate pipeline
- Configurable technique selection
- Performance metrics
- Comparison with baseline RAG

---

#### **Lesson 20: Final Project**

[`module5-specialized/lesson20-final-project/`](module5-specialized/lesson20-final-project/)

**README.md Enhancements:**

- Detailed project specifications for each option
- Architecture templates and diagrams
- Step-by-step implementation guides
- Testing strategies
- Deployment considerations
- Example timelines and milestones

**Additional Files:**

- `project_ideas.md`: Expanded project descriptions with technical requirements
- `evaluation_rubric.md`: Detailed rubric with scoring criteria
- `templates/`: Starter templates for each project type
  - `research_assistant_template.py`
  - `code_review_bot_template.py`
  - `customer_support_template.py`
  - `data_analysis_template.py`

---

## Implementation Strategy

### For Each Lesson:

1. **README.md**: Add 2-3 detailed code examples, expand use cases, include diagrams where helpful
2. **demo.py**: 3-5 comprehensive demos (150-250 lines total) with proper error handling
3. **challenge.py**: Clear boilerplate with TODOs, partial implementations, and guidance
4. **solution.py**: Complete working solution with comments explaining key decisions

### Code Quality Standards:

- Type hints for all functions
- Comprehensive docstrings
- Error handling with try/except
- Clear print statements for demo flow
- Comments explaining complex logic
- Consistent formatting and style

### Dependencies:

Add to `requirements.txt`:

```
wikipedia==1.4.0  # Lesson 7 (already needed)
pillow==10.0.0    # Lesson 17 (image processing)
```

MCP library already included.

---

## Validation

After implementation:

- Test all demo.py files run without errors
- Verify challenge.py has clear TODOs
- Confirm solution.py provides complete working code
- Check README.md has sufficient detail and examples
- Ensure consistent style across all lessons