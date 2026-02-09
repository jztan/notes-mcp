# test_server.py
import pytest
from fastmcp.client import Client
from fastmcp.exceptions import ToolError
from server import mcp, init_db

@pytest.fixture(autouse=True)
async def setup_db(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    db_path = str(tmp_path / "test_notes.db")
    monkeypatch.setattr("server.DB_PATH", db_path)
    await init_db()

@pytest.fixture
async def client():
    async with Client(transport=mcp) as c:
        yield c

async def test_add_and_search(client):
    """Test creating a note and finding it via search."""
    result = await client.call_tool(
        "add_note",
        {"title": "Meeting Notes", "content": "Discuss Q1 roadmap"},
    )
    assert "Meeting Notes" in str(result)

    results = await client.call_tool(
        "search_notes",
        {"query": "roadmap"},
    )
    assert "Q1 roadmap" in str(results)

async def test_delete_nonexistent(client):
    """Deleting a missing note should return an error."""
    with pytest.raises(ToolError, match="not found"):
        await client.call_tool(
            "delete_note",
            {"note_id": "doesnotexist"},
        )

async def test_list_tools(client):
    """Verify all expected tools are registered."""
    tools = await client.list_tools()
    tool_names = {t.name for t in tools}
    assert "add_note" in tool_names
    assert "search_notes" in tool_names
    assert "delete_note" in tool_names
