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

The default command is incremental. It hashes the Markdown sources and only
chunks, embeds, and replaces new or changed notes; removed notes are deleted
from Qdrant. The first run after enabling incremental indexing performs one
complete rebuild and writes a per-collection manifest under
`qdrant_storage/`.

Force a complete rebuild when required:

```powershell
.\.venv\Scripts\python.exe -m app.indexer --full
```

After indexing changes, restart the MCP server so its in-memory document graph
and lexical entity index reflect the updated notes.

Confirm the collection exists:

```powershell
Invoke-RestMethod http://127.0.0.1:6333/collections
```

Expected collection name: `obsidian` (see `config.yaml`).

## Run the MCP server

The server supports stdio and HTTP from the same entry point. It defaults to
stdio for Cursor.

### stdio (Cursor)

```powershell
.\.venv\Scripts\python.exe .\app\mcp_server.py
```

This process waits on stdin/stdout.
A HTTP 200 from `http://127.0.0.1:6333/` is Qdrant, not MCP.

Cursor MCP config example (replace both absolute paths on each PC):

```json
{
  "mcpServers": {
    "obsidian-rag": {
      "command": "G:\\RAG_test\\.venv\\Scripts\\python.exe",
      "args": ["G:\\RAG_test\\app\\mcp_server.py"]
    }
  }
}
```

The script and `load_config()` resolve the project root and `config.yaml` from
their own file locations, so they do not depend on Cursor preserving `cwd`.

### Streamable HTTP (local Obsidian plugin)

Run this on the PC where Obsidian is installed:

```powershell
$env:OBSIDIAN_RAG_TRANSPORT = "streamable-http"
.\.venv\Scripts\python.exe .\app\mcp_server.py
```

Configure the plugin with:

```text
http://127.0.0.1:8000/mcp
```

The default listener is local-only. Keep it on `127.0.0.1` unless another
device must connect; the server currently has no authentication. For LAN
access, explicitly set `OBSIDIAN_RAG_HOST=0.0.0.0` (and optionally
`OBSIDIAN_RAG_PORT`), allow the port through the firewall, and add
authentication or another access-control layer.

## MCP tools

- `search_knowledge(query, top_k)`: semantic search with source metadata
- `query_knowledge(query, scope, entity, top_k)`: high-level setting search with
  deterministic category routing and source-cited results
- `retrieve_evidence(query, scope, entity, max_sources, token_budget)`: hybrid
  entity/vector retrieval, one-hop graph expansion, source diversity, and
  NotebookLM-style primary/related evidence bundles
- `get_related_sources(path, depth)`: inspect typed wikilinks, backlinks, and
  event relations
- `get_document(path)`: read one relative Markdown source
- `list_sources(folder)`: list eligible Markdown sources

`query_knowledge` supports these scopes: `characters`, `locations`, `species`,
`languages`, `srunes`, `technology`, `items`, `organizations`, `events`,
`legends`, and `factions`. Chinese aliases such as `角色`, `事件`, `法術`,
`組織`, and `派系` are also accepted. If a single category is clear from the
query, it is selected automatically; ambiguous queries search the full vault.
The search returns `scope_used` together with each result's source path. Use
`get_document` when the complete note is needed.

The index stores the category derived from the numbered setting folder and
selected frontmatter fields (`type`, `importance`, `entity_type`, `alive`,
`ranger`, `military`, `process_srune`, and event relation fields) together with
aliases and wikilinks in each chunk payload. Increment the index schema version
and run a full rebuild after changing this metadata schema.

The indexer keeps a normalized note at or below `max_tokens * 4` characters as
one chunk, even when it contains several headings. Longer notes are split on
heading boundaries; overlap is used only when an individual section exceeds
the same limit. Chunk IDs remain deterministic. Incremental runs delete old
chunks for each changed source before inserting its replacement, and delete
sources removed from the vault. Limited smoke-test runs do not update the
manifest or delete unrelated sources.

`retrieve_evidence` treats exact title/alias/entity matches and top semantic
hits as primary sources, expands one hop through the source graph, reranks and
deduplicates chunks, then packs them under a token budget. Every evidence item
contains a stable `source_path`, `heading`, and `chunk_id`, plus the relation
reason for graph-expanded sources. The bundle also reports
`grounding_confidence` and marks low-confidence answers as `uncertain`.

## Testing instructions

Run these from the project root after Qdrant and Ollama are up.

### 1. Empty Qdrant smoke test

Start Qdrant with an empty or new `qdrant_storage`, then:

```powershell
.\.venv\Scripts\python.exe -c "from app import mcp_server; print('import_ok')"
.\.venv\Scripts\python.exe -c "from app import mcp_server; print(mcp_server.list_sources('IU7')[:200])"
```

Expected:

- `import_ok`
- `list_sources` returns JSON paths under `Setting/`
- `search_knowledge` may fail with collection-not-found until you index

### 2. Small fake-embedding test (no Ollama GPU)

If Ollama CUDA fails, use deterministic fake embeddings for a tiny pipeline smoke test:

```powershell
.\.venv\Scripts\python.exe tests/test_embeddings.py --limit-documents 5 --query "星降神臨"
```

This uses `config.test.yaml` (`provider: fake`, collection `obsidian_test`).
Expected: `fake_embed_ok`, indexed chunks > 0, and search hits.

Run the deterministic cross-source retrieval evaluation:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests
```

The evaluation includes role/world-setting, event sequence, organization,
root-note, citation, and graph-relation cases. Cases are defined in
`retrieval_eval_cases.json`.

For Cursor MCP with the same fake provider, temporarily set `config.yaml` embedding provider to `fake`, or point the server at `config.test.yaml`.

### 3. Indexing test (real Ollama embeddings)

```powershell
.\.venv\Scripts\python.exe -m app.indexer
Invoke-RestMethod http://127.0.0.1:6333/collections/obsidian
```

Expected: collection `obsidian` exists and point count > 0.

### 4. Search test

```powershell
.\.venv\Scripts\python.exe -c "from app import mcp_server; print(mcp_server.search_knowledge('星降神臨', 3))"
```

Expected: JSON chunks with `source_path`, `text`, and `score`.

### 5. Document read test

```powershell
.\.venv\Scripts\python.exe -c "from app import mcp_server; print(mcp_server.get_document('IU7/05_srune/原初大法術．星降神臨.md')[:300])"
```

Expected: Markdown note content.

### 6. Cursor MCP test

1. Add the MCP config above.
2. Restart Cursor MCP / reload window.
3. Confirm tools appear: `search_knowledge`, `query_knowledge`,
   `retrieve_evidence`, `get_related_sources`, `get_document`, and
   `list_sources`.
5. Call `list_sources` with folder `IU7`.
6. Call `query_knowledge` with a Chinese query from the vault, for example
   `query_knowledge("星降神臨是甚麼法術？", scope="srunes", top_k=3)`.
7. Call `search_knowledge` with a Chinese query from the vault as the
   unfiltered fallback.
8. Call `retrieve_evidence` for cross-source questions and verify that its
   output separates `primary` and `related` evidence with citations.

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

`scripts/format_converter.py` converts explicit ruby markers and exactly-four-character
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
.\.venv\Scripts\python.exe scripts/format_converter.py input.md output.md
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
