# Lesson 13: MCP Basics

## Theory

Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect to external data sources and tools. Think of it as a universal adapter that lets AI assistants interact with your local files, databases, APIs, and more.

### Why MCP?

Before MCP, every AI tool needed custom integrations for each data source. MCP standardizes this:

**Without MCP:**
```
AI App 1 → Custom Integration → Database
AI App 1 → Custom Integration → Files
AI App 2 → Custom Integration → Database (duplicate work!)
AI App 2 → Custom Integration → Files (duplicate work!)
```

**With MCP:**
```
AI App 1 ──┐
AI App 2 ──┼→ MCP Protocol → MCP Server (Database)
AI App 3 ──┘                 MCP Server (Files)
                             MCP Server (API)
```

---

## Architecture

### Three Core Components

```
┌─────────────┐         ┌───────────────┐         ┌──────────────┐
│   Client    │ ◄─────► │   Transport   │ ◄─────► │    Server    │
│ (AI App)    │         │ (stdio/HTTP)  │         │ (Tools/Data) │
└─────────────┘         └───────────────┘         └──────────────┘
```

**1. Client (AI Application)**
- Your AI assistant (Claude, GPT, local LLM)
- Sends requests to servers
- Receives and processes responses
- Examples: Cursor IDE, Claude Desktop, custom agents

**2. Transport Layer**
- Communication protocol between client and server
- **stdio**: Standard input/output (local processes)
- **HTTP/SSE**: Network communication (remote servers)
- Handles message serialization and delivery

**3. Server (Data/Tool Provider)**
- Exposes tools and resources to clients
- Handles requests and returns results
- Examples: filesystem server, database server, API wrapper

---

## Core Concepts

### 1. Resources

Resources are **data sources** that the AI can read from.

**Examples:**
- File contents
- Database records
- API responses
- Configuration data

**Resource Structure:**
```json
{
  "uri": "file:///path/to/document.txt",
  "name": "Project Documentation",
  "mimeType": "text/plain",
  "description": "Main project README"
}
```

**Use Cases:**
- Reading documentation
- Accessing database schemas
- Fetching configuration files
- Loading context for AI

### 2. Tools

Tools are **actions** that the AI can execute.

**Examples:**
- Write to file
- Execute SQL query
- Call external API
- Run system command

**Tool Structure:**
```json
{
  "name": "write_file",
  "description": "Write content to a file",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {"type": "string"},
      "content": {"type": "string"}
    },
    "required": ["path", "content"]
  }
}
```

**Use Cases:**
- File operations
- Database modifications
- API interactions
- System automation

### 3. Prompts

Prompts are **reusable templates** for common tasks.

**Example:**
```json
{
  "name": "summarize_file",
  "description": "Summarize a file's contents",
  "arguments": [
    {
      "name": "file_path",
      "description": "Path to file",
      "required": true
    }
  ]
}
```

---

## MCP Protocol Flow

### Initialization

```
Client                          Server
  │                               │
  │──── initialize request ──────>│
  │                               │
  │<─── capabilities response ────│
  │                               │
  │──── initialized notification ─>│
```

### Tool Execution

```
Client                          Server
  │                               │
  │──── tools/list ──────────────>│
  │<─── [available tools] ────────│
  │                               │
  │──── tools/call ──────────────>│
  │     (name: "write_file")      │
  │     (args: {...})             │
  │                               │
  │<─── result ───────────────────│
```

### Resource Access

```
Client                          Server
  │                               │
  │──── resources/list ──────────>│
  │<─── [available resources] ────│
  │                               │
  │──── resources/read ──────────>│
  │     (uri: "file://...")       │
  │                               │
  │<─── content ──────────────────│
```

---

## Transport Types

### stdio (Standard Input/Output)

**Best for:** Local processes, development, IDE integrations

```python
# Server runs as subprocess
import subprocess

server_process = subprocess.Popen(
    ["python", "mcp_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
)

# Client communicates via stdin/stdout
```

**Pros:**
- Simple setup
- No network configuration
- Secure (local only)
- Fast communication

**Cons:**
- Local only (no remote access)
- One client per server instance

### HTTP/SSE (Server-Sent Events)

**Best for:** Remote servers, multiple clients, production deployments

```python
# Server runs as HTTP endpoint
from fastapi import FastAPI

app = FastAPI()

@app.post("/mcp")
async def handle_mcp_request(request: MCPRequest):
    return handle_request(request)
```

**Pros:**
- Remote access
- Multiple clients
- Standard web protocols
- Scalable

**Cons:**
- More complex setup
- Network security considerations
- Requires server infrastructure

---

## Benefits of MCP

### 1. Standardization
- One protocol for all integrations
- Consistent API across servers
- Interoperable tools

### 2. Reusability
- Write server once, use with any MCP client
- Share servers across team
- Community-built servers

### 3. Security
- Clear boundaries between AI and data
- Permission-based access
- Sandboxed execution

### 4. Modularity
- Add/remove servers dynamically
- Independent server updates
- Composable functionality

### 5. Developer Experience
- Simple to build servers
- Well-documented protocol
- SDKs for multiple languages

---

## Real-World Use Cases

### IDE Integration (Cursor, VS Code)
```
Cursor IDE (Client)
  ├─> MCP Filesystem Server (read/write code)
  ├─> MCP Git Server (commit, branch, diff)
  ├─> MCP Database Server (query schemas)
  └─> MCP Documentation Server (search docs)
```

### Data Analysis Assistant
```
AI Agent (Client)
  ├─> MCP Database Server (SQL queries)
  ├─> MCP API Server (fetch external data)
  ├─> MCP Visualization Server (create charts)
  └─> MCP Export Server (save reports)
```

### Customer Support Bot
```
Support Bot (Client)
  ├─> MCP CRM Server (customer data)
  ├─> MCP Ticket Server (create/update tickets)
  ├─> MCP Knowledge Base Server (search articles)
  └─> MCP Email Server (send responses)
```

---

## Getting Started

### Basic Client Example

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Connect to server
server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Initialize
        await session.initialize()
        
        # List tools
        tools = await session.list_tools()
        print(f"Available tools: {tools}")
        
        # Call tool
        result = await session.call_tool("write_file", {
            "path": "test.txt",
            "content": "Hello MCP!"
        })
        print(f"Result: {result}")
```

### Basic Server Example

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("my-mcp-server")

@app.tool()
async def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"

@app.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Run server
async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write)
```

---

## Security Considerations

### 1. Sandboxing
- Servers should validate all inputs
- Restrict file system access
- Limit command execution

### 2. Authentication
- API keys for remote servers
- Token-based auth for HTTP transport
- Client certificates for mutual TLS

### 3. Rate Limiting
- Prevent abuse
- Quota management
- Throttling mechanisms

### 4. Audit Logging
- Track all tool calls
- Log resource access
- Monitor for suspicious activity

---

## Challenge

Build an **MCP Client** that:
1. Connects to a filesystem MCP server
2. Lists available tools and resources
3. Performs file operations via natural language
4. Handles errors gracefully

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)
