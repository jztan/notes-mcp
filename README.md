# Notes MCP Server

A sample MCP (Model Context Protocol) server that manages notes in SQLite, built with [FastMCP](https://github.com/jlowin/fastmcp). Companion repo for my blog post [How to Build an MCP Server in Python (Step-by-Step)](https://blog.jztan.com/how-to-build-an-mcp-server-in-python-step-by-step/).

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

## Tests

```bash
pytest
```
