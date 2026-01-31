"""
Lesson 13 Solution: MCP Filesystem Client

Complete implementation of MCP client with natural language interface.
"""

import asyncio
import json
import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from langchain_community.chat_models import ChatOllama


# ============================================================================
# MCP Data Structures
# ============================================================================

@dataclass
class MCPTool:
    """Represents an MCP tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]


# ============================================================================
# Mock MCP Server
# ============================================================================

class MockFilesystemServer:
    """Mock filesystem MCP server"""
    
    def __init__(self):
        self.files: Dict[str, str] = {
            "/readme.md": "# Project\nThis is a test project.",
            "/config.json": '{"theme": "dark", "lang": "en"}',
            "/data.txt": "Sample data content"
        }
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Return available tools"""
        return [
            {
                "name": "read_file",
                "description": "Read contents of a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
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
            },
            {
                "name": "list_files",
                "description": "List all files",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "delete_file",
                "description": "Delete a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool"""
        if name == "read_file":
            path = arguments["path"]
            if path in self.files:
                return {"content": [{"type": "text", "text": self.files[path]}]}
            else:
                return {"content": [{"type": "text", "text": f"Error: File {path} not found"}]}
        
        elif name == "write_file":
            path = arguments["path"]
            content = arguments["content"]
            self.files[path] = content
            return {"content": [{"type": "text", "text": f"Successfully wrote to {path}"}]}
        
        elif name == "list_files":
            file_list = "\n".join(self.files.keys())
            return {"content": [{"type": "text", "text": f"Files:\n{file_list}"}]}
        
        elif name == "delete_file":
            path = arguments["path"]
            if path in self.files:
                del self.files[path]
                return {"content": [{"type": "text", "text": f"Deleted {path}"}]}
            else:
                return {"content": [{"type": "text", "text": f"Error: File {path} not found"}]}
        
        else:
            raise ValueError(f"Unknown tool: {name}")


# ============================================================================
# MCP Filesystem Client
# ============================================================================

class MCPFilesystemClient:
    """MCP client for filesystem operations with natural language interface"""
    
    def __init__(self, server: MockFilesystemServer):
        self.server = server
        self.connected = False
        self.tools: List[Dict[str, Any]] = []
        self.llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    async def connect(self) -> bool:
        """Connect to the MCP server and initialize"""
        print("🔌 Connecting to filesystem server...")
        
        try:
            # Fetch available tools
            self.tools = await self.server.list_tools()
            self.connected = True
            
            print(f"✅ Connected! Found {len(self.tools)} tools:")
            for tool in self.tools:
                print(f"   - {tool['name']}: {tool['description']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        if not self.connected:
            raise RuntimeError("Not connected to server")
        
        return self.tools
    
    async def execute_natural_language_command(self, command: str) -> str:
        """
        Execute a natural language command.
        
        Parses the command, determines the appropriate tool and arguments,
        then executes via MCP.
        """
        if not self.connected:
            raise RuntimeError("Not connected to server")
        
        print(f"\n💬 Command: {command}")
        
        # Parse command to tool call
        tool_call = await self._parse_command_to_tool_call(command)
        
        if not tool_call:
            return "❌ Could not understand command"
        
        print(f"🔧 Tool: {tool_call['tool_name']}")
        print(f"📋 Arguments: {tool_call['arguments']}")
        
        # Execute tool
        result = await self._execute_tool(
            tool_call["tool_name"],
            tool_call["arguments"]
        )
        
        return result
    
    async def _parse_command_to_tool_call(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Use LLM to parse natural language command into tool call.
        
        Returns dict with tool_name and arguments.
        """
        # Build tool descriptions
        tools_desc = []
        for tool in self.tools:
            params = tool['inputSchema'].get('properties', {})
            param_list = ", ".join(params.keys()) if params else "none"
            tools_desc.append(
                f"- {tool['name']}: {tool['description']} (params: {param_list})"
            )
        
        tools_text = "\n".join(tools_desc)
        
        prompt = f"""Parse this command into a tool call.

Available tools:
{tools_text}

Command: "{command}"

Determine:
1. Which tool to use
2. What arguments to pass

Respond ONLY in this format:
TOOL: <tool_name>
ARGUMENTS: {{"key": "value"}}

If the command mentions a file, include the full path starting with /.
Examples:
- "readme" or "readme.md" → "/readme.md"
- "config.json" → "/config.json"
- "test.txt" → "/test.txt"

Response:"""
        
        try:
            response = self.llm.invoke(prompt).content
            
            # Parse response
            tool_name = None
            arguments = {}
            
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('TOOL:'):
                    tool_name = line.split('TOOL:')[1].strip()
                elif line.startswith('ARGUMENTS:'):
                    args_str = line.split('ARGUMENTS:')[1].strip()
                    try:
                        arguments = json.loads(args_str)
                    except json.JSONDecodeError:
                        # Try to extract manually
                        if '{}' in args_str or not args_str:
                            arguments = {}
                        else:
                            # Simple extraction for common patterns
                            path_match = re.search(r'"path":\s*"([^"]+)"', args_str)
                            content_match = re.search(r'"content":\s*"([^"]+)"', args_str)
                            if path_match:
                                arguments["path"] = path_match.group(1)
                            if content_match:
                                arguments["content"] = content_match.group(1)
            
            if tool_name:
                return {
                    "tool_name": tool_name,
                    "arguments": arguments
                }
            else:
                return None
                
        except Exception as e:
            print(f"⚠️  Parse error: {e}")
            return None
    
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute an MCP tool"""
        try:
            # Call tool via MCP
            result = await self.server.call_tool(tool_name, arguments)
            
            # Extract text from result
            if "content" in result and len(result["content"]) > 0:
                text = result["content"][0]["text"]
                return text
            else:
                return "No result returned"
                
        except Exception as e:
            return f"❌ Tool execution error: {e}"


# ============================================================================
# Test Function
# ============================================================================

async def test_client():
    """Test the MCP filesystem client"""
    print("=" * 70)
    print("MCP Filesystem Client Solution")
    print("=" * 70)
    
    # Create server and client
    server = MockFilesystemServer()
    client = MCPFilesystemClient(server)
    
    # Test connection
    print("\n📋 Test 1: Connection")
    connected = await client.connect()
    if not connected:
        print("❌ Connection failed")
        return
    
    # Test listing tools
    print("\n📋 Test 2: List Tools")
    tools = await client.list_tools()
    print(f"✅ Found {len(tools)} tools")
    
    # Test natural language commands
    test_commands = [
        "List all files",
        "Read the readme file",
        "Write 'Hello MCP!' to greeting.txt",
        "Read greeting.txt",
        "Delete the data.txt file",
        "List all files again"
    ]
    
    print("\n📋 Test 3: Natural Language Commands")
    for i, command in enumerate(test_commands, 1):
        print(f"\n{'='*70}")
        print(f"Command {i}/{len(test_commands)}")
        print(f"{'='*70}")
        try:
            result = await client.execute_natural_language_command(command)
            print(f"✅ Result:\n{result}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Verify final state
    print(f"\n{'='*70}")
    print("Final State Verification")
    print(f"{'='*70}")
    result = await client.execute_natural_language_command("List all files")
    print(f"Final files:\n{result}")


# ============================================================================
# Interactive Mode
# ============================================================================

async def interactive_mode():
    """Interactive command-line interface"""
    print("=" * 70)
    print("MCP Filesystem Client - Interactive Mode")
    print("=" * 70)
    
    server = MockFilesystemServer()
    client = MCPFilesystemClient(server)
    
    # Connect
    connected = await client.connect()
    if not connected:
        print("❌ Failed to connect")
        return
    
    print("\n💡 Try commands like:")
    print("   - List all files")
    print("   - Read the readme file")
    print("   - Write 'content' to filename.txt")
    print("   - Delete filename.txt")
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            command = input("📝 Command: ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not command:
                continue
            
            result = await client.execute_natural_language_command(command)
            print(f"\n{result}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run the solution"""
    import sys
    
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            await interactive_mode()
        else:
            await test_client()
            
            print("\n" + "=" * 70)
            print("Solution completed!")
            print("=" * 70)
            print("\nKey Features:")
            print("✅ MCP client connection and initialization")
            print("✅ Tool discovery and listing")
            print("✅ Natural language command parsing with LLM")
            print("✅ Tool execution via MCP protocol")
            print("✅ Error handling and validation")
            print("\nRun with --interactive for interactive mode:")
            print("  python solution.py --interactive")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running:")
        print("  ollama serve")
        print("  ollama pull llama3.2")
