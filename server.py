import aiosqlite
import asyncio
from contextlib import asynccontextmanager
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from typing import Annotated
from uuid import uuid4
from fastmcp.exceptions import ToolError

DB_PATH = "notes.db"

@asynccontextmanager
async def get_db():
    """Provide a database connection with auto-cleanup."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()

mcp = FastMCP("Notes")

@mcp.tool
async def add_note(
    title: Annotated[str, "Title of the note"],
    content: Annotated[str, "Note body text"],
    db=Depends(get_db),
) -> dict:
    """Create a new note and return it."""
    note_id = uuid4().hex[:8]
    await db.execute(
        "INSERT INTO notes (id, title, content) VALUES (?, ?, ?)",
        (note_id, title, content),
    )
    await db.commit()
    return {"id": note_id, "title": title, "content": content}

@mcp.tool
async def search_notes(
    query: Annotated[str, "Text to search for in titles and content"],
    db=Depends(get_db),
) -> list[dict]:
    """Search notes by title or content."""
    cursor = await db.execute(
        "SELECT id, title, content FROM notes "
        "WHERE title LIKE ? OR content LIKE ?",
        (f"%{query}%", f"%{query}%"),
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

@mcp.tool
async def delete_note(
    note_id: Annotated[str, "ID of the note to delete"],
    db=Depends(get_db),
) -> str:
    """Delete a note by ID."""
    cursor = await db.execute(
        "DELETE FROM notes WHERE id = ?", (note_id,)
    )
    await db.commit()
    if cursor.rowcount == 0:
        raise ToolError(f"Note '{note_id}' not found.")
    return f"Deleted note '{note_id}'."

@mcp.resource("note://{note_id}")
async def get_note(note_id: str, db=Depends(get_db)) -> dict:
    """Read a specific note by ID."""
    cursor = await db.execute(
        "SELECT id, title, content FROM notes WHERE id = ?", (note_id,)
    )
    row = await cursor.fetchone()
    if row is None:
        raise ToolError(f"Note '{note_id}' not found.")
    return dict(row)

@mcp.resource("note://all")
async def list_notes(db=Depends(get_db)) -> list[dict]:
    """List all notes with their IDs and titles."""
    cursor = await db.execute("SELECT id, title FROM notes")
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]

@mcp.prompt
async def summarize_notes(
    style: Annotated[str, "Summary style: 'brief' or 'detailed'"] = "brief",
    db=Depends(get_db),
) -> str:
    """Create a prompt to summarize all stored notes."""
    cursor = await db.execute("SELECT title, content FROM notes")
    rows = await cursor.fetchall()

    if not rows:
        return "There are no notes to summarize."

    note_list = "\n".join(
        f"- **{row['title']}**: {row['content']}" for row in rows
    )

    if style == "detailed":
        return (
            f"Here are all my notes:\n\n{note_list}\n\n"
            "Please provide a detailed summary of each note, "
            "highlighting key themes and connections between them."
        )
    return (
        f"Here are all my notes:\n\n{note_list}\n\n"
        "Please provide a brief, one-paragraph summary."
    )

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """
        )
        await db.commit()

if __name__ == "__main__":
    asyncio.run(init_db())
    mcp.run()
