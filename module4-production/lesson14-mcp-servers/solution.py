"""
Lesson 14 Solution: Complete TODO List MCP Server

Full implementation with all features.
"""

# The complete solution is in server.py
# This file demonstrates how to use it

import asyncio
from server import server


async def demonstrate_solution():
    """Demonstrate the complete solution"""
    print("=" * 70)
    print("TODO List MCP Server - Complete Solution")
    print("=" * 70)
    
    print("\n📋 Server Features:")
    print("   ✅ Tool registration system")
    print("   ✅ Persistent storage (JSON)")
    print("   ✅ Input validation")
    print("   ✅ Error handling")
    print("   ✅ Statistics tracking")
    
    # List tools
    print("\n🔧 Available Tools:")
    tools = await server.list_tools()
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # Demonstrate CRUD operations
    print("\n" + "=" * 70)
    print("Demonstration: CRUD Operations")
    print("=" * 70)
    
    # Create
    print("\n📝 CREATE: Adding tasks...")
    tasks = [
        ("Complete lesson 14", "Finish MCP server implementation"),
        ("Review code", "Check for bugs and improvements"),
        ("Write tests", "Add unit tests for all tools")
    ]
    
    task_ids = []
    for title, desc in tasks:
        result = await server.call_tool("add_task", {
            "title": title,
            "description": desc
        })
        import json
        data = json.loads(result["content"][0]["text"])
        task_ids.append(data["task_id"])
        print(f"   ✅ Added: {title}")
    
    # Read
    print("\n📖 READ: Listing all tasks...")
    result = await server.call_tool("list_tasks", {"status": "all"})
    data = json.loads(result["content"][0]["text"])
    print(f"   Found {data['count']} tasks:")
    for task in data["tasks"]:
        print(f"      - [{task['id']}] {task['title']}")
    
    # Update
    print("\n✏️  UPDATE: Modifying a task...")
    result = await server.call_tool("update_task", {
        "task_id": task_ids[0],
        "title": "Complete lesson 14 ✓",
        "description": "Finished! Great work!"
    })
    data = json.loads(result["content"][0]["text"])
    print(f"   ✅ Updated: {data['task']['title']}")
    
    # Complete
    print("\n✅ COMPLETE: Marking task as done...")
    result = await server.call_tool("complete_task", {
        "task_id": task_ids[0]
    })
    data = json.loads(result["content"][0]["text"])
    print(f"   {data['message']}")
    
    # Delete
    print("\n🗑️  DELETE: Removing a task...")
    result = await server.call_tool("delete_task", {
        "task_id": task_ids[2]
    })
    data = json.loads(result["content"][0]["text"])
    print(f"   {data['message']}")
    
    # Final state
    print("\n📊 Final State:")
    result = await server.call_tool("list_tasks", {"status": "all"})
    data = json.loads(result["content"][0]["text"])
    for task in data["tasks"]:
        status_icon = "✅" if task["status"] == "completed" else "⏳"
        print(f"   {status_icon} {task['title']}")
    
    # Statistics
    print("\n📈 Server Statistics:")
    result = await server.call_tool("get_stats", {})
    stats = json.loads(result["content"][0]["text"])
    print(f"   Total tasks: {stats['total_tasks']}")
    print(f"   Pending: {stats['pending_tasks']}")
    print(f"   Completed: {stats['completed_tasks']}")
    print(f"   Total tool calls: {stats['total_tool_calls']}")
    
    print("\n" + "=" * 70)
    print("Solution Highlights")
    print("=" * 70)
    print("""
Key Implementation Details:

1. **Data Model**
   - Task dataclass with all required fields
   - Type hints for clarity
   - Optional fields (completed_at)

2. **Storage**
   - JSON file persistence
   - Automatic load on startup
   - Save after each modification
   - Error handling for file operations

3. **Tool Registration**
   - Decorator pattern for clean API
   - Automatic schema generation
   - Handler function mapping

4. **Validation**
   - Input validation (empty titles, invalid status)
   - Task existence checks
   - Proper error messages

5. **Error Handling**
   - Try-catch blocks
   - Meaningful error responses
   - Graceful degradation

6. **Statistics**
   - Track tool usage
   - Count tasks by status
   - Server metadata

7. **Best Practices**
   - Async/await throughout
   - Type hints
   - Docstrings
   - Clean code structure
   - Separation of concerns

See server.py for the complete implementation!
    """)


async def main():
    """Run the solution demonstration"""
    try:
        await demonstrate_solution()
        
        print("\n" + "=" * 70)
        print("Solution completed!")
        print("=" * 70)
        print("\nFiles to review:")
        print("   - server.py: Complete server implementation")
        print("   - client_demo.py: Client usage examples")
        print("   - demo.py: Server building patterns")
        print("\nNext steps:")
        print("   - Extend with more features (tags, priorities, due dates)")
        print("   - Add authentication")
        print("   - Implement rate limiting")
        print("   - Add resource providers")
        print("   - Deploy with real MCP transport (stdio/HTTP)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
