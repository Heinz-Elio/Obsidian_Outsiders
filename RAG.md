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

## Novel formatting conversion

`format_converter.py` converts explicit ruby markers and four-or-more-character
fullwidth-dot notation:

```text
{{ruby:漢字|かんじ}}
甲．乙．丙．丁
```

For the whole vault, run the script without entering any Chinese text:

```powershell
.\.venv\Scripts\python.exe convert_vault.py
```

It reads `Setting/` and writes converted files to `rendered/`.

For one file, the lower-level converter is also available:

```powershell
.\.venv\Scripts\python.exe format_converter.py input.md output.md
```

The dot notation becomes a `bouten` span. Add this CSS in the rendered page:

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

Then select text in Obsidian or any editor and press `Ctrl+Shift+R`.
The script copies the selection, converts it, and pastes ruby HTML back.

CLI test:

```powershell
.\.venv\Scripts\python.exe convert_selection.py "地對空法力導引飛彈（Sruna homing Surface-to-Air Missile，SSAM）"
```
