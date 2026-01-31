"""
Lesson 13 Challenge: MCP Filesystem Client

Build an MCP client that connects to a filesystem server and performs
file operations via natural language commands.
"""

import asyncio
import json
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


@dataclass
class MCPResource:
    """Represents an MCP resource"""
    uri: str
    name: str
    mime_type: str
    description: str


# ============================================================================
# Mock MCP Server (provided for testing)
# ============================================================================

class MockFilesystemServer:
    """Mock filesystem MCP server for testing"""
    
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
# Challenge: Implement MCPFilesystemClient
# ============================================================================

class MCPFilesystemClient:
    """
    MCP client for filesystem operations.
    
    TODO: Implement the following methods:
    - connect()
    - list_tools()
    - execute_natural_language_command()
    - _parse_command_to_tool_call()
    - _execute_tool()
    """
    
    def __init__(self, server: MockFilesystemServer):
        self.server = server
        self.connected = False
        self.tools: List[Dict[str, Any]] = []
        self.llm = ChatOllama(model="llama3.2", temperature=0.3)
    
    async def connect(self) -> bool:
        """
        Connect to the MCP server and initialize.
        
        TODO:
        - Set self.connected = True
        - Fetch and store available tools
        - Return True on success
        """
        # TODO: Implement connection logic
        print("🔌 Connecting to filesystem server...")
        
        # TODO: Fetch tools from server
        # self.tools = await self.server.list_tools()
        
        # TODO: Set connected flag
        # self.connected = True
        
        print("❌ connect() not implemented yet")
        return False
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools.
        
        TODO:
        - Check if connected
        - Return self.tools
        """
        # TODO: Check connection
        if not self.connected:
            raise RuntimeError("Not connected to server")
        
        # TODO: Return tools
        return []
    
    async def execute_natural_language_command(self, command: str) -> str:
        """
        Execute a natural language command by:
        1. Parsing command to determine tool and arguments
        2. Calling the appropriate MCP tool
        3. Returning the result
        
        TODO:
        - Use LLM to parse command into tool call
        - Execute the tool via MCP
        - Return formatted result
        
        Example commands:
        - "Read the readme file"
        - "Write 'Hello' to test.txt"
        - "List all files"
        - "Delete config.json"
        """
        # TODO: Check connection
        if not self.connected:
            raise RuntimeError("Not connected to server")
        
        print(f"\n💬 Command: {command}")
        
        # TODO: Parse command to tool call
        tool_call = await self._parse_command_to_tool_call(command)
        
        if not tool_call:
            return "Could not understand command"
        
        # TODO: Execute tool
        result = await self._execute_tool(
            tool_call["tool_name"],
            tool_call["arguments"]
        )
        
        return result
    
    async def _parse_command_to_tool_call(self, command: str) -> Optional[Dict[str, Any]]:
        """
        Use LLM to parse natural language command into tool call.
        
        TODO:
        - Create prompt with available tools
        - Ask LLM to extract tool name and arguments
        - Return dict with tool_name and arguments
        
        Returns:
            {
                "tool_name": "read_file",
                "arguments": {"path": "/readme.md"}
            }
        """
        # TODO: Build prompt with tool descriptions
        tools_desc = "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.tools
        ])
        
        prompt = f"""Parse this command into a tool call.

Available tools:
{tools_desc}

Command: {command}

TODO: Complete this prompt to extract:
1. Tool name
2. Arguments (as JSON)

Return format:
Tool: <tool_name>
Arguments: {{"key": "value"}}
"""
        
        # TODO: Call LLM
        # response = self.llm.invoke(prompt).content
        
        # TODO: Parse response into dict
        # Extract tool name and arguments from LLM response
        
        print("❌ _parse_command_to_tool_call() not implemented yet")
        return None
    
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Execute an MCP tool.
        
        TODO:
        - Call server.call_tool()
        - Extract text from result
        - Return formatted string
        """
        # TODO: Call tool
        # result = await self.server.call_tool(tool_name, arguments)
        
        # TODO: Extract text from result
        # text = result["content"][0]["text"]
        
        print("❌ _execute_tool() not implemented yet")
        return "Tool execution not implemented"


# ============================================================================
# Test Function
# ============================================================================

async def test_client():
    """Test the MCP filesystem client"""
    print("=" * 70)
    print("MCP Filesystem Client Challenge")
    print("=" * 70)
    
    # Create server and client
    server = MockFilesystemServer()
    client = MCPFilesystemClient(server)
    
    # Test connection
    print("\n📋 Test 1: Connection")
    connected = await client.connect()
    if not connected:
        print("\n❌ Client not implemented yet!")
        print("\nTODO:")
        print("1. Implement connect() method")
        print("2. Implement list_tools() method")
        print("3. Implement execute_natural_language_command() method")
        print("4. Implement _parse_command_to_tool_call() method")
        print("5. Implement _execute_tool() method")
        print("\nSee solution.py for reference implementation")
        return
    
    # Test listing tools
    print("\n📋 Test 2: List Tools")
    try:
        tools = await client.list_tools()
        print(f"✅ Found {len(tools)} tools")
        for tool in tools:
            print(f"   - {tool['name']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test natural language commands
    test_commands = [
        "List all files",
        "Read the readme file",
        "Write 'Hello MCP!' to greeting.txt",
        "Delete the data.txt file"
    ]
    
    print("\n📋 Test 3: Natural Language Commands")
    for i, command in enumerate(test_commands, 1):
        print(f"\n--- Command {i} ---")
        try:
            result = await client.execute_natural_language_command(command)
            print(f"✅ Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Verify final state
    print("\n📋 Test 4: Verify Final State")
    try:
        result = await client.execute_natural_language_command("List all files")
        print(f"Final files:\n{result}")
    except Exception as e:
        print(f"❌ Error: {e}")


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run the challenge"""
    try:
        await test_client()
        
        print("\n" + "=" * 70)
        print("Challenge Tips:")
        print("=" * 70)
        print("1. Start by implementing connect() and list_tools()")
        print("2. Use the LLM to parse natural language into structured tool calls")
        print("3. Handle errors gracefully (file not found, etc.)")
        print("4. Test with various command phrasings")
        print("\nBonus:")
        print("- Add support for multiple operations in one command")
        print("- Implement command history")
        print("- Add file content validation")
        
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
