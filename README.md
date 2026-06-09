# Notes MCP Server

A sample MCP (Model Context Protocol) server that manages notes in SQLite, built with [FastMCP 3](https://gofastmcp.com). Companion repo for two blog posts:

- Part 1: [How to Build an MCP Server in Python (Step-by-Step)](https://blog.jztan.com/how-to-build-an-mcp-server-in-python-step-by-step/?utm_source=github&utm_medium=readme&utm_campaign=notes-mcp) — the local STDIO server.
- Part 2: [How to Deploy a Python MCP Server: Remote HTTP, Auth, and Docker](https://blog.jztan.com/how-to-deploy-a-python-mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=notes-mcp) — taking it remote.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Local (STDIO)

```bash
python server.py
```

This initializes the SQLite database and starts the MCP server over STDIO, the transport Claude Desktop and most IDE clients spawn locally.

### Remote (HTTP + auth)

Set a bearer token and run over HTTP:

```bash
MCP_TOKEN="your-secret-token" MCP_TRANSPORT=http python server.py
```

The server listens on `http://0.0.0.0:8000/mcp`. Clients must send `Authorization: Bearer your-secret-token`. Without `MCP_TOKEN`, no auth gate is applied (fine for local STDIO, not for a public server).

| Env var | Default | Purpose |
|---------|---------|---------|
| `MCP_TOKEN` | _unset_ | Bearer token; enables the auth gate when set |
| `MCP_TRANSPORT` | `stdio` | Set to `http` to serve remotely |
| `HOST` | `0.0.0.0` | HTTP bind host |
| `PORT` | `8000` | HTTP bind port |

> `StaticTokenVerifier` stores tokens in plaintext and is meant for development or a single-user server behind a VPN. For a public, multi-tenant server, swap `build_auth()` for `JWTVerifier` or OAuth 2.1 — the tools do not change.

### Docker

```bash
docker build -t notes-mcp .
docker run -d -p 8000:8000 -e MCP_TOKEN="your-secret-token" --name notes-mcp notes-mcp
```

Run it behind a reverse proxy that terminates TLS (set `proxy_buffering off` and a generous `proxy_read_timeout` for the streaming endpoint). For horizontal scaling, run the ASGI app under a process manager: `uvicorn server:app --host 0.0.0.0 --port 8000` (`create_app()` wires `init_db()` into the startup lifespan).

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
