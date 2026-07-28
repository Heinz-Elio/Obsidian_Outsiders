# Local RAG scaffold

This project indexes the Markdown notes under `Setting/` into Qdrant and exposes
read-only retrieval tools through MCP.

## Local services

Start Ollama and pull an embedding model:

```powershell
ollama pull nomic-embed-text
```

Start Qdrant on `localhost:6333`, then install dependencies with Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Build or refresh the index:

```powershell
.\.venv\Scripts\python.exe -m app.indexer
```

Run the MCP server over stdio:

```powershell
.\.venv\Scripts\python.exe mcp_server.py
```

The server exposes:

- `search_knowledge(query, top_k)`: semantic search with source metadata
- `get_document(path)`: read one relative Markdown source
- `list_sources(folder)`: list eligible Markdown sources

The current indexer uses deterministic chunk IDs, so rerunning it updates
existing chunks. It does not yet delete stale chunks for deleted or shortened
documents.
