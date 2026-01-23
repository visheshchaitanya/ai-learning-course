# Lesson 13: MCP Basics

## Theory

Model Context Protocol (MCP) is a standard for connecting AI applications to external data sources and tools.

### Architecture
- **Client**: AI application
- **Server**: Provides tools/resources
- **Transport**: Communication layer (stdio, HTTP)

### Core Concepts
- **Resources**: Data sources (files, databases)
- **Tools**: Actions the AI can take
- **Prompts**: Reusable prompt templates

### Benefits
- Standardized integration
- Reusable servers
- Security boundaries
- Easy deployment

## Challenge

Build an **MCP Client** that connects to a filesystem server and performs file operations via natural language.

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
