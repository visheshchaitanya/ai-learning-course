"""
Lesson 13 Demo: MCP Basics

Demonstrates Model Context Protocol concepts with practical examples.
Note: These are conceptual demos showing MCP patterns. Full MCP implementation
requires running MCP servers.
"""

import asyncio
import json
from typing import Any, Dict, List
from dataclasses import dataclass


# ============================================================================
# Demo 1: Understanding MCP Message Structure
# ============================================================================

def demo_mcp_messages():
    """Demo 1: MCP protocol message structures"""
    print("\n" + "=" * 70)
    print("Demo 1: MCP Message Structures")
    print("=" * 70)
    
    # Initialize request
    print("\n📤 Initialize Request:")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {}
            },
            "clientInfo": {
                "name": "my-mcp-client",
                "version": "1.0.0"
            }
        }
    }
    print(json.dumps(init_request, indent=2))
    
    # Initialize response
    print("\n📥 Initialize Response:")
    init_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {"subscribe": True}
            },
            "serverInfo": {
                "name": "filesystem-server",
                "version": "1.0.0"
            }
        }
    }
    print(json.dumps(init_response, indent=2))
    
    # Tools list request
    print("\n📤 List Tools Request:")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    print(json.dumps(tools_request, indent=2))
    
    # Tools list response
    print("\n📥 List Tools Response:")
    tools_response = {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {
            "tools": [
                {
                    "name": "read_file",
                    "description": "Read contents of a file",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to file"
                            }
                        },
                        "required": ["path"]
                    }
                },
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
            ]
        }
    }
    print(json.dumps(tools_response, indent=2))
    
    # Tool call request
    print("\n📤 Call Tool Request:")
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "read_file",
            "arguments": {
                "path": "/path/to/file.txt"
            }
        }
    }
    print(json.dumps(call_request, indent=2))
    
    # Tool call response
    print("\n📥 Call Tool Response:")
    call_response = {
        "jsonrpc": "2.0",
        "id": 3,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": "File contents here..."
                }
            ]
        }
    }
    print(json.dumps(call_response, indent=2))


# ============================================================================
# Demo 2: Simulated MCP Client
# ============================================================================

@dataclass
class MCPTool:
    """Represents an MCP tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class MCPResource:
    """Represents an MCP resource"""
    uri: str
    name: str
    mime_type: str
    description: str


class MockMCPServer:
    """Mock MCP server for demonstration"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools: List[MCPTool] = []
        self.resources: List[MCPResource] = []
        self._setup()
    
    def _setup(self):
        """Setup mock tools and resources"""
        # Add tools
        self.tools = [
            MCPTool(
                name="read_file",
                description="Read contents of a file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"]
                }
            ),
            MCPTool(
                name="write_file",
                description="Write content to a file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["path", "content"]
                }
            ),
            MCPTool(
                name="list_files",
                description="List files in a directory",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"]
                }
            )
        ]
        
        # Add resources
        self.resources = [
            MCPResource(
                uri="file:///docs/readme.md",
                name="README",
                mime_type="text/markdown",
                description="Project documentation"
            ),
            MCPResource(
                uri="file:///config/settings.json",
                name="Settings",
                mime_type="application/json",
                description="Configuration file"
            )
        ]
    
    async def list_tools(self) -> List[MCPTool]:
        """List available tools"""
        return self.tools
    
    async def list_resources(self) -> List[MCPResource]:
        """List available resources"""
        return self.resources
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool"""
        if name == "read_file":
            path = arguments.get("path", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Contents of {path}:\nThis is a mock file content."
                    }
                ]
            }
        elif name == "write_file":
            path = arguments.get("path", "")
            content = arguments.get("content", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Successfully wrote {len(content)} bytes to {path}"
                    }
                ]
            }
        elif name == "list_files":
            path = arguments.get("path", "")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Files in {path}:\n- file1.txt\n- file2.py\n- folder/"
                    }
                ]
            }
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource"""
        if "readme" in uri.lower():
            return "# Project README\n\nThis is the project documentation."
        elif "settings" in uri.lower():
            return '{"theme": "dark", "language": "en"}'
        else:
            return f"Resource content for {uri}"


class MCPClient:
    """Simple MCP client"""
    
    def __init__(self, server: MockMCPServer):
        self.server = server
        self.initialized = False
    
    async def initialize(self):
        """Initialize connection"""
        print(f"\n🔌 Connecting to server: {self.server.name}")
        await asyncio.sleep(0.1)  # Simulate connection
        self.initialized = True
        print("✅ Connected and initialized")
    
    async def list_tools(self) -> List[MCPTool]:
        """List available tools"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")
        
        print("\n📋 Listing available tools...")
        tools = await self.server.list_tools()
        
        for tool in tools:
            print(f"\n🔧 {tool.name}")
            print(f"   Description: {tool.description}")
            print(f"   Parameters: {list(tool.input_schema.get('properties', {}).keys())}")
        
        return tools
    
    async def list_resources(self) -> List[MCPResource]:
        """List available resources"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")
        
        print("\n📋 Listing available resources...")
        resources = await self.server.list_resources()
        
        for resource in resources:
            print(f"\n📄 {resource.name}")
            print(f"   URI: {resource.uri}")
            print(f"   Type: {resource.mime_type}")
            print(f"   Description: {resource.description}")
        
        return resources
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")
        
        print(f"\n⚙️  Calling tool: {name}")
        print(f"   Arguments: {arguments}")
        
        result = await self.server.call_tool(name, arguments)
        
        print(f"✅ Result: {result['content'][0]['text']}")
        return result
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")
        
        print(f"\n📖 Reading resource: {uri}")
        content = await self.server.read_resource(uri)
        print(f"✅ Content ({len(content)} bytes):\n{content[:200]}...")
        return content


async def demo_mcp_client():
    """Demo 2: Simulated MCP client interaction"""
    print("\n" + "=" * 70)
    print("Demo 2: MCP Client Interaction")
    print("=" * 70)
    
    # Create server and client
    server = MockMCPServer("filesystem-server")
    client = MCPClient(server)
    
    # Initialize
    await client.initialize()
    
    # List tools
    tools = await client.list_tools()
    
    # List resources
    resources = await client.list_resources()
    
    # Call tools
    await client.call_tool("read_file", {"path": "/docs/readme.md"})
    await client.call_tool("write_file", {
        "path": "/output/result.txt",
        "content": "Hello from MCP!"
    })
    await client.call_tool("list_files", {"path": "/docs"})
    
    # Read resources
    await client.read_resource("file:///docs/readme.md")
    await client.read_resource("file:///config/settings.json")


# ============================================================================
# Demo 3: MCP with LLM Integration
# ============================================================================

async def demo_mcp_with_llm():
    """Demo 3: Using MCP tools with LLM"""
    print("\n" + "=" * 70)
    print("Demo 3: MCP with LLM Integration")
    print("=" * 70)
    
    server = MockMCPServer("filesystem-server")
    client = MCPClient(server)
    await client.initialize()
    
    # Simulate LLM deciding which tools to use
    user_query = "Read the README file and create a summary in summary.txt"
    
    print(f"\n💬 User Query: {user_query}")
    print("\n🤖 LLM Analysis:")
    print("   1. Need to read README file")
    print("   2. Need to write summary to file")
    print("   3. Will use: read_file, write_file")
    
    # Step 1: Read README
    print("\n📖 Step 1: Reading README...")
    readme_result = await client.call_tool("read_file", {
        "path": "/docs/readme.md"
    })
    readme_content = readme_result['content'][0]['text']
    
    # Step 2: Simulate LLM summarization
    print("\n🤖 Step 2: LLM generating summary...")
    summary = "Summary: This project provides documentation and examples."
    print(f"   Generated: {summary}")
    
    # Step 3: Write summary
    print("\n💾 Step 3: Writing summary...")
    await client.call_tool("write_file", {
        "path": "/output/summary.txt",
        "content": summary
    })
    
    print("\n✅ Task completed successfully!")


# ============================================================================
# Demo 4: Error Handling
# ============================================================================

async def demo_error_handling():
    """Demo 4: Error handling in MCP"""
    print("\n" + "=" * 70)
    print("Demo 4: Error Handling")
    print("=" * 70)
    
    server = MockMCPServer("filesystem-server")
    client = MCPClient(server)
    await client.initialize()
    
    # Test 1: Invalid tool
    print("\n🧪 Test 1: Calling non-existent tool")
    try:
        await client.call_tool("invalid_tool", {})
    except ValueError as e:
        print(f"❌ Caught error: {e}")
        print("✅ Error handled gracefully")
    
    # Test 2: Missing required argument
    print("\n🧪 Test 2: Missing required argument")
    try:
        result = await client.call_tool("read_file", {})
        # In real implementation, server would validate
        print("⚠️  Server should validate required arguments")
    except Exception as e:
        print(f"❌ Caught error: {e}")
    
    # Test 3: Client not initialized
    print("\n🧪 Test 3: Using uninitialized client")
    new_client = MCPClient(server)
    try:
        await new_client.list_tools()
    except RuntimeError as e:
        print(f"❌ Caught error: {e}")
        print("✅ Proper initialization check")


# ============================================================================
# Demo 5: Multiple Servers
# ============================================================================

async def demo_multiple_servers():
    """Demo 5: Working with multiple MCP servers"""
    print("\n" + "=" * 70)
    print("Demo 5: Multiple MCP Servers")
    print("=" * 70)
    
    # Create multiple servers
    fs_server = MockMCPServer("filesystem-server")
    db_server = MockMCPServer("database-server")
    api_server = MockMCPServer("api-server")
    
    # Create clients
    fs_client = MCPClient(fs_server)
    db_client = MCPClient(db_server)
    api_client = MCPClient(api_server)
    
    # Initialize all
    print("\n🔌 Connecting to multiple servers...")
    await fs_client.initialize()
    await db_client.initialize()
    await api_client.initialize()
    
    print("\n✅ All servers connected!")
    print("\n📊 Available capabilities:")
    print("   - Filesystem: read/write files")
    print("   - Database: query/update data")
    print("   - API: external service calls")
    
    # Orchestrate across servers
    print("\n🎯 Orchestrating multi-server workflow:")
    print("   1. Read config from filesystem")
    print("   2. Query database with config")
    print("   3. Call API with database results")
    print("   4. Write API response to file")
    
    await fs_client.call_tool("read_file", {"path": "/config/db.json"})
    print("   ↓")
    print("   [Database query executed]")
    print("   ↓")
    print("   [API call made]")
    print("   ↓")
    await fs_client.call_tool("write_file", {
        "path": "/output/results.json",
        "content": '{"status": "success"}'
    })
    
    print("\n✅ Multi-server workflow completed!")


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("MCP Basics Demo")
    print("=" * 70)
    
    try:
        demo_mcp_messages()
        await demo_mcp_client()
        await demo_mcp_with_llm()
        await demo_error_handling()
        await demo_multiple_servers()
        
        print("\n" + "=" * 70)
        print("All demos completed!")
        print("=" * 70)
        print("\nKey Concepts:")
        print("✅ MCP protocol message structure")
        print("✅ Client-server communication")
        print("✅ Tools and resources")
        print("✅ LLM integration patterns")
        print("✅ Error handling")
        print("✅ Multiple server orchestration")
        print("\nNext: Try challenge.py to build your own MCP client!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
