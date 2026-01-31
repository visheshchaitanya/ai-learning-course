# Lesson 14: MCP Servers

## Theory

Building custom MCP servers allows you to expose your own tools, data sources, and capabilities to AI applications. This lesson covers server architecture, implementation patterns, and best practices.

---

## Why Build MCP Servers?

**Encapsulation**: Wrap complex functionality in simple, AI-accessible tools
**Reusability**: One server works with any MCP-compatible client
**Security**: Control access and permissions at the server level
**Modularity**: Independent deployment and updates

---

## Server Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│           MCP Server                    │
├─────────────────────────────────────────┤
│  1. Tool Registry                       │
│     - Tool definitions                  │
│     - Input schemas                     │
│     - Handlers                          │
├─────────────────────────────────────────┤
│  2. Resource Providers                  │
│     - Data sources                      │
│     - Resource URIs                     │
│     - Content handlers                  │
├─────────────────────────────────────────┤
│  3. Request Handler                     │
│     - Protocol implementation           │
│     - Message routing                   │
│     - Response formatting               │
├─────────────────────────────────────────┤
│  4. Transport Layer                     │
│     - stdio / HTTP / SSE                │
│     - Connection management             │
│     - Error handling                    │
└─────────────────────────────────────────┘
```

---

## 1. Tool Registration

Tools are functions that AI can call. Each tool needs:
- **Name**: Unique identifier
- **Description**: What it does (for AI to understand)
- **Input Schema**: JSON Schema for parameters
- **Handler**: Function that executes the tool

### Basic Tool

```python
from mcp.server import Server

app = Server("my-server")

@app.tool()
async def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"
```

### Tool with Complex Schema

```python
@app.tool()
async def search_database(
    query: str,
    limit: int = 10,
    filters: dict = None
) -> list:
    """
    Search database with filters.
    
    Args:
        query: Search query string
        limit: Maximum results to return
        filters: Optional filters (e.g., {"status": "active"})
    """
    # Implementation
    results = perform_search(query, limit, filters)
    return results
```

The SDK automatically generates the JSON Schema from type hints and docstrings.

### Manual Schema Definition

```python
from mcp.types import Tool

tool = Tool(
    name="calculate",
    description="Perform mathematical calculations",
    inputSchema={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression to evaluate"
            },
            "precision": {
                "type": "integer",
                "description": "Decimal precision",
                "default": 2
            }
        },
        "required": ["expression"]
    }
)

@app.tool_handler(tool)
async def handle_calculate(expression: str, precision: int = 2):
    result = eval(expression)  # Unsafe! Use ast.literal_eval
    return round(result, precision)
```

---

## 2. Resource Providers

Resources are read-only data sources that AI can access.

### File Resource

```python
@app.resource("file:///{path}")
async def read_file(path: str) -> str:
    """Read file contents"""
    with open(path, 'r') as f:
        return f.read()
```

### Database Resource

```python
@app.resource("db:///{table}/{id}")
async def get_record(table: str, id: str) -> dict:
    """Get database record"""
    record = database.get(table, id)
    return json.dumps(record)
```

### Dynamic Resource List

```python
@app.list_resources()
async def list_available_resources():
    """List all available resources"""
    files = os.listdir("/data")
    return [
        {
            "uri": f"file:///{f}",
            "name": f,
            "mimeType": "text/plain",
            "description": f"Contents of {f}"
        }
        for f in files
    ]
```

---

## 3. Request Handling

### Lifecycle

```
Client                          Server
  │                               │
  │──── initialize ──────────────>│
  │                               │ Setup
  │<─── capabilities ─────────────│
  │                               │
  │──── initialized ─────────────>│
  │                               │
  │──── tools/list ──────────────>│
  │<─── [tools] ──────────────────│
  │                               │
  │──── tools/call ──────────────>│
  │                               │ Execute
  │<─── result ───────────────────│
  │                               │
  │──── shutdown ────────────────>│
  │                               │ Cleanup
  │<─── ok ───────────────────────│
```

### Implementing Handlers

```python
from mcp.server import Server
from mcp.server.models import InitializationOptions

app = Server("my-server")

@app.initialize()
async def initialize(options: InitializationOptions):
    """Called when client connects"""
    print(f"Client connected: {options.clientInfo.name}")
    # Setup resources, connections, etc.
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {},
            "resources": {}
        },
        "serverInfo": {
            "name": "my-server",
            "version": "1.0.0"
        }
    }

@app.shutdown()
async def shutdown():
    """Called when client disconnects"""
    print("Client disconnected")
    # Cleanup resources, close connections, etc.
```

---

## 4. Error Handling

### Tool Errors

```python
from mcp.server.models import McpError, ErrorCode

@app.tool()
async def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise McpError(
            ErrorCode.InvalidParams,
            "Cannot divide by zero"
        )
    return a / b
```

### Validation

```python
@app.tool()
async def create_user(name: str, email: str, age: int) -> dict:
    """Create a new user"""
    # Validate inputs
    if not name or len(name) < 2:
        raise McpError(
            ErrorCode.InvalidParams,
            "Name must be at least 2 characters"
        )
    
    if "@" not in email:
        raise McpError(
            ErrorCode.InvalidParams,
            "Invalid email address"
        )
    
    if age < 0 or age > 150:
        raise McpError(
            ErrorCode.InvalidParams,
            "Age must be between 0 and 150"
        )
    
    # Create user
    user = database.create_user(name, email, age)
    return user
```

### Graceful Degradation

```python
@app.tool()
async def fetch_weather(city: str) -> dict:
    """Get weather for a city"""
    try:
        # Try primary API
        return await weather_api.get(city)
    except APIError:
        try:
            # Fallback to secondary API
            return await backup_weather_api.get(city)
        except APIError:
            # Return cached data if available
            cached = cache.get(f"weather:{city}")
            if cached:
                return {**cached, "source": "cache"}
            else:
                raise McpError(
                    ErrorCode.InternalError,
                    "Weather service unavailable"
                )
```

---

## Transport Implementations

### stdio (Standard Input/Output)

Best for local processes, IDE integrations.

```python
from mcp.server.stdio import stdio_server

async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**Run as subprocess:**
```bash
python mcp_server.py
```

### HTTP/SSE (Server-Sent Events)

Best for remote access, multiple clients.

```python
from mcp.server.sse import sse_server
from fastapi import FastAPI

fastapi_app = FastAPI()

@fastapi_app.get("/sse")
async def handle_sse(request: Request):
    async with sse_server(request) as (read, write):
        await app.run(read, write)

# Run with: uvicorn server:fastapi_app
```

---

## Server Patterns

### 1. Stateless Server

Each request is independent, no session state.

```python
@app.tool()
async def calculate(expression: str) -> float:
    """Stateless calculation"""
    return eval(expression)
```

**Pros**: Simple, scalable, no memory leaks
**Cons**: Can't maintain context between calls

### 2. Stateful Server

Maintains state across requests.

```python
class StatefulServer:
    def __init__(self):
        self.sessions = {}
    
    @app.tool()
    async def start_session(user_id: str) -> str:
        """Start a new session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "user_id": user_id,
            "created": datetime.now(),
            "data": {}
        }
        return session_id
    
    @app.tool()
    async def add_to_session(session_id: str, key: str, value: any):
        """Add data to session"""
        if session_id not in self.sessions:
            raise McpError(ErrorCode.InvalidParams, "Invalid session")
        self.sessions[session_id]["data"][key] = value
```

**Pros**: Can maintain context, more powerful
**Cons**: Memory management, cleanup needed

### 3. Hybrid Server

Combines both approaches.

```python
@app.tool()
async def query_database(query: str, session_id: str = None) -> list:
    """Query with optional session context"""
    # Stateless: just run query
    if not session_id:
        return database.query(query)
    
    # Stateful: use session context
    session = get_session(session_id)
    filters = session.get("filters", {})
    return database.query(query, filters=filters)
```

---

## Security Best Practices

### 1. Input Validation

```python
import re

@app.tool()
async def read_file(path: str) -> str:
    """Read file with path validation"""
    # Prevent directory traversal
    if ".." in path or path.startswith("/"):
        raise McpError(ErrorCode.InvalidParams, "Invalid path")
    
    # Whitelist allowed extensions
    if not path.endswith((".txt", ".md", ".json")):
        raise McpError(ErrorCode.InvalidParams, "File type not allowed")
    
    # Read from safe directory
    safe_path = os.path.join("/safe/directory", path)
    with open(safe_path, 'r') as f:
        return f.read()
```

### 2. Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, window: timedelta):
        self.max_calls = max_calls
        self.window = window
        self.calls = defaultdict(list)
    
    def check(self, client_id: str) -> bool:
        now = datetime.now()
        # Remove old calls
        self.calls[client_id] = [
            t for t in self.calls[client_id]
            if now - t < self.window
        ]
        # Check limit
        if len(self.calls[client_id]) >= self.max_calls:
            return False
        self.calls[client_id].append(now)
        return True

limiter = RateLimiter(max_calls=100, window=timedelta(minutes=1))

@app.tool()
async def expensive_operation(client_id: str, data: str):
    """Rate-limited operation"""
    if not limiter.check(client_id):
        raise McpError(ErrorCode.InvalidRequest, "Rate limit exceeded")
    
    return perform_operation(data)
```

### 3. Authentication

```python
import hmac
import hashlib

def verify_token(token: str, secret: str) -> bool:
    """Verify HMAC token"""
    try:
        payload, signature = token.split(".")
        expected = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)
    except:
        return False

@app.tool()
async def protected_operation(token: str, data: str):
    """Operation requiring authentication"""
    if not verify_token(token, SECRET_KEY):
        raise McpError(ErrorCode.InvalidRequest, "Invalid token")
    
    return perform_protected_operation(data)
```

---

## Testing MCP Servers

### Unit Tests

```python
import pytest
from mcp.client.session import ClientSession

@pytest.mark.asyncio
async def test_tool_execution():
    """Test tool execution"""
    # Create test client
    async with create_test_client(app) as client:
        # Call tool
        result = await client.call_tool("greet", {"name": "Alice"})
        assert result == "Hello, Alice!"

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling"""
    async with create_test_client(app) as client:
        with pytest.raises(McpError) as exc:
            await client.call_tool("divide", {"a": 10, "b": 0})
        assert exc.value.code == ErrorCode.InvalidParams
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_workflow():
    """Test complete workflow"""
    async with create_test_client(app) as client:
        # Initialize
        await client.initialize()
        
        # List tools
        tools = await client.list_tools()
        assert len(tools) > 0
        
        # Execute workflow
        session = await client.call_tool("start_session", {"user": "test"})
        await client.call_tool("add_data", {"session": session, "key": "value"})
        result = await client.call_tool("get_data", {"session": session})
        assert result["key"] == "value"
```

---

## Challenge

Build a **TODO List MCP Server** that provides:

**Tools:**
- `add_task(title, description)`: Add new task
- `list_tasks(status)`: List tasks (all, pending, completed)
- `complete_task(task_id)`: Mark task as complete
- `delete_task(task_id)`: Delete a task
- `update_task(task_id, title, description)`: Update task details

**Resources:**
- `todo://tasks`: List of all tasks
- `todo://task/{id}`: Individual task details

**Requirements:**
- Persistent storage (JSON file)
- Input validation
- Error handling
- Task IDs (UUID)

See `demo.py`, `server.py`, `client_demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [Building MCP Servers](https://modelcontextprotocol.io/docs/server)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
