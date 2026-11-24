# tab-header.ps1 — dot-source at the top of every Vault 3 terminal tab (off camera: it prints a personal path).
#   . C:\Dev\v3-preflight\tab-header.ps1              # Performance Edition: the public novel, the workshop already built
#   . C:\Dev\v3-preflight\tab-header.ps1 -NoTranscript
param([switch]$NoTranscript)
$PSVersionTable.PSVersion
if (-not $NoTranscript) {
    New-Item -ItemType Directory -Force "$HOME\v3-transcripts" | Out-Null
    Start-Transcript -Path "$HOME\v3-transcripts\performance-$(Get-Date -Format yyyyMMdd_HHmmss).txt" | Out-Null
}
# Vault 1 and 2 names, unchanged
$VS      = 'C:\Dev\vector-snake\vector_snake_v2.py'
$VS_PY   = "$env:USERPROFILE\.pyenv\pyenv-win\versions\3.11.9\python.exe"
$LAB_PY  = 'C:\Dev\smoke-lab\.venv\Scripts\python.exe'
# Vault 3
$DOOR_PY = 'C:\Dev\novel-door\.venv\Scripts\python.exe'
$BOOK    = 'C:\Dev\novel-ssot'
$MCP_LOG = "$env:LOCALAPPDATA\Claude\logs\mcp-server-novel_door.log"   # V3 rehearsal: LOCALAPPDATA, not APPDATA
$env:NOVEL_SSOT            = $BOOK
$env:NOVEL_REPO            = 'DamianGiambazi/novel-ssot'
$env:NOVEL_GITHUB_PROVIDER = 'novel-door-github'       # the Arcade provider made in the rehearsal (V3-S06)
$env:ARCADE_USAGE_TRACKING = '0'
$env:HF_HUB_OFFLINE        = '1'
$env:TEMP = 'C:\Dev\tmp'
$env:TMP  = 'C:\Dev\tmp'
# A clean call log for this run: an old one is archived, never deleted
foreach ($f in 'calls.jsonl', 'answers.txt', 'smoke-calls.jsonl') {
    $p = "C:\Dev\novel-door\$f"
    if (Test-Path $p) {
        New-Item -ItemType Directory -Force "$HOME\v3-evidence\archive" | Out-Null
        Move-Item $p "$HOME\v3-evidence\archive\$(Get-Date -Format yyyyMMdd_HHmmss)-$f"
    }
}
Set-Location $BOOK
"PERFORMANCE   BOOK $BOOK   REPO $env:NOVEL_REPO   KEY $env:NOVEL_GITHUB_PROVIDER"
Start-Sleep 2
Clear-Host
