# setup.ps1 — build the project-scoped venv for novel-door (off camera, P4; Vault 1 discipline).
# Run from C:\Dev\novel-door in PowerShell 7, non-elevated. Nothing is installed outside .venv\.
# Versions: the same sentence-transformers and torch as vector-snake used for the Vault 2 index (same
# translator), lancedb as in Vault 1's smoke-lab, and the Arcade MCP framework pinned for the series.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$env:TEMP = 'C:\Dev\tmp'; $env:TMP = 'C:\Dev\tmp'
$t = [Diagnostics.Stopwatch]::StartNew()
uv venv .venv --python 3.11
uv pip install --python .venv\Scripts\python.exe `
    arcade-mcp-server==1.33.0 lancedb==0.40.0 sentence-transformers==6.1.0 torch==2.14.1 httpx==0.28.1
$t.Stop()
.venv\Scripts\python.exe -c "import arcade_mcp_server, lancedb, sentence_transformers, torch; print('VENV_OK  torch', torch.__version__, ' sentence-transformers', sentence_transformers.__version__, ' lancedb', lancedb.__version__)"
"INSTALL_TIME  {0:mm\:ss}   <- write this on the Honest Cut card for D" -f $t.Elapsed
