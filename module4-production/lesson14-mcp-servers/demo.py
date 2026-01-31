"""
Lesson 14 Demo: Building MCP Servers

Demonstrates how to build MCP servers with tools, resources, and proper architecture.
"""

import asyncio
import json
from typing import Any, Dict, List
from datetime import datetime


# ============================================================================
# Demo 1: Simple MCP Server
# ============================================================================

class SimpleMCPServer:
    """Minimal MCP server example"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.tool_handlers = {}
    
    def tool(self, name: str, description: str):
        """Register a tool"""
        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description,
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
            self.tool_handlers[name] = func
            return func
        return decorator
    
    async def list_tools(self):
        """List available tools"""
        return list(self.tools.values())
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Call a tool"""
        if name not in self.tool_handlers:
            raise ValueError(f"Unknown tool: {name}")
        return await self.tool_handlers[name](**arguments)


async def demo_simple_server():
    """Demo 1: Simple MCP server with basic tools"""
    print("\n" + "=" * 70)
    print("Demo 1: Simple MCP Server")
    print("=" * 70)
    
    # Create server
    server = SimpleMCPServer("calculator-server")
    
    # Register tools
    @server.tool("add", "Add two numbers")
    async def add(a: float, b: float) -> float:
        return a + b
    
    @server.tool("multiply", "Multiply two numbers")
    async def multiply(a: float, b: float) -> float:
        return a * b
    
    @server.tool("greet", "Greet someone")
    async def greet(name: str) -> str:
        return f"Hello, {name}!"
    
    # List tools
    print("\n📋 Available Tools:")
    tools = await server.list_tools()
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # Call tools
    print("\n⚙️  Calling Tools:")
    
    result1 = await server.call_tool("add", {"a": 5, "b": 3})
    print(f"   add(5, 3) = {result1}")
    
    result2 = await server.call_tool("multiply", {"a": 4, "b": 7})
    print(f"   multiply(4, 7) = {result2}")
    
    result3 = await server.call_tool("greet", {"name": "Alice"})
    print(f"   greet('Alice') = {result3}")
    
    print("\n✅ Simple server demo complete!")


# ============================================================================
# Demo 2: Server with State
# ============================================================================

class StatefulMCPServer:
    """MCP server that maintains state"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.tool_handlers = {}
        self.data_store = {}  # State storage
    
    def tool(self, name: str, description: str):
        """Register a tool"""
        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description
            }
            self.tool_handlers[name] = func
            return func
        return decorator
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Call a tool with server context"""
        if name not in self.tool_handlers:
            raise ValueError(f"Unknown tool: {name}")
        # Pass self as first argument
        return await self.tool_handlers[name](self, **arguments)


async def demo_stateful_server():
    """Demo 2: Stateful server with data persistence"""
    print("\n" + "=" * 70)
    print("Demo 2: Stateful MCP Server")
    print("=" * 70)
    
    # Create server
    server = StatefulMCPServer("counter-server")
    
    # Register tools that use state
    @server.tool("increment", "Increment a counter")
    async def increment(self, counter_name: str) -> int:
        current = self.data_store.get(counter_name, 0)
        new_value = current + 1
        self.data_store[counter_name] = new_value
        return new_value
    
    @server.tool("get_counter", "Get counter value")
    async def get_counter(self, counter_name: str) -> int:
        return self.data_store.get(counter_name, 0)
    
    @server.tool("reset_counter", "Reset a counter")
    async def reset_counter(self, counter_name: str) -> str:
        self.data_store[counter_name] = 0
        return f"Counter '{counter_name}' reset to 0"
    
    # Use the stateful server
    print("\n⚙️  Using Stateful Server:")
    
    # Increment counter multiple times
    for i in range(3):
        result = await server.call_tool("increment", {"counter_name": "visits"})
        print(f"   Increment {i+1}: visits = {result}")
    
    # Get counter value
    value = await server.call_tool("get_counter", {"counter_name": "visits"})
    print(f"   Current value: {value}")
    
    # Reset counter
    msg = await server.call_tool("reset_counter", {"counter_name": "visits"})
    print(f"   {msg}")
    
    # Verify reset
    value = await server.call_tool("get_counter", {"counter_name": "visits"})
    print(f"   After reset: {value}")
    
    print("\n✅ Stateful server demo complete!")


# ============================================================================
# Demo 3: Server with Validation
# ============================================================================

class ValidatingMCPServer:
    """MCP server with input validation"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.tool_handlers = {}
    
    def tool(self, name: str, description: str, validator=None):
        """Register a tool with optional validator"""
        def decorator(func):
            self.tools[name] = {
                "name": name,
                "description": description,
                "validator": validator
            }
            self.tool_handlers[name] = func
            return func
        return decorator
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Call a tool with validation"""
        if name not in self.tool_handlers:
            raise ValueError(f"Unknown tool: {name}")
        
        # Run validator if present
        tool_info = self.tools[name]
        if tool_info.get("validator"):
            validator = tool_info["validator"]
            error = validator(arguments)
            if error:
                raise ValueError(f"Validation error: {error}")
        
        return await self.tool_handlers[name](**arguments)


async def demo_validating_server():
    """Demo 3: Server with input validation"""
    print("\n" + "=" * 70)
    print("Demo 3: Server with Validation")
    print("=" * 70)
    
    # Create server
    server = ValidatingMCPServer("user-server")
    
    # Validators
    def validate_create_user(args):
        """Validate user creation arguments"""
        name = args.get("name", "")
        email = args.get("email", "")
        age = args.get("age", 0)
        
        if not name or len(name) < 2:
            return "Name must be at least 2 characters"
        if "@" not in email:
            return "Invalid email address"
        if age < 0 or age > 150:
            return "Age must be between 0 and 150"
        return None
    
    # Register tool with validator
    @server.tool(
        "create_user",
        "Create a new user",
        validator=validate_create_user
    )
    async def create_user(name: str, email: str, age: int) -> str:
        return json.dumps({
            "success": True,
            "user": {"name": name, "email": email, "age": age}
        })
    
    # Test valid input
    print("\n✅ Test 1: Valid Input")
    try:
        result = await server.call_tool("create_user", {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30
        })
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test invalid inputs
    print("\n❌ Test 2: Invalid Name")
    try:
        await server.call_tool("create_user", {
            "name": "A",
            "email": "alice@example.com",
            "age": 30
        })
    except ValueError as e:
        print(f"   Caught: {e}")
    
    print("\n❌ Test 3: Invalid Email")
    try:
        await server.call_tool("create_user", {
            "name": "Alice",
            "email": "invalid-email",
            "age": 30
        })
    except ValueError as e:
        print(f"   Caught: {e}")
    
    print("\n❌ Test 4: Invalid Age")
    try:
        await server.call_tool("create_user", {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 200
        })
    except ValueError as e:
        print(f"   Caught: {e}")
    
    print("\n✅ Validation demo complete!")


# ============================================================================
# Demo 4: Server with Resources
# ============================================================================

class ResourceMCPServer:
    """MCP server with resources"""
    
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        self.tool_handlers = {}
        self.resources = {}
        self.resource_handlers = {}
    
    def tool(self, name: str, description: str):
        """Register a tool"""
        def decorator(func):
            self.tools[name] = {"name": name, "description": description}
            self.tool_handlers[name] = func
            return func
        return decorator
    
    def resource(self, uri: str, description: str):
        """Register a resource"""
        def decorator(func):
            self.resources[uri] = {
                "uri": uri,
                "description": description
            }
            self.resource_handlers[uri] = func
            return func
        return decorator
    
    async def list_resources(self):
        """List available resources"""
        return [
            {
                "uri": uri,
                "name": uri.split("/")[-1],
                "description": info["description"]
            }
            for uri, info in self.resources.items()
        ]
    
    async def read_resource(self, uri: str):
        """Read a resource"""
        if uri not in self.resource_handlers:
            raise ValueError(f"Unknown resource: {uri}")
        return await self.resource_handlers[uri]()


async def demo_resources():
    """Demo 4: Server with resources"""
    print("\n" + "=" * 70)
    print("Demo 4: Server with Resources")
    print("=" * 70)
    
    # Create server
    server = ResourceMCPServer("data-server")
    
    # Register resources
    @server.resource("config://settings", "Application settings")
    async def get_settings():
        return json.dumps({
            "theme": "dark",
            "language": "en",
            "notifications": True
        })
    
    @server.resource("data://stats", "Server statistics")
    async def get_stats():
        return json.dumps({
            "uptime": "2h 15m",
            "requests": 1523,
            "errors": 3
        })
    
    @server.resource("info://version", "Server version info")
    async def get_version():
        return json.dumps({
            "version": "1.0.0",
            "build": "2024-01-15",
            "api_version": "v1"
        })
    
    # List resources
    print("\n📋 Available Resources:")
    resources = await server.list_resources()
    for resource in resources:
        print(f"   - {resource['uri']}: {resource['description']}")
    
    # Read resources
    print("\n📖 Reading Resources:")
    
    for uri in ["config://settings", "data://stats", "info://version"]:
        content = await server.read_resource(uri)
        print(f"\n   {uri}:")
        print(f"   {content}")
    
    print("\n✅ Resources demo complete!")


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("MCP Server Building Demo")
    print("=" * 70)
    
    try:
        await demo_simple_server()
        await demo_stateful_server()
        await demo_validating_server()
        await demo_resources()
        
        print("\n" + "=" * 70)
        print("All demos completed!")
        print("=" * 70)
        print("\nKey Concepts:")
        print("✅ Tool registration and handling")
        print("✅ Stateful vs stateless servers")
        print("✅ Input validation")
        print("✅ Resource providers")
        print("✅ Error handling")
        print("\nNext: See server.py for complete implementation")
        print("      See challenge.py to build your own server")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
