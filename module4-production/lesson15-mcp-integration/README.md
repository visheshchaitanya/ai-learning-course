# Lesson 15: MCP Integration

## Theory

Integrating MCP servers with LangChain and LangGraph creates powerful, modular AI systems. This lesson shows how to combine MCP's standardized tool protocol with LangChain's agent framework.

---

## Why Integrate MCP with LangChain?

**MCP provides**: Standardized tools and resources
**LangChain provides**: Agent reasoning and orchestration
**Together**: Modular, scalable AI systems with clean boundaries

```
┌──────────────────────────────────────────────┐
│         LangChain/LangGraph Agent            │
│  (Reasoning, Planning, Orchestration)        │
└──────────────┬───────────────────────────────┘
               │
       ┌───────┴────────┐
       │  MCP Protocol  │
       └───────┬────────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼───┐  ┌──▼────┐
│  FS   │  │  DB  │  │  API  │
│Server │  │Server│  │Server │
└───────┘  └──────┘  └───────┘
```

---

## Integration Patterns

### 1. LangChain Agent with MCP Tools

Convert MCP tools to LangChain tools:

```python
from langchain.tools import Tool
from langchain.agents import create_react_agent

# MCP client
mcp_client = MCPClient(server)
await mcp_client.connect()

# Convert MCP tools to LangChain tools
langchain_tools = []
for mcp_tool in await mcp_client.list_tools():
    tool = Tool(
        name=mcp_tool["name"],
        description=mcp_tool["description"],
        func=lambda **kwargs: mcp_client.call_tool(
            mcp_tool["name"], kwargs
        )
    )
    langchain_tools.append(tool)

# Create agent
agent = create_react_agent(llm, langchain_tools, prompt)
```

### 2. LangGraph Workflow with MCP

Integrate MCP into LangGraph nodes:

```python
from langgraph.graph import StateGraph

class WorkflowState(TypedDict):
    input: str
    data: dict
    result: str

async def fetch_data(state: WorkflowState):
    """Node that uses MCP filesystem server"""
    result = await fs_client.call_tool("read_file", {
        "path": state["input"]
    })
    state["data"] = result
    return state

async def process_data(state: WorkflowState):
    """Node that uses MCP database server"""
    result = await db_client.call_tool("query", {
        "sql": f"INSERT INTO data VALUES ('{state['data']}')"
    })
    state["result"] = result
    return state

workflow = StateGraph(WorkflowState)
workflow.add_node("fetch", fetch_data)
workflow.add_node("process", process_data)
workflow.add_edge("fetch", "process")
```

### 3. Multiple MCP Servers

Orchestrate multiple servers:

```python
class MultiServerOrchestrator:
    def __init__(self):
        self.servers = {
            "filesystem": MCPClient(fs_server),
            "database": MCPClient(db_server),
            "api": MCPClient(api_server)
        }
    
    async def connect_all(self):
        """Connect to all servers"""
        for name, client in self.servers.items():
            await client.connect()
            print(f"Connected to {name}")
    
    async def execute_pipeline(self, data):
        """Execute multi-server pipeline"""
        # Step 1: Read from filesystem
        file_data = await self.servers["filesystem"].call_tool(
            "read_file", {"path": data["file"]}
        )
        
        # Step 2: Process with API
        processed = await self.servers["api"].call_tool(
            "process", {"data": file_data}
        )
        
        # Step 3: Store in database
        result = await self.servers["database"].call_tool(
            "insert", {"data": processed}
        )
        
        return result
```

### 4. Dynamic Tool Discovery

Automatically discover and register tools:

```python
async def discover_and_register_tools(mcp_clients):
    """Discover tools from multiple MCP servers"""
    all_tools = []
    
    for server_name, client in mcp_clients.items():
        tools = await client.list_tools()
        
        for tool in tools:
            # Add server prefix to avoid name conflicts
            tool_name = f"{server_name}_{tool['name']}"
            
            langchain_tool = Tool(
                name=tool_name,
                description=f"[{server_name}] {tool['description']}",
                func=create_tool_func(client, tool['name'])
            )
            all_tools.append(langchain_tool)
    
    return all_tools

def create_tool_func(client, tool_name):
    """Create tool function with closure"""
    async def tool_func(**kwargs):
        return await client.call_tool(tool_name, kwargs)
    return tool_func
```

---

## Architecture Patterns

### Pattern 1: Agent with MCP Tools

```
User Query
    ↓
LangChain Agent (Reasoning)
    ↓
Tool Selection
    ↓
MCP Tool Call
    ↓
MCP Server Execution
    ↓
Result to Agent
    ↓
Final Answer
```

**Use case**: Question answering with external data

### Pattern 2: Multi-Stage Pipeline

```
Input
  ↓
[LangGraph Node 1] → MCP Server A
  ↓
[LangGraph Node 2] → MCP Server B
  ↓
[LangGraph Node 3] → MCP Server C
  ↓
Output
```

**Use case**: Data processing workflows

### Pattern 3: Parallel Execution

```
        Input
          ↓
    ┌─────┼─────┐
    ↓     ↓     ↓
  MCP-A MCP-B MCP-C
    ↓     ↓     ↓
    └─────┼─────┘
          ↓
      Synthesize
          ↓
        Output
```

**Use case**: Gathering data from multiple sources

---

## Benefits

### 1. Modularity
- MCP servers are independent
- Easy to add/remove servers
- Clear separation of concerns

### 2. Reusability
- Same MCP server works with any agent
- Share servers across projects
- Community-built servers

### 3. Testability
- Test servers independently
- Mock MCP clients for agent testing
- Integration tests with real servers

### 4. Scalability
- Scale servers independently
- Distribute across machines
- Load balancing per server

### 5. Maintainability
- Update servers without touching agents
- Version servers independently
- Clear interfaces

---

## Error Handling

### Graceful Degradation

```python
async def robust_tool_call(client, tool_name, arguments):
    """Call MCP tool with fallback"""
    try:
        return await client.call_tool(tool_name, arguments)
    except ConnectionError:
        # Fallback to cached data
        return get_cached_result(tool_name, arguments)
    except TimeoutError:
        # Retry with timeout
        return await retry_with_timeout(client, tool_name, arguments)
    except Exception as e:
        # Log and return error
        logger.error(f"Tool call failed: {e}")
        return {"error": str(e)}
```

### Retry Logic

```python
async def call_with_retry(client, tool_name, arguments, max_retries=3):
    """Call MCP tool with retry"""
    for attempt in range(max_retries):
        try:
            return await client.call_tool(tool_name, arguments)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Performance Considerations

### 1. Connection Pooling

```python
class MCPConnectionPool:
    """Pool of MCP client connections"""
    def __init__(self, server, pool_size=5):
        self.server = server
        self.pool = []
        self.pool_size = pool_size
    
    async def initialize(self):
        """Create connection pool"""
        for _ in range(self.pool_size):
            client = MCPClient(self.server)
            await client.connect()
            self.pool.append(client)
    
    async def execute(self, tool_name, arguments):
        """Execute using pooled connection"""
        client = self.pool.pop(0)
        try:
            result = await client.call_tool(tool_name, arguments)
            return result
        finally:
            self.pool.append(client)
```

### 2. Caching

```python
from functools import lru_cache
import hashlib

class CachedMCPClient:
    """MCP client with caching"""
    def __init__(self, client):
        self.client = client
        self.cache = {}
    
    async def call_tool(self, tool_name, arguments):
        """Call tool with caching"""
        # Create cache key
        key = hashlib.md5(
            f"{tool_name}:{json.dumps(arguments)}".encode()
        ).hexdigest()
        
        # Check cache
        if key in self.cache:
            return self.cache[key]
        
        # Call tool
        result = await self.client.call_tool(tool_name, arguments)
        
        # Cache result
        self.cache[key] = result
        return result
```

### 3. Parallel Execution

```python
async def execute_parallel(clients, tool_calls):
    """Execute multiple MCP calls in parallel"""
    tasks = [
        client.call_tool(tool_name, arguments)
        for client, tool_name, arguments in tool_calls
    ]
    return await asyncio.gather(*tasks)
```

---

## Challenge

Build a **Data Pipeline Agent** that:

1. Uses filesystem MCP server to read data files
2. Uses API MCP server to process data
3. Uses database MCP server to store results
4. Orchestrates with LangGraph
5. Handles errors gracefully
6. Provides status updates

**Requirements:**
- Connect to 3 MCP servers
- Implement multi-stage pipeline
- Add error handling and retries
- Include logging
- Create LangGraph workflow

See `demo.py`, `challenge.py`, and `solution.py` for examples.

## Resources
- [MCP + LangChain](https://modelcontextprotocol.io/docs/integrations/langchain)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
