$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

$env:OBSIDIAN_RAG_TRANSPORT = "streamable-http"
if (-not $env:OBSIDIAN_RAG_HOST) { $env:OBSIDIAN_RAG_HOST = "127.0.0.1" }
if (-not $env:OBSIDIAN_RAG_PORT) { $env:OBSIDIAN_RAG_PORT = "8000" }

& .\.venv\Scripts\python.exe .\app\mcp_server.py
