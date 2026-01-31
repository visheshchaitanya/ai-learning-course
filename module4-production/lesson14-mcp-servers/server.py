"""
Lesson 14: Example MCP Server

A complete example MCP server with multiple tools and resources.
This demonstrates server architecture, tool registration, and best practices.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict


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


@dataclass
class ServerStats:
    """Server statistics"""
    total_calls: int = 0
    tools_called: Dict[str, int] = None
    
    def __post_init__(self):
        if self.tools_called is None:
            self.tools_called = {}


# ============================================================================
# Mock MCP Server Implementation
# ============================================================================

class MCPServer:
    """
    Mock MCP Server for demonstration.
    
    In a real implementation, this would use the actual MCP SDK:
    from mcp.server import Server
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_handlers: Dict[str, callable] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.stats = ServerStats()
        self.storage_file = "tasks.json"
        self.tasks: Dict[str, Task] = {}
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from storage"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = {
                        task_id: Task(**task_data)
                        for task_id, task_data in data.items()
                    }
                print(f"📂 Loaded {len(self.tasks)} tasks from storage")
            except Exception as e:
                print(f"⚠️  Error loading tasks: {e}")
                self.tasks = {}
        else:
            self.tasks = {}
    
    def _save_tasks(self):
        """Save tasks to storage"""
        try:
            data = {
                task_id: asdict(task)
                for task_id, task in self.tasks.items()
            }
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving tasks: {e}")
    
    def tool(self, name: str = None, description: str = None):
        """Decorator to register a tool"""
        def decorator(func):
            tool_name = name or func.__name__
            tool_desc = description or func.__doc__ or "No description"
            
            # Register tool
            self.tools[tool_name] = {
                "name": tool_name,
                "description": tool_desc.strip(),
                "inputSchema": self._generate_schema(func)
            }
            self.tool_handlers[tool_name] = func
            
            return func
        return decorator
    
    def _generate_schema(self, func) -> Dict[str, Any]:
        """Generate JSON Schema from function signature"""
        import inspect
        sig = inspect.signature(func)
        
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            param_type = "string"  # Default
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"
                elif param.annotation == dict:
                    param_type = "object"
            
            properties[param_name] = {"type": param_type}
            
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
    
    def resource(self, uri_pattern: str):
        """Decorator to register a resource"""
        def decorator(func):
            self.resources[uri_pattern] = {
                "uri": uri_pattern,
                "handler": func
            }
            return func
        return decorator
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return list(self.tools.values())
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool"""
        if name not in self.tool_handlers:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error: Unknown tool '{name}'"
                }],
                "isError": True
            }
        
        # Update stats
        self.stats.total_calls += 1
        self.stats.tools_called[name] = self.stats.tools_called.get(name, 0) + 1
        
        try:
            handler = self.tool_handlers[name]
            result = await handler(self, **arguments)
            
            return {
                "content": [{
                    "type": "text",
                    "text": str(result)
                }]
            }
        except Exception as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error: {str(e)}"
                }],
                "isError": True
            }
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources"""
        return [
            {
                "uri": uri,
                "name": uri.split("/")[-1],
                "mimeType": "application/json",
                "description": f"Resource at {uri}"
            }
            for uri in self.resources.keys()
        ]


# ============================================================================
# Create Server Instance
# ============================================================================

server = MCPServer("task-manager-server", "1.0.0")


# ============================================================================
# Tool Implementations
# ============================================================================

@server.tool(
    name="add_task",
    description="Add a new task to the TODO list"
)
async def add_task(self, title: str, description: str = "") -> str:
    """Add a new task"""
    import uuid
    
    # Validate input
    if not title or len(title.strip()) == 0:
        raise ValueError("Title cannot be empty")
    
    # Create task
    task_id = str(uuid.uuid4())[:8]
    task = Task(
        id=task_id,
        title=title.strip(),
        description=description.strip(),
        status="pending",
        created_at=datetime.now().isoformat()
    )
    
    # Store task
    self.tasks[task_id] = task
    self._save_tasks()
    
    return json.dumps({
        "success": True,
        "task_id": task_id,
        "message": f"Task '{title}' added successfully"
    })


@server.tool(
    name="list_tasks",
    description="List all tasks, optionally filtered by status"
)
async def list_tasks(self, status: str = "all") -> str:
    """List tasks"""
    # Validate status
    if status not in ["all", "pending", "completed"]:
        raise ValueError("Status must be 'all', 'pending', or 'completed'")
    
    # Filter tasks
    if status == "all":
        tasks = list(self.tasks.values())
    else:
        tasks = [t for t in self.tasks.values() if t.status == status]
    
    # Format output
    if not tasks:
        return json.dumps({
            "count": 0,
            "tasks": [],
            "message": f"No {status} tasks found"
        })
    
    return json.dumps({
        "count": len(tasks),
        "tasks": [asdict(t) for t in tasks]
    }, indent=2)


@server.tool(
    name="complete_task",
    description="Mark a task as completed"
)
async def complete_task(self, task_id: str) -> str:
    """Complete a task"""
    if task_id not in self.tasks:
        raise ValueError(f"Task '{task_id}' not found")
    
    task = self.tasks[task_id]
    
    if task.status == "completed":
        return json.dumps({
            "success": False,
            "message": f"Task '{task.title}' is already completed"
        })
    
    task.status = "completed"
    task.completed_at = datetime.now().isoformat()
    self._save_tasks()
    
    return json.dumps({
        "success": True,
        "message": f"Task '{task.title}' marked as completed"
    })


@server.tool(
    name="delete_task",
    description="Delete a task from the TODO list"
)
async def delete_task(self, task_id: str) -> str:
    """Delete a task"""
    if task_id not in self.tasks:
        raise ValueError(f"Task '{task_id}' not found")
    
    task = self.tasks[task_id]
    title = task.title
    del self.tasks[task_id]
    self._save_tasks()
    
    return json.dumps({
        "success": True,
        "message": f"Task '{title}' deleted successfully"
    })


@server.tool(
    name="update_task",
    description="Update a task's title and/or description"
)
async def update_task(
    self,
    task_id: str,
    title: str = None,
    description: str = None
) -> str:
    """Update a task"""
    if task_id not in self.tasks:
        raise ValueError(f"Task '{task_id}' not found")
    
    task = self.tasks[task_id]
    
    if title:
        task.title = title.strip()
    if description is not None:
        task.description = description.strip()
    
    self._save_tasks()
    
    return json.dumps({
        "success": True,
        "message": f"Task updated successfully",
        "task": asdict(task)
    })


@server.tool(
    name="get_stats",
    description="Get server statistics"
)
async def get_stats(self) -> str:
    """Get server statistics"""
    return json.dumps({
        "server": self.name,
        "version": self.version,
        "total_tasks": len(self.tasks),
        "pending_tasks": len([t for t in self.tasks.values() if t.status == "pending"]),
        "completed_tasks": len([t for t in self.tasks.values() if t.status == "completed"]),
        "total_tool_calls": self.stats.total_calls,
        "tools_called": self.stats.tools_called
    }, indent=2)


# ============================================================================
# Server Runner
# ============================================================================

async def run_server():
    """Run the MCP server"""
    print("=" * 70)
    print(f"🚀 Starting {server.name} v{server.version}")
    print("=" * 70)
    
    # List available tools
    tools = await server.list_tools()
    print(f"\n📋 Available Tools ({len(tools)}):")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    print("\n✅ Server ready!")
    print("   Connect clients to start using tools")
    print("=" * 70)
    
    # In a real implementation, this would start the transport layer:
    # async with stdio_server() as (read, write):
    #     await server.run(read, write)
    
    # For demo, just keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Server shutting down...")


# ============================================================================
# Main
# ============================================================================

def main():
    """Main entry point"""
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
