"""
Lesson 14 Challenge: Build a TODO List MCP Server

Create a complete MCP server for managing TODO tasks with persistent storage.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class Task:
    """Task data model"""
    id: str
    title: str
    description: str
    status: str  # "pending" or "completed"
    created_at: str
    completed_at: Optional[str] = None


# ============================================================================
# Challenge: Implement TODOMCPServer
# ============================================================================

class TODOMCPServer:
    """
    TODO List MCP Server
    
    TODO: Implement the following:
    1. Tool registration system
    2. Task storage (in-memory + JSON file)
    3. Tool handlers for CRUD operations
    4. Input validation
    5. Error handling
    """
    
    def __init__(self, name: str = "todo-server", storage_file: str = "tasks.json"):
        self.name = name
        self.version = "1.0.0"
        self.storage_file = storage_file
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_handlers: Dict[str, callable] = {}
        self.tasks: Dict[str, Task] = {}
        
        # TODO: Load tasks from storage
        # self._load_tasks()
    
    def _load_tasks(self):
        """
        Load tasks from JSON file.
        
        TODO:
        - Check if storage file exists
        - Read JSON data
        - Convert to Task objects
        - Store in self.tasks dict
        """
        # TODO: Implement task loading
        pass
    
    def _save_tasks(self):
        """
        Save tasks to JSON file.
        
        TODO:
        - Convert Task objects to dicts
        - Write to JSON file
        - Handle errors
        """
        # TODO: Implement task saving
        pass
    
    def tool(self, name: str, description: str):
        """
        Decorator to register a tool.
        
        TODO:
        - Store tool metadata in self.tools
        - Store handler function in self.tool_handlers
        - Return decorator function
        """
        def decorator(func):
            # TODO: Register tool
            # self.tools[name] = {...}
            # self.tool_handlers[name] = func
            return func
        return decorator
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools.
        
        TODO:
        - Return list of tool metadata
        """
        # TODO: Implement
        return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool by name with arguments.
        
        TODO:
        - Validate tool exists
        - Call handler function
        - Format response
        - Handle errors
        """
        # TODO: Implement tool calling
        return {
            "content": [{
                "type": "text",
                "text": "Tool calling not implemented"
            }]
        }


# ============================================================================
# TODO: Implement Tool Handlers
# ============================================================================

# Create server instance
server = TODOMCPServer()


# TODO: Implement add_task tool
@server.tool("add_task", "Add a new task to the TODO list")
async def add_task(self, title: str, description: str = "") -> str:
    """
    Add a new task.
    
    TODO:
    - Validate title (not empty)
    - Generate unique task ID
    - Create Task object
    - Store in self.tasks
    - Save to file
    - Return success response
    """
    # TODO: Implement
    return json.dumps({"error": "Not implemented"})


# TODO: Implement list_tasks tool
@server.tool("list_tasks", "List all tasks, optionally filtered by status")
async def list_tasks(self, status: str = "all") -> str:
    """
    List tasks.
    
    TODO:
    - Validate status parameter
    - Filter tasks by status
    - Format as JSON response
    - Return task list
    """
    # TODO: Implement
    return json.dumps({"error": "Not implemented"})


# TODO: Implement complete_task tool
@server.tool("complete_task", "Mark a task as completed")
async def complete_task(self, task_id: str) -> str:
    """
    Complete a task.
    
    TODO:
    - Validate task exists
    - Check if already completed
    - Update status
    - Set completed_at timestamp
    - Save to file
    - Return success response
    """
    # TODO: Implement
    return json.dumps({"error": "Not implemented"})


# TODO: Implement delete_task tool
@server.tool("delete_task", "Delete a task from the TODO list")
async def delete_task(self, task_id: str) -> str:
    """
    Delete a task.
    
    TODO:
    - Validate task exists
    - Remove from self.tasks
    - Save to file
    - Return success response
    """
    # TODO: Implement
    return json.dumps({"error": "Not implemented"})


# TODO: Implement update_task tool
@server.tool("update_task", "Update a task's title and/or description")
async def update_task(
    self,
    task_id: str,
    title: str = None,
    description: str = None
) -> str:
    """
    Update a task.
    
    TODO:
    - Validate task exists
    - Update title if provided
    - Update description if provided
    - Save to file
    - Return updated task
    """
    # TODO: Implement
    return json.dumps({"error": "Not implemented"})


# ============================================================================
# Test Client
# ============================================================================

class TestClient:
    """Simple client for testing the server"""
    
    def __init__(self, server):
        self.server = server
    
    async def test_server(self):
        """Run tests on the server"""
        print("=" * 70)
        print("Testing TODO MCP Server")
        print("=" * 70)
        
        # List tools
        print("\n📋 Test 1: List Tools")
        tools = await self.server.list_tools()
        if not tools:
            print("❌ No tools found - implement list_tools()")
            return False
        print(f"✅ Found {len(tools)} tools")
        
        # Add tasks
        print("\n📋 Test 2: Add Tasks")
        result = await self.server.call_tool("add_task", {
            "title": "Test task",
            "description": "This is a test"
        })
        data = json.loads(result["content"][0]["text"])
        if "error" in data:
            print(f"❌ {data['error']}")
            return False
        print("✅ Task added successfully")
        
        # List tasks
        print("\n📋 Test 3: List Tasks")
        result = await self.server.call_tool("list_tasks", {"status": "all"})
        data = json.loads(result["content"][0]["text"])
        if "error" in data:
            print(f"❌ {data['error']}")
            return False
        print(f"✅ Found {data.get('count', 0)} tasks")
        
        print("\n" + "=" * 70)
        print("Server implementation incomplete!")
        print("=" * 70)
        print("\nTODO:")
        print("1. Implement _load_tasks() and _save_tasks()")
        print("2. Implement tool registration in tool() decorator")
        print("3. Implement list_tools()")
        print("4. Implement call_tool()")
        print("5. Implement all tool handlers (add, list, complete, delete, update)")
        print("\nSee solution.py for reference implementation")
        
        return True


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run the challenge"""
    try:
        client = TestClient(server)
        await client.test_server()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
