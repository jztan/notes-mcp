# Notes MCP Server

A sample MCP (Model Context Protocol) server that manages notes in SQLite, built with [FastMCP 3](https://gofastmcp.com). Companion repo for my blog post [How to Build an MCP Server in Python (Step-by-Step) [Updated for FastMCP 3.0]](https://blog.jztan.com/how-to-build-an-mcp-server-in-python-step-by-step/).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python server.py
```

This initializes the SQLite database and starts the MCP server.

## MCP Surface Area

| Type | Name | Description |
|------|------|-------------|
| Tool | `add_note` | Create a new note |
| Tool | `search_notes` | Search notes by title or content |
| Tool | `delete_note` | Delete a note by ID |
| Resource | `note://{note_id}` | Read a single note |
| Resource | `note://all` | List all notes |
| Prompt | `summarize_notes` | Summarize all notes (brief or detailed) |

## Tests

```bash
pytest
```
