# AI Development Learning Course

Complete hands-on curriculum for learning AI development from Langchain basics to production AI agents.

## Course Structure

- **Module 1**: Foundations (Lessons 1-4)
- **Module 2**: Retrieval & Tools (Lessons 5-8)
- **Module 3**: Advanced Agents (Lessons 9-12)
- **Module 4**: Production & Integration (Lessons 13-16)
- **Module 5**: Specialized Topics (Lessons 17-20)

## Quick Start

1. Install Python 3.10+
2. Install Ollama: https://ollama.com/download
3. Set up environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Pull required models:

```bash
ollama pull llama3.2
ollama pull llama3.2-vision
ollama pull codellama
```

5. Start with Module 1, Lesson 1

## Directory Structure

```
ai-learning-course/
├── module1-foundations/
│   ├── lesson1-setup/
│   ├── lesson2-langchain-basics/
│   ├── lesson3-memory/
│   └── lesson4-embeddings/
├── module2-retrieval-tools/
│   ├── lesson5-rag/
│   ├── lesson6-tools/
│   ├── lesson7-agents/
│   └── lesson8-structured-output/
├── module3-advanced-agents/
│   ├── lesson9-langgraph/
│   ├── lesson10-multi-agent/
│   ├── lesson11-human-in-loop/
│   └── lesson12-advanced-patterns/
├── module4-production/
│   ├── lesson13-mcp-basics/
│   ├── lesson14-mcp-servers/
│   ├── lesson15-mcp-integration/
│   └── lesson16-deployment/
└── module5-specialized/
    ├── lesson17-multimodal/
    ├── lesson18-code-generation/
    ├── lesson19-advanced-rag/
    └── lesson20-final-project/
```

## Learning Tips

1. Code along with every example
2. Complete challenges before moving forward
3. Experiment and break things
4. Use print statements to debug agent reasoning
5. Keep a learning journal
6. Build a portfolio of your projects

## Support

- Langchain Docs: https://python.langchain.com/
- Langgraph Docs: https://langchain-ai.github.io/langgraph/
- Ollama Docs: https://ollama.com/docs
- MCP Docs: https://modelcontextprotocol.io/

## Time Commitment

7-12 weeks at 5-10 hours/week, depending on your pace and prior experience.
