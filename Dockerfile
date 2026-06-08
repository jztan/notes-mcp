FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8000

# Run over HTTP. init_db() runs first, then the HTTP transport starts.
# Pass the bearer token at runtime:
#   docker run -d -p 8000:8000 -e MCP_TOKEN="your-secret-token" notes-mcp
ENV MCP_TRANSPORT=http
CMD ["python", "server.py"]

# For horizontal scaling, run the ASGI app under a process manager instead:
#   uvicorn server:app --host 0.0.0.0 --port 8000
# create_app() wires init_db() into the app's startup lifespan.
