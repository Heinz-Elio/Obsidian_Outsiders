# Local RAG scaffold

This project indexes the Markdown notes under `Setting/` into Qdrant and exposes
read-only retrieval tools through MCP.

## Prerequisites

- Python 3.11
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/download/windows)

## Install

From the project root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Start Qdrant

Use a persistent local folder so data survives container restarts:

```powershell
docker rm -f qdrant 2>$null
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v "${PWD}\qdrant_storage:/qdrant/storage" qdrant/qdrant
```

Verify:

```powershell
Invoke-RestMethod http://127.0.0.1:6333/
Invoke-RestMethod http://127.0.0.1:6333/collections
```

Useful commands:

```powershell
docker start qdrant
docker stop qdrant
docker logs qdrant
```

Notes:

- Storage lives in `./qdrant_storage` and is gitignored.
- Do not commit Qdrant storage through Git. Copy it as a zip/snapshot if needed.
- Keep Qdrant versions aligned across machines when copying storage.

## Start Ollama

```powershell
ollama --version
ollama pull nomic-embed-text
ollama list
```

Quick embed smoke test:

```powershell
# GPU path (fails on some old CUDA setups)
$body = @{ model = "nomic-embed-text"; input = "test" } | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:11434/api/embed -Method Post -Body $body -ContentType "application/json"

# CPU path (works when CUDA crashes)
$body = @{ model = "nomic-embed-text"; input = "test"; options = @{ num_gpu = 0 } } | ConvertTo-Json -Depth 5
Invoke-RestMethod http://127.0.0.1:11434/api/embed -Method Post -Body $body -ContentType "application/json"
```

This project’s `config.yaml` sets `embedding.num_gpu: 0` so the indexer/MCP use CPU embeddings by default.
Remove that key on a healthy GPU machine (for example a 3050 Ti) to allow GPU offload.

Optional CPU-only model:

```powershell
@"
FROM nomic-embed-text
PARAMETER num_gpu 0
"@ | Set-Content Modelfile.cpu -Encoding ascii
ollama create nomic-embed-text-cpu -f Modelfile.cpu
```

## Build the index

With Qdrant and Ollama running:

```powershell
.\.venv\Scripts\python.exe -m app.indexer
```

Confirm the collection exists:

```powershell
Invoke-RestMethod http://127.0.0.1:6333/collections
```

Expected collection name: `obsidian` (see `config.yaml`).

## Run the MCP server

stdio server (for Cursor local MCP):

```powershell
.\.venv\Scripts\python.exe mcp_server.py
```

This process waits on stdin/stdout. It does not serve HTTP by itself.
A HTTP 200 from `http://127.0.0.1:6333/` is Qdrant, not MCP.

### Cursor MCP config example

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "G:\\RAG_test\\.venv\\Scripts\\python.exe",
      "args": ["G:\\RAG_test\\mcp_server.py"],
      "cwd": "G:\\RAG_test"
    }
  }
}
```

`mcp_server.py` and `load_config()` resolve `config.yaml` from the project root
even if Cursor starts the process with a different working directory.
Absolute paths in the MCP config are still recommended.

## MCP tools

- `search_knowledge(query, top_k)`: semantic search with source metadata
- `get_document(path)`: read one relative Markdown source
- `list_sources(folder)`: list eligible Markdown sources

The indexer uses deterministic chunk IDs, so rerunning it updates existing chunks.
It does not yet delete stale chunks for deleted or shortened documents.

## Testing instructions

Run these from the project root after Qdrant and Ollama are up.

### 1. Empty Qdrant smoke test

Start Qdrant with an empty or new `qdrant_storage`, then:

```powershell
.\.venv\Scripts\python.exe -c "import mcp_server; print('import_ok')"
.\.venv\Scripts\python.exe -c "import mcp_server; print(mcp_server.list_sources('IU7')[:200])"
```

Expected:

- `import_ok`
- `list_sources` returns JSON paths under `Setting/`
- `search_knowledge` may fail with collection-not-found until you index

### 2. Small fake-embedding test (no Ollama GPU)

If Ollama CUDA fails, use deterministic fake embeddings for a tiny pipeline smoke test:

```powershell
.\.venv\Scripts\python.exe test_embeddings.py --limit-documents 5 --query "星降神臨"
```

This uses `config.test.yaml` (`provider: fake`, collection `obsidian_test`).
Expected: `fake_embed_ok`, indexed chunks > 0, and search hits.

For Cursor MCP with the same fake provider, temporarily set `config.yaml` embedding provider to `fake`, or point the server at `config.test.yaml`.

### 3. Indexing test (real Ollama embeddings)

```powershell
.\.venv\Scripts\python.exe -m app.indexer
Invoke-RestMethod http://127.0.0.1:6333/collections/obsidian
```

Expected: collection `obsidian` exists and point count > 0.

### 4. Search test

```powershell
.\.venv\Scripts\python.exe -c "import mcp_server; print(mcp_server.search_knowledge('星降神臨', 3))"
```

Expected: JSON chunks with `source_path`, `text`, and `score`.

### 5. Document read test

```powershell
.\.venv\Scripts\python.exe -c "import mcp_server; print(mcp_server.get_document('IU7/05_srune/原初大法術．星降神臨.md')[:300])"
```

Expected: Markdown note content.

### 6. Cursor MCP test

1. Add the MCP config above.
2. Restart Cursor MCP / reload window.
3. Confirm tools appear: `search_knowledge`, `get_document`, `list_sources`.
4. Call `list_sources` with folder `IU7`.
5. Call `search_knowledge` with a Chinese query from the vault.

### Failure checklist

| Symptom | Likely cause |
|---|---|
| MCP connection fails immediately | Wrong `command`/`cwd`, or import crash |
| `config.yaml` not found | Cursor `cwd` is not project root |
| Qdrant 200 but MCP fails | Confusing Qdrant health with MCP stdio |
| `search_knowledge` HTTP 500 | Ollama embedding/CUDA failure |
| Collection not found | Index not built yet |
| Empty search results | Wrong collection, or vault path mismatch |

## Novel formatting conversion

`format_converter.py` converts explicit ruby markers and exactly-four-character
fullwidth-dot notation:

```text
{{ruby:漢字|かんじ}}
甲．乙．丙．丁
```

For the whole vault:

```powershell
.\.venv\Scripts\python.exe convert_vault.py
```

It reads `Setting/` and writes converted files to `rendered/`.

For one file:

```powershell
.\.venv\Scripts\python.exe format_converter.py input.md output.md
```

CSS for emphasis dots:

```css
.bouten {
  -webkit-text-emphasis: filled dot;
  text-emphasis: filled dot;
  text-emphasis-position: under;
}
```

## Selection hotkey conversion

For manual ruby conversion of normalized names:

```text
地對空法力導引飛彈（Sruna homing Surface-to-Air Missile，SSAM）
地對空法力導引飛彈（Sruna homing Surface-to-Air Missile）
```

Run the AutoHotkey script once:

```powershell
convert_selection.ahk
```

Then select text and press `Ctrl+Shift+R`.

CLI test:

```powershell
.\.venv\Scripts\python.exe convert_selection.py "地對空法力導引飛彈（Sruna homing Surface-to-Air Missile，SSAM）"
```
