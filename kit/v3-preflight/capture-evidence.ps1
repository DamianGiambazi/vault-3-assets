# capture-evidence.ps1 — OFF CAMERA, straight after the take. The PowerShell transcript drops native programs'
# output (Vault 2 lesson), so this re-runs the read-only checks and saves their full output to files.
#   C:\Dev\v3-preflight\capture-evidence.ps1 -Label TAKE
# It also copies Claude Desktop's MCP log for novel_door (V3 rehearsal: it lives in LOCALAPPDATA).
param([Parameter(Mandatory)][string]$Label)
$door = 'C:\Dev\novel-door'; $py = "$door\.venv\Scripts\python.exe"
$book = if ($env:NOVEL_SSOT) { $env:NOVEL_SSOT } else { 'C:\Dev\novel-ssot' }
$out = "$HOME\v3-evidence\$Label"; New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $book
git log --format='%h  %cI  %s' -8      *>&1 | Set-Content "$out\git-log.txt"
.\spine\seal-check-v3.ps1              *>&1 | Set-Content "$out\seal-check.txt"
Pop-Location
Push-Location $door
if (Test-Path answers.txt) { & $py score.py answers.txt *>&1 | Set-Content "$out\score.txt"; Copy-Item answers.txt $out }
if (Test-Path calls.jsonl) { duckdb -bail -f calls.sql *>&1 | Set-Content "$out\calls.txt"; Copy-Item calls.jsonl $out }
if (Test-Path smoke-calls.jsonl) { Copy-Item smoke-calls.jsonl $out }
uv pip list --python $py               *>&1 | Set-Content "$out\venv-packages.txt"
Pop-Location
$mcp = "$env:LOCALAPPDATA\Claude\logs\mcp-server-novel_door.log"
if (Test-Path $mcp) { Copy-Item $mcp "$out\mcp-server-novel_door.log" }
Get-ChildItem $out | Select-Object Name, Length | Format-Table -AutoSize
Get-Content "$out\seal-check.txt" -Tail 1
if (Test-Path "$out\score.txt") { Get-Content "$out\score.txt" -Tail 1 }
if (Test-Path "$out\calls.txt") { Select-String -Path "$out\calls.txt" -Pattern '(READER|FIREWALL_)\S*.*' | ForEach-Object { $_.Matches.Value.TrimEnd(' │') } }
"EVIDENCE_SAVED  $out"
