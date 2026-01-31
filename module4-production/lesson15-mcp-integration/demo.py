"""
Lesson 15 Demo: MCP Integration with LangChain/LangGraph

Demonstrates integrating MCP servers with LangChain agents and LangGraph workflows.
"""

import asyncio
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_community.chat_models import ChatOllama


# Mock MCP clients for demonstration
class MockMCPClient:
    """Mock MCP client"""
    def __init__(self, name: str, tools: Dict[str, Any]):
        self.name = name
        self.tools = tools
    
    async def connect(self):
        print(f"🔌 Connected to {self.name}")
    
    async def list_tools(self):
        return list(self.tools.values())
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        if name in self.tools:
            return self.tools[name]["handler"](arguments)
        raise ValueError(f"Unknown tool: {name}")


# Demo 1: LangGraph with MCP
class PipelineState(TypedDict):
    input_file: str
    file_data: str
    processed_data: str
    db_result: str


async def demo_langgraph_mcp():
    """Demo: LangGraph workflow with MCP servers"""
    print("\n" + "=" * 70)
    print("Demo: LangGraph with MCP Integration")
    print("=" * 70)
    
    # Create mock MCP servers
    fs_server = MockMCPClient("filesystem", {
        "read_file": {
            "name": "read_file",
            "handler": lambda args: f"Contents of {args['path']}: Sample data"
        }
    })
    
    api_server = MockMCPClient("api", {
        "process": {
            "name": "process",
            "handler": lambda args: f"Processed: {args['data']}"
        }
    })
    
    db_server = MockMCPClient("database", {
        "insert": {
            "name": "insert",
            "handler": lambda args: f"Inserted {len(args['data'])} bytes"
        }
    })
    
    # Connect all servers
    await fs_server.connect()
    await api_server.connect()
    await db_server.connect()
    
    # Define workflow nodes
    async def read_file(state: PipelineState):
        print(f"\n📖 Reading file: {state['input_file']}")
        result = await fs_server.call_tool("read_file", {"path": state['input_file']})
        state["file_data"] = result
        print(f"✅ Read complete")
        return state
    
    async def process_data(state: PipelineState):
        print(f"\n⚙️  Processing data...")
        result = await api_server.call_tool("process", {"data": state['file_data']})
        state["processed_data"] = result
        print(f"✅ Processing complete")
        return state
    
    async def store_data(state: PipelineState):
        print(f"\n💾 Storing data...")
        result = await db_server.call_tool("insert", {"data": state['processed_data']})
        state["db_result"] = result
        print(f"✅ Storage complete")
        return state
    
    # Build workflow
    workflow = StateGraph(PipelineState)
    workflow.add_node("read", read_file)
    workflow.add_node("process", process_data)
    workflow.add_node("store", store_data)
    
    workflow.set_entry_point("read")
    workflow.add_edge("read", "process")
    workflow.add_edge("process", "store")
    workflow.add_edge("store", END)
    
    app = workflow.compile()
    
    # Execute pipeline
    result = app.invoke({
        "input_file": "/data/input.txt",
        "file_data": "",
        "processed_data": "",
        "db_result": ""
    })
    
    print("\n" + "=" * 70)
    print("Pipeline Result:")
    print(f"  File: {result['input_file']}")
    print(f"  Data: {result['file_data'][:50]}...")
    print(f"  Processed: {result['processed_data'][:50]}...")
    print(f"  DB: {result['db_result']}")
    print("=" * 70)


# Demo 2: Multi-server orchestration
async def demo_multi_server():
    """Demo: Orchestrating multiple MCP servers"""
    print("\n" + "=" * 70)
    print("Demo: Multi-Server Orchestration")
    print("=" * 70)
    
    class Orchestrator:
        def __init__(self):
            self.servers = {}
        
        async def add_server(self, name: str, client: MockMCPClient):
            await client.connect()
            self.servers[name] = client
            tools = await client.list_tools()
            print(f"  ✅ {name}: {len(tools)} tools")
        
        async def execute_workflow(self, steps):
            results = []
            for server_name, tool_name, arguments in steps:
                client = self.servers[server_name]
                result = await client.call_tool(tool_name, arguments)
                results.append(result)
                print(f"  ✅ {server_name}.{tool_name}(): {result[:50]}...")
            return results
    
    # Setup
    orchestrator = Orchestrator()
    
    print("\n📋 Connecting to servers:")
    await orchestrator.add_server("fs", MockMCPClient("filesystem", {
        "read": {"name": "read", "handler": lambda a: f"Data from {a['path']}"}
    }))
    await orchestrator.add_server("api", MockMCPClient("api", {
        "transform": {"name": "transform", "handler": lambda a: f"Transformed: {a['data']}"}
    }))
    await orchestrator.add_server("db", MockMCPClient("database", {
        "save": {"name": "save", "handler": lambda a: f"Saved: {a['data']}"}
    }))
    
    # Execute workflow
    print("\n⚙️  Executing workflow:")
    results = await orchestrator.execute_workflow([
        ("fs", "read", {"path": "/data/input.json"}),
        ("api", "transform", {"data": "input_data"}),
        ("db", "save", {"data": "transformed_data"})
    ])
    
    print(f"\n✅ Workflow complete: {len(results)} steps executed")


async def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("MCP Integration Demo")
    print("=" * 70)
    
    try:
        await demo_langgraph_mcp()
        await demo_multi_server()
        
        print("\n" + "=" * 70)
        print("All demos completed!")
        print("=" * 70)
        print("\nKey Concepts:")
        print("✅ LangGraph workflows with MCP")
        print("✅ Multi-server orchestration")
        print("✅ Pipeline patterns")
        print("\nNext: Try challenge.py!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
