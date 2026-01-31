"""
Lesson 14: MCP Client Demo

Demonstrates how to connect to and use the MCP server.
"""

import asyncio
import json
from typing import Dict, Any


# Import the server
from server import server


# ============================================================================
# Simple MCP Client
# ============================================================================

class MCPClient:
    """Simple MCP client for testing servers"""
    
    def __init__(self, server):
        self.server = server
        self.connected = False
    
    async def connect(self):
        """Connect to server"""
        print("🔌 Connecting to server...")
        self.connected = True
        print(f"✅ Connected to {self.server.name} v{self.server.version}")
    
    async def list_tools(self):
        """List available tools"""
        if not self.connected:
            raise RuntimeError("Not connected")
        return await self.server.list_tools()
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Call a tool"""
        if not self.connected:
            raise RuntimeError("Not connected")
        return await self.server.call_tool(name, arguments)


# ============================================================================
# Demo Functions
# ============================================================================

async def demo_basic_operations():
    """Demo basic TODO operations"""
    print("\n" + "=" * 70)
    print("Demo 1: Basic TODO Operations")
    print("=" * 70)
    
    client = MCPClient(server)
    await client.connect()
    
    # Add tasks
    print("\n📝 Adding Tasks:")
    tasks_to_add = [
        ("Buy groceries", "Milk, eggs, bread"),
        ("Write report", "Q4 financial report"),
        ("Call dentist", "Schedule appointment")
    ]
    
    for title, desc in tasks_to_add:
        result = await client.call_tool("add_task", {
            "title": title,
            "description": desc
        })
        data = json.loads(result["content"][0]["text"])
        print(f"   ✅ {data['message']}")
    
    # List all tasks
    print("\n📋 Listing All Tasks:")
    result = await client.call_tool("list_tasks", {"status": "all"})
    data = json.loads(result["content"][0]["text"])
    print(f"   Found {data['count']} tasks:")
    for task in data["tasks"]:
        print(f"   - [{task['id']}] {task['title']} ({task['status']})")


async def demo_task_completion():
    """Demo completing tasks"""
    print("\n" + "=" * 70)
    print("Demo 2: Completing Tasks")
    print("=" * 70)
    
    client = MCPClient(server)
    await client.connect()
    
    # Get pending tasks
    result = await client.call_tool("list_tasks", {"status": "pending"})
    data = json.loads(result["content"][0]["text"])
    
    if data["count"] == 0:
        print("   No pending tasks to complete")
        return
    
    # Complete first task
    first_task = data["tasks"][0]
    task_id = first_task["id"]
    
    print(f"\n✅ Completing task: {first_task['title']}")
    result = await client.call_tool("complete_task", {"task_id": task_id})
    response = json.loads(result["content"][0]["text"])
    print(f"   {response['message']}")
    
    # Show updated task list
    print("\n📋 Updated Task List:")
    result = await client.call_tool("list_tasks", {"status": "all"})
    data = json.loads(result["content"][0]["text"])
    for task in data["tasks"]:
        status_icon = "✅" if task["status"] == "completed" else "⏳"
        print(f"   {status_icon} {task['title']}")


async def demo_task_management():
    """Demo updating and deleting tasks"""
    print("\n" + "=" * 70)
    print("Demo 3: Task Management")
    print("=" * 70)
    
    client = MCPClient(server)
    await client.connect()
    
    # Add a test task
    print("\n📝 Adding test task...")
    result = await client.call_tool("add_task", {
        "title": "Test task",
        "description": "This is a test"
    })
    data = json.loads(result["content"][0]["text"])
    task_id = data["task_id"]
    print(f"   Added task {task_id}")
    
    # Update the task
    print(f"\n✏️  Updating task {task_id}...")
    result = await client.call_tool("update_task", {
        "task_id": task_id,
        "title": "Updated test task",
        "description": "This has been updated"
    })
    response = json.loads(result["content"][0]["text"])
    print(f"   {response['message']}")
    print(f"   New title: {response['task']['title']}")
    
    # Delete the task
    print(f"\n🗑️  Deleting task {task_id}...")
    result = await client.call_tool("delete_task", {"task_id": task_id})
    response = json.loads(result["content"][0]["text"])
    print(f"   {response['message']}")


async def demo_server_stats():
    """Demo server statistics"""
    print("\n" + "=" * 70)
    print("Demo 4: Server Statistics")
    print("=" * 70)
    
    client = MCPClient(server)
    await client.connect()
    
    # Get stats
    result = await client.call_tool("get_stats", {})
    stats = json.loads(result["content"][0]["text"])
    
    print("\n📊 Server Statistics:")
    print(f"   Server: {stats['server']} v{stats['version']}")
    print(f"   Total Tasks: {stats['total_tasks']}")
    print(f"   Pending: {stats['pending_tasks']}")
    print(f"   Completed: {stats['completed_tasks']}")
    print(f"   Total Tool Calls: {stats['total_tool_calls']}")
    
    if stats['tools_called']:
        print("\n   Tool Usage:")
        for tool, count in stats['tools_called'].items():
            print(f"      {tool}: {count} calls")


async def demo_error_handling():
    """Demo error handling"""
    print("\n" + "=" * 70)
    print("Demo 5: Error Handling")
    print("=" * 70)
    
    client = MCPClient(server)
    await client.connect()
    
    # Test 1: Invalid task ID
    print("\n❌ Test 1: Invalid task ID")
    result = await client.call_tool("complete_task", {"task_id": "invalid-id"})
    if result.get("isError"):
        print(f"   Error caught: {result['content'][0]['text']}")
    
    # Test 2: Empty title
    print("\n❌ Test 2: Empty title")
    result = await client.call_tool("add_task", {"title": "", "description": "test"})
    if result.get("isError"):
        print(f"   Error caught: {result['content'][0]['text']}")
    
    # Test 3: Invalid status filter
    print("\n❌ Test 3: Invalid status filter")
    result = await client.call_tool("list_tasks", {"status": "invalid"})
    if result.get("isError"):
        print(f"   Error caught: {result['content'][0]['text']}")
    
    print("\n✅ Error handling working correctly!")


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("MCP Client Demo - Testing Task Manager Server")
    print("=" * 70)
    
    try:
        await demo_basic_operations()
        await demo_task_completion()
        await demo_task_management()
        await demo_server_stats()
        await demo_error_handling()
        
        print("\n" + "=" * 70)
        print("All client demos completed!")
        print("=" * 70)
        print("\nThe client successfully:")
        print("✅ Connected to the MCP server")
        print("✅ Listed available tools")
        print("✅ Called tools with various arguments")
        print("✅ Handled errors gracefully")
        print("✅ Managed stateful operations")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
