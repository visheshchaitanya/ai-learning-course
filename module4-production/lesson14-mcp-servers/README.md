# Lesson 14: MCP Servers

## Theory

Building custom MCP servers to expose your own tools and resources to AI applications.

### Server Components
1. **Tool Registration**: Define available tools
2. **Resource Providers**: Expose data sources
3. **Request Handling**: Process client requests
4. **Error Handling**: Graceful failures

### Implementation

```python
from mcp.server import Server
from mcp.types import Tool

server = Server("my-server")

@server.tool()
def my_tool(param: str) -> str:
    return f"Result: {param}"

server.run()
```

## Challenge

Build an **MCP Server** that provides tools for managing a TODO list (add, list, complete, delete tasks).

See `demo.py`, `server.py`, `client_demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Building MCP Servers](https://modelcontextprotocol.io/docs/server)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
